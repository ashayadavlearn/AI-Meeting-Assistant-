from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field

# Auth Schemas
class UserRegister(BaseModel):
    email: str
    password: str = Field(min_length=6)
    full_name: str
    role: Optional[str] = "Product Lead"

class UserLogin(BaseModel):
    email: str
    password: str

class ForgotPasswordRequest(BaseModel):
    email: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    avatar: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Decision Schemas
class DecisionResponse(BaseModel):
    id: int
    meeting_id: int
    title: str
    rationale: str
    impact: str
    decision_maker: str
    created_at: datetime

    class Config:
        from_attributes = True

# Task Schemas
class TaskCreate(BaseModel):
    meeting_id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    owner: Optional[str] = "Unassigned"
    deadline: Optional[str] = "No deadline"
    priority: Optional[str] = "Medium"
    status: Optional[str] = "Pending"
    completion_percentage: Optional[int] = 0

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None
    deadline: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    completion_percentage: Optional[int] = None

class TaskResponse(BaseModel):
    id: int
    user_id: int
    meeting_id: Optional[int] = None
    meeting_title: Optional[str] = None
    title: str
    description: str
    owner: str
    deadline: str
    priority: str
    status: str
    completion_percentage: int
    created_at: datetime

    class Config:
        from_attributes = True

# Meeting Schemas
class MeetingCreate(BaseModel):
    title: Optional[str] = None
    date: Optional[str] = None
    duration_minutes: Optional[int] = 30
    meeting_type: Optional[str] = "Strategy"
    participants: Optional[List[str]] = []
    raw_transcript: str
    tags: Optional[List[str]] = []

class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    executive_summary: Optional[str] = None
    sentiment: Optional[str] = None
    tags: Optional[List[str]] = None

class MeetingResponse(BaseModel):
    id: int
    user_id: int
    title: str
    date: str
    duration_minutes: int
    meeting_type: str
    participants: List[str]
    raw_transcript: str
    executive_summary: str
    key_points: List[str]
    sentiment: str
    tags: List[str]
    audio_path: Optional[str] = None
    created_at: datetime
    decisions: List[DecisionResponse] = []
    tasks: List[TaskResponse] = []

    class Config:
        from_attributes = True

class MeetingListItem(BaseModel):
    id: int
    title: str
    date: str
    duration_minutes: int
    meeting_type: str
    participants_count: int
    executive_summary: str
    sentiment: str
    tags: List[str]
    tasks_count: int
    decisions_count: int
    created_at: datetime

    class Config:
        from_attributes = True

# Chat Schemas
class ChatRequest(BaseModel):
    message: str
    meeting_id: Optional[int] = None
    conversation_history: Optional[List[dict]] = []

class SourceCitation(BaseModel):
    meeting_id: int
    meeting_title: str
    snippet: str
    speaker: Optional[str] = ""
    relevance_score: float

class ChatResponse(BaseModel):
    reply: str
    sources: List[SourceCitation] = []
    action_suggestions: List[str] = []

# Search Schemas
class SearchQuery(BaseModel):
    query: str
    meeting_type: Optional[str] = None
    tag: Optional[str] = None
    priority: Optional[str] = None

class SearchResultItem(BaseModel):
    type: str  # "meeting", "task", "decision"
    id: int
    title: str
    snippet: str
    date: Optional[str] = None
    relevance: float
    meeting_id: Optional[int] = None
    meeting_title: Optional[str] = None
    metadata: Optional[dict] = {}

class SearchResponse(BaseModel):
    query: str
    total_results: int
    results: List[SearchResultItem]

# Notification Schemas
class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str
    type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Activity Log
class ActivityResponse(BaseModel):
    id: int
    action: str
    target: str
    details: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

# Analytics Schemas
class StatMetrics(BaseModel):
    total_meetings: int
    pending_tasks: int
    completed_tasks: int
    upcoming_deadlines: int
    total_decisions: int
    total_action_items: int
    ai_productivity_score: int
    avg_meeting_duration: int
    task_completion_rate: float

class AnalyticsResponse(BaseModel):
    metrics: StatMetrics
    meeting_frequency: List[dict]
    task_distribution: List[dict]
    active_contributors: List[dict]
    sentiment_distribution: List[dict]
    monthly_productivity: List[dict]
    recent_activities: List[ActivityResponse]
