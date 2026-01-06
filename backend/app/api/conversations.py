from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.services.conversation_service import ConversationService
from app.schemas import (
    ConversationCreate,
    ConversationUpdate,
    ConversationResponse,
    ConversationListResponse,
    MessageResponse,
)

router = APIRouter(prefix="/conversations", tags=["conversations"])


@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation: ConversationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new conversation."""
    return await ConversationService.create_conversation(db, conversation)


@router.get("/", response_model=List[ConversationListResponse])
async def list_conversations(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """List all conversations."""
    conversations = await ConversationService.list_conversations(db, skip, limit)
    
    # Convert to list response with message count
    result = []
    for conv in conversations:
        count = await ConversationService.get_message_count(db, conv.id)
        conv_dict = {
            "id": conv.id,
            "title": conv.title,
            "provider": conv.provider.value,
            "created_at": conv.created_at,
            "updated_at": conv.updated_at,
            "message_count": count
        }
        result.append(ConversationListResponse(**conv_dict))
    
    return result


@router.get("/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific conversation with messages."""
    conversation = await ConversationService.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Load messages
    messages = await ConversationService.get_messages(db, conversation_id)
    
    # Convert to response format
    conv_dict = {
        "id": conversation.id,
        "title": conversation.title,
        "provider": conversation.provider.value,
        "model": conversation.model,
        "temperature": conversation.temperature,
        "max_tokens": conversation.max_tokens,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "messages": [
            {
                "id": msg.id,
                "conversation_id": msg.conversation_id,
                "role": msg.role.value,
                "content": msg.content,
                "error": msg.error,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }
    
    return ConversationResponse(**conv_dict)


@router.patch("/{conversation_id}", response_model=ConversationResponse)
async def update_conversation(
    conversation_id: UUID,
    update_data: ConversationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a conversation."""
    conversation = await ConversationService.update_conversation(
        db, conversation_id, update_data
    )
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Load messages
    messages = await ConversationService.get_messages(db, conversation_id)
    
    conv_dict = {
        "id": conversation.id,
        "title": conversation.title,
        "provider": conversation.provider.value,
        "model": conversation.model,
        "temperature": conversation.temperature,
        "max_tokens": conversation.max_tokens,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "messages": [
            {
                "id": msg.id,
                "conversation_id": msg.conversation_id,
                "role": msg.role.value,
                "content": msg.content,
                "error": msg.error,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }
    
    return ConversationResponse(**conv_dict)


@router.delete("/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a conversation."""
    deleted = await ConversationService.delete_conversation(db, conversation_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    return None


@router.get("/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_messages(
    conversation_id: UUID,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get messages for a conversation."""
    # Verify conversation exists
    conversation = await ConversationService.get_conversation(db, conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    messages = await ConversationService.get_messages(db, conversation_id, skip, limit)
    
    return [
        MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role.value,
            content=msg.content,
            error=msg.error,
            created_at=msg.created_at
        )
        for msg in messages
    ]
