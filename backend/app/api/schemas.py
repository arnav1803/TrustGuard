from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class VerificationStatus(str, Enum):
    PENDING = "pending"
    TRUE = "true"
    FALSE = "false"
    PARTIALLY_TRUE = "partially_true"
    MISLEADING = "misleading"
    UNVERIFIABLE = "unverifiable"

class AlertSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# User schemas
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

class UserResponse(BaseSchema):
    id: int
    username: str
    email: str
    created_at: datetime
    is_active: bool = True

# Claim schemas
class ClaimCreate(BaseModel):
    text: str
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    
    @validator('text')
    def validate_text(cls, v):
        if len(v.strip()) < 10:
            raise ValueError('Claim text must be at least 10 characters long')
        return v.strip()

class ClaimResponse(BaseSchema):
    id: int
    text: str
    source: Optional[str]
    user_id: int
    verification_status: Optional[VerificationStatus] = VerificationStatus.PENDING
    created_at: datetime
    updated_at: Optional[datetime]
    metadata: Optional[Dict[str, Any]]

# Verification schemas
class VerificationResponse(BaseSchema):
    id: int
    claim_id: int
    verdict: VerificationStatus
    confidence_score: float
    evidence: List[str]
    sources: List[str]
    verified_at: datetime
    explanation: Optional[str]
    
    @validator('confidence_score')
    def validate_confidence(cls, v):
        if not 0 <= v <= 1:
            raise ValueError('Confidence score must be between 0 and 1')
        return v

# Trend analysis schemas
class TrendData(BaseModel):
    date: datetime
    claim_count: int
    false_claim_count: int
    trending_topics: List[str]

class TrendAnalysisResponse(BaseModel):
    period_days: int
    total_claims: int
    false_claims_percentage: float
    trending_topics: List[str]
    daily_trends: List[TrendData]
    top_sources: List[Dict[str, Any]]
    misinformation_categories: Dict[str, int]

# Alert schemas
class AlertResponse(BaseModel):
    id: str
    title: str
    message: str
    severity: AlertSeverity
    category: str
    created_at: datetime
    is_active: bool = True
    metadata: Optional[Dict[str, Any]]

# Batch processing schemas
class BatchClaimCreate(BaseModel):
    claims: List[ClaimCreate]
    batch_name: Optional[str]
    
    @validator('claims')
    def validate_claims_count(cls, v):
        if len(v) > 100:
            raise ValueError('Maximum 100 claims per batch')
        return v

class BatchProcessingResponse(BaseModel):
    batch_id: str
    status: str
    total_claims: int
    processed_claims: int
    failed_claims: int
    started_at: datetime
    completed_at: Optional[datetime]

# Search and filter schemas
class ClaimSearchRequest(BaseModel):
    query: Optional[str]
    status: Optional[VerificationStatus]
    source: Optional[str]
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    limit: int = 20
    offset: int = 0
    
    @validator('limit')
    def validate_limit(cls, v):
        if v > 100:
            raise ValueError('Maximum limit is 100')
        return v

class SearchResponse(BaseModel):
    total_count: int
    results: List[ClaimResponse]
    has_more: bool

# Statistics schemas
class ClaimStatistics(BaseModel):
    total_claims: int
    verified_claims: int
    false_claims: int
    true_claims: int
    pending_claims: int
    verification_rate: float

class SystemStatistics(BaseModel):
    claim_stats: ClaimStatistics
    active_users: int
    recent_activity: List[Dict[str, Any]]
    system_health: Dict[str, Any]

# Export schemas
class ExportRequest(BaseModel):
    format: str = "json"  # json, csv, xlsx
    filters: Optional[ClaimSearchRequest]
    include_verifications: bool = True
    
    @validator('format')
    def validate_format(cls, v):
        if v not in ['json', 'csv', 'xlsx']:
            raise ValueError('Format must be json, csv, or xlsx')
        return v

class ExportResponse(BaseModel):
    export_id: str
    status: str
    download_url: Optional[str]
    created_at: datetime
    expires_at: datetime

# Webhook schemas
class WebhookEvent(BaseModel):
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime

class WebhookResponse(BaseModel):
    success: bool
    message: str

# Error schemas
class ErrorResponse(BaseModel):
    error: str
    detail: str
    timestamp: datetime = datetime.utcnow()

# API Key schemas
class APIKeyCreate(BaseModel):
    name: str
    permissions: List[str]
    expires_at: Optional[datetime]

class APIKeyResponse(BaseModel):
    id: str
    name: str
    key: str  # Only returned on creation
    permissions: List[str]
    created_at: datetime
    expires_at: Optional[datetime]
    is_active: bool = True