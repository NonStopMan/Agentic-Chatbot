from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List
from uuid import UUID


class AIProviderEnum(str):
    """AI provider enum."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    LOCAL = "local"


class MessageRoleEnum(str):
    """Message role enum."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


# Message Schemas
class MessageBase(BaseModel):
    """Base message schema."""
    role: str
    content: str
    error: Optional[str] = None


class MessageCreate(MessageBase):
    """Message creation schema."""
    pass


class MessageResponse(MessageBase):
    """Message response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    conversation_id: UUID
    created_at: datetime


# Conversation Schemas
class ConversationBase(BaseModel):
    """Base conversation schema."""
    title: str
    provider: str
    model: Optional[str] = None
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=2048, gt=0)


class ConversationCreate(ConversationBase):
    """Conversation creation schema."""
    pass


class ConversationUpdate(BaseModel):
    """Conversation update schema."""
    title: Optional[str] = None
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = Field(default=None, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, gt=0)


class ConversationResponse(ConversationBase):
    """Conversation response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []


class ConversationListResponse(BaseModel):
    """Conversation list response schema."""
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    title: str
    provider: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0


# Chat Schemas
class ChatRequest(BaseModel):
    """Chat request schema."""
    content: str = Field(..., min_length=1)
    conversation_id: Optional[UUID] = None
    provider: str = "openai"
    model: Optional[str] = None
    temperature: Optional[float] = Field(default=0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=2048, gt=0)
    stream: bool = True


class ChatResponse(BaseModel):
    """Chat response schema."""
    conversation_id: UUID
    message: MessageResponse


# WebSocket Message Schemas
class WebSocketMessage(BaseModel):
    """WebSocket message schema."""
    type: str  # 'message' | 'stream' | 'error' | 'system' | 'end'
    data: dict


# Health Check
class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    database: str
    redis: str
    providers: dict
