from sqlalchemy import Column, String, ForeignKey, Text, Float, JSON, Enum, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class User(BaseModel):
    __tablename__ = 'users'
    email = Column(String, unique=True, index=True, nullable=False)
    businesses = relationship("Business", back_populates="owner")

class Business(BaseModel):
    __tablename__ = 'businesses'
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=True)
    profile_summary = Column(Text, nullable=True)
    owner = relationship("User", back_populates="businesses")
    documents = relationship("BusinessDocument", back_populates="business")
    analyses = relationship("BusinessAnalysis", back_populates="business")
    strategies = relationship("Strategy", back_populates="business")

class BusinessDocument(BaseModel):
    __tablename__ = 'business_documents'
    business_id = Column(ForeignKey('businesses.id'), nullable=False, index=True)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="pending")
    business = relationship("Business", back_populates="documents")

class BusinessAnalysis(BaseModel):
    __tablename__ = 'business_analyses'
    business_id = Column(ForeignKey('businesses.id'), nullable=False, index=True)
    content = Column(JSON, nullable=False)
    business = relationship("Business", back_populates="analyses")

class Strategy(BaseModel):
    __tablename__ = 'strategies'
    business_id = Column(ForeignKey('businesses.id'), nullable=False, index=True)
    goals = Column(JSON, nullable=False)
    status = Column(String, nullable=False, default="active")
    business = relationship("Business", back_populates="strategies")
    campaigns = relationship("Campaign", back_populates="strategy")

class Campaign(BaseModel):
    __tablename__ = 'campaigns'
    strategy_id = Column(ForeignKey('strategies.id'), nullable=False, index=True)
    title = Column(String, nullable=False)
    budget = Column(Float, nullable=True)
    status = Column(String, nullable=False, default="draft")
    strategy = relationship("Strategy", back_populates="campaigns")

class Recommendation(BaseModel):
    __tablename__ = 'recommendations'
    business_id = Column(ForeignKey('businesses.id'), nullable=False, index=True)
    agent_source = Column(String, nullable=False)
    content = Column(JSON, nullable=False)
    status = Column(String, nullable=False, default="pending") # pending, approved, rejected

class KPIMetric(BaseModel):
    __tablename__ = 'kpi_metrics'
    business_id = Column(ForeignKey('businesses.id'), nullable=False, index=True)
    metric_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    recorded_at = Column(DateTime(timezone=True), nullable=False)

class Memory(BaseModel):
    __tablename__ = 'memories'
    business_id = Column(ForeignKey('businesses.id'), nullable=False, index=True)
    context = Column(Text, nullable=False)
    memory_type = Column(String, nullable=False) # e.g., 'campaign_outcome', 'kpi_trend'

class ChatHistory(BaseModel):
    __tablename__ = 'chat_histories'
    session_id = Column(String, nullable=False, index=True)
    role = Column(String, nullable=False) # 'user' or 'ai'
    content = Column(Text, nullable=False)
    metadata_info = Column(JSON, nullable=True) # avoiding 'metadata' reserved word

class AgentLog(BaseModel):
    __tablename__ = 'agent_logs'
    trace_id = Column(String, nullable=False, index=True)
    agent_name = Column(String, nullable=False)
    action = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
