from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional
from uuid import UUID

from app.models import Conversation, Message, MessageRole
from app.schemas import ConversationCreate, ConversationUpdate, MessageCreate
import logging

logger = logging.getLogger(__name__)


class ConversationService:
    """Service for conversation operations."""
    
    @staticmethod
    async def create_conversation(
        db: AsyncSession,
        conversation_data: ConversationCreate
    ) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(**conversation_data.model_dump())
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        logger.info(f"Created conversation: {conversation.id}")
        return conversation
    
    @staticmethod
    async def get_conversation(
        db: AsyncSession,
        conversation_id: UUID
    ) -> Optional[Conversation]:
        """Get conversation by ID with messages."""
        result = await db.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        return result.scalar_one_or_none()
    
    @staticmethod
    async def list_conversations(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 50
    ) -> List[Conversation]:
        """List conversations ordered by updated_at."""
        result = await db.execute(
            select(Conversation)
            .order_by(desc(Conversation.updated_at))
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def update_conversation(
        db: AsyncSession,
        conversation_id: UUID,
        update_data: ConversationUpdate
    ) -> Optional[Conversation]:
        """Update conversation."""
        conversation = await ConversationService.get_conversation(db, conversation_id)
        if not conversation:
            return None
        
        update_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(conversation, key, value)
        
        await db.commit()
        await db.refresh(conversation)
        logger.info(f"Updated conversation: {conversation_id}")
        return conversation
    
    @staticmethod
    async def delete_conversation(
        db: AsyncSession,
        conversation_id: UUID
    ) -> bool:
        """Delete conversation."""
        conversation = await ConversationService.get_conversation(db, conversation_id)
        if not conversation:
            return False
        
        await db.delete(conversation)
        await db.commit()
        logger.info(f"Deleted conversation: {conversation_id}")
        return True
    
    @staticmethod
    async def add_message(
        db: AsyncSession,
        conversation_id: UUID,
        message_data: MessageCreate
    ) -> Optional[Message]:
        """Add message to conversation."""
        # Verify conversation exists
        conversation = await ConversationService.get_conversation(db, conversation_id)
        if not conversation:
            return None
        
        message = Message(
            conversation_id=conversation_id,
            **message_data.model_dump()
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)
        logger.info(f"Added message to conversation: {conversation_id}")
        return message
    
    @staticmethod
    async def get_messages(
        db: AsyncSession,
        conversation_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[Message]:
        """Get messages for a conversation."""
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())
    
    @staticmethod
    async def get_message_count(
        db: AsyncSession,
        conversation_id: UUID
    ) -> int:
        """Get message count for a conversation."""
        result = await db.execute(
            select(func.count(Message.id))
            .where(Message.conversation_id == conversation_id)
        )
        return result.scalar() or 0
