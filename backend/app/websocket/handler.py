import socketio
import logging
from uuid import UUID, uuid4
from typing import Optional

from app.core.database import AsyncSessionLocal
from app.services.ai import provider_manager
from app.services.conversation_service import ConversationService
from app.schemas import MessageCreate, ConversationCreate

logger = logging.getLogger(__name__)

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    logger=True,
    engineio_logger=True
)


@sio.event
async def connect(sid, environ):
    """Handle client connection."""
    logger.info(f"Client connected: {sid}")
    await sio.emit('message', {
        'type': 'system',
        'data': {'content': 'Connected to server'}
    }, room=sid)


@sio.event
async def disconnect(sid):
    """Handle client disconnection."""
    logger.info(f"Client disconnected: {sid}")


@sio.event
async def chat_message(sid, data):
    """
    Handle incoming chat messages.
    
    Expected data format:
    {
        'type': 'message',
        'data': {
            'content': str,
            'provider': str,
            'conversationId': str (optional),
            'model': str (optional),
            'temperature': float (optional),
            'maxTokens': int (optional)
        }
    }
    """
    try:
        logger.info(f"Received message from {sid}: {data}")
        
        # Extract message data
        message_data = data.get('data', {})
        content = message_data.get('content')
        provider_name = message_data.get('provider', 'openai')
        conversation_id_str = message_data.get('conversationId')
        model = message_data.get('model')
        temperature = message_data.get('temperature', 0.7)
        max_tokens = message_data.get('maxTokens', 2048)
        
        if not content:
            await sio.emit('message', {
                'type': 'error',
                'data': {'error': 'Message content is required'}
            }, room=sid)
            return
        
        # Get AI provider
        provider = provider_manager.get_provider(provider_name)
        if not provider:
            await sio.emit('message', {
                'type': 'error',
                'data': {'error': f'Provider {provider_name} is not available'}
            }, room=sid)
            return
        
        # Database operations
        async with AsyncSessionLocal() as db:
            # Get or create conversation
            conversation_id = None
            if conversation_id_str:
                try:
                    conversation_id = UUID(conversation_id_str)
                    conversation = await ConversationService.get_conversation(db, conversation_id)
                    if not conversation:
                        logger.warning(f"Conversation {conversation_id} not found, creating new one")
                        conversation_id = None
                except ValueError:
                    logger.error(f"Invalid conversation ID: {conversation_id_str}")
                    conversation_id = None
            
            if not conversation_id:
                # Create new conversation
                conversation_create = ConversationCreate(
                    title=content[:50] + ('...' if len(content) > 50 else ''),
                    provider=provider_name,
                    model=model or provider.get_default_model(),
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                conversation = await ConversationService.create_conversation(db, conversation_create)
                conversation_id = conversation.id
                
                # Send conversation ID to client
                await sio.emit('message', {
                    'type': 'system',
                    'data': {
                        'conversationId': str(conversation_id),
                        'message': 'New conversation created'
                    }
                }, room=sid)
            
            # Save user message
            user_message = MessageCreate(
                role='user',
                content=content
            )
            await ConversationService.add_message(db, conversation_id, user_message)
            
            # Get conversation history
            messages = await ConversationService.get_messages(db, conversation_id)
            
            # Convert to provider format
            message_history = [
                {'role': msg.role, 'content': msg.content}
                for msg in messages
            ]
        
        # Stream AI response
        assistant_message_id = str(uuid4())
        accumulated_content = ""
        
        try:
            async for chunk in provider.chat(
                messages=message_history,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True
            ):
                accumulated_content += chunk
                
                # Send streaming chunk
                await sio.emit('message', {
                    'type': 'stream',
                    'data': {
                        'conversationId': str(conversation_id),
                        'messageId': assistant_message_id,
                        'content': chunk,
                        'role': 'assistant'
                    }
                }, room=sid)
            
            # Send end signal
            await sio.emit('message', {
                'type': 'end',
                'data': {
                    'conversationId': str(conversation_id),
                    'messageId': assistant_message_id
                }
            }, room=sid)
            
            # Save assistant message to database
            async with AsyncSessionLocal() as db:
                assistant_message = MessageCreate(
                    role='assistant',
                    content=accumulated_content
                )
                await ConversationService.add_message(db, conversation_id, assistant_message)
        
        except Exception as e:
            logger.error(f"Error during AI streaming: {str(e)}")
            await sio.emit('message', {
                'type': 'error',
                'data': {
                    'conversationId': str(conversation_id) if conversation_id else None,
                    'error': str(e)
                }
            }, room=sid)
    
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}", exc_info=True)
        await sio.emit('message', {
            'type': 'error',
            'data': {'error': 'Internal server error'}
        }, room=sid)


# Create ASGI application
socket_app = socketio.ASGIApp(sio)
