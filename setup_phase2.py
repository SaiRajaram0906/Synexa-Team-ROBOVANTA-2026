import os

root_dir = "/home/ruban/Documents/robovantha/hackathon/synexa-growth-os"

files = {
    # ---------------------------------------------------------
    # 1. DATABASE MODELS (SQLAlchemy)
    # ---------------------------------------------------------
    "backend/app/models/base.py": """import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
""",
    "backend/app/models/domain.py": """from sqlalchemy import Column, String, ForeignKey, Text, Float, JSON, Enum
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
""",
    # ---------------------------------------------------------
    # 2. SCHEMAS (Pydantic)
    # ---------------------------------------------------------
    "backend/app/schemas/domain.py": """from pydantic import BaseModel, UUID4, ConfigDict
from typing import Optional, Dict, Any, List
from datetime import datetime

class SchemaBase(BaseModel):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserSchema(SchemaBase):
    email: str

class BusinessCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    profile_summary: Optional[str] = None

class BusinessSchema(SchemaBase, BusinessCreate):
    user_id: UUID4
""",
    # ---------------------------------------------------------
    # 3. FASTAPI SUPABASE AUTH MIDDLEWARE
    # ---------------------------------------------------------
    "backend/app/middleware/auth.py": """from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import jwt # PyJWT

security = HTTPBearer()

def verify_supabase_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    supabase_jwt_secret = os.getenv("SUPABASE_JWT_SECRET")
    
    if not supabase_jwt_secret:
        raise HTTPException(status_code=500, detail="Missing SUPABASE_JWT_SECRET environment variable")

    try:
        # Supabase uses HS256 algorithm by default
        payload = jwt.decode(
            token,
            supabase_jwt_secret,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(payload: dict = Depends(verify_supabase_token)):
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid user context in token")
    email = payload.get("email")
    return {"id": user_id, "email": email}
""",
    # ---------------------------------------------------------
    # 4. CREWAI AGENT DEFINITIONS
    # ---------------------------------------------------------
    "ai/llm_config.py": """from langchain_google_genai import ChatGoogleGenerativeAI
import os

def get_gemini_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.7
    )
""",
    "ai/agents/ceo_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm

class CEOAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Executive Officer",
            goal="Coordinate business experts, resolve high-level conflicts, and make final executive decisions based on strategic and financial inputs.",
            backstory="A seasoned executive capable of synthesizing inputs from Marketing, Sales, Operations, and Finance to ensure sustainable business growth.",
            verbose=True,
            allow_delegation=True,
            llm=self.llm,
            tools=[] # TODO: Add tools (e.g., DecisionEngine Tool)
        )
""",
    "ai/agents/marketing_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm

class MarketingAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Marketing Officer",
            goal="Design high-converting marketing campaigns based on the overarching business strategy.",
            backstory="An expert marketer who relies on data and trends to acquire new customers efficiently.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[] # TODO: Add tools
        )
""",
    "ai/agents/sales_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm

class SalesAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="VP of Sales",
            goal="Optimize conversion pipelines and design sales scripts to turn leads into revenue.",
            backstory="A results-driven sales leader focused on closing deals and optimizing the sales funnel.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
""",
    "ai/agents/finance_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm

class FinanceAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Financial Officer",
            goal="Evaluate ROI of proposed campaigns, enforce budget constraints, and manage financial risk.",
            backstory="A conservative financial planner who ensures that growth does not come at the cost of profitability.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
""",
    "ai/agents/operations_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm

class OperationsAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Operating Officer",
            goal="Ensure fulfillment capacity can handle projected sales volume and identify operational bottlenecks.",
            backstory="A process-oriented leader who ensures that the business can deliver on its promises to customers.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
""",
    "ai/agents/customer_success_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm

class CustomerSuccessAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Head of Customer Success",
            goal="Analyze customer feedback, predict churn, and suggest retention strategies.",
            backstory="A customer-obsessed advocate who believes retention is the true driver of long-term growth.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
""",
    "ai/agents/strategy_agent.py": """from crewai import Agent
from ai.llm_config import get_gemini_llm

class StrategyAgent:
    def __init__(self):
        self.llm = get_gemini_llm()

    def create(self):
        return Agent(
            role="Chief Strategy Officer",
            goal="Formulate quarterly and annual strategic objectives based on market analysis and business capabilities.",
            backstory="A visionary thinker who maps out the long-term direction of the business.",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=[]
        )
""",
    "ai/tasks/strategy_tasks.py": """from crewai import Task

class StrategyTasks:
    def design_strategy(self, agent, business_context):
        return Task(
            description=f"TODO: Implement strategy design logic using context: {business_context}",
            expected_output="A structured JSON strategic plan outlining quarterly objectives.",
            agent=agent
        )
""",
    "ai/tasks/execution_tasks.py": """from crewai import Task

class ExecutionTasks:
    def plan_marketing_campaign(self, agent, strategy_plan):
        return Task(
            description=f"TODO: Implement marketing campaign logic based on: {strategy_plan}",
            expected_output="A detailed marketing campaign proposal including budget and channels.",
            agent=agent
        )
    
    def review_budget(self, agent, campaign_proposal):
        return Task(
            description=f"TODO: Evaluate the ROI and budget feasibility of the campaign: {campaign_proposal}",
            expected_output="Approval or rejection decision with financial justification.",
            agent=agent
        )
""",
    "ai/tasks/ceo_tasks.py": """from crewai import Task

class CEOTasks:
    def evaluate_and_approve(self, agent, sub_agent_outputs):
        return Task(
            description=f"TODO: Review all sub-agent outputs and resolve conflicts: {sub_agent_outputs}",
            expected_output="Final executive decision and aggregated recommendations for the user.",
            agent=agent
        )
""",
    "ai/crews/executive_crew.py": """from crewai import Crew, Process
from ai.agents.ceo_agent import CEOAgent
from ai.agents.strategy_agent import StrategyAgent
from ai.agents.marketing_agent import MarketingAgent
from ai.agents.finance_agent import FinanceAgent
from ai.tasks.strategy_tasks import StrategyTasks
from ai.tasks.execution_tasks import ExecutionTasks
from ai.tasks.ceo_tasks import CEOTasks

class ExecutiveCrewManager:
    def __init__(self):
        self.ceo = CEOAgent().create()
        self.strategy = StrategyAgent().create()
        self.marketing = MarketingAgent().create()
        self.finance = FinanceAgent().create()
        
        self.strategy_tasks = StrategyTasks()
        self.exec_tasks = ExecutionTasks()
        self.ceo_tasks = CEOTasks()

    def run_growth_cycle(self, business_context):
        # 1. Define Tasks
        t_strategy = self.strategy_tasks.design_strategy(self.strategy, business_context)
        t_marketing = self.exec_tasks.plan_marketing_campaign(self.marketing, "TODO: inject strategy output")
        t_finance = self.exec_tasks.review_budget(self.finance, "TODO: inject marketing output")
        t_ceo_final = self.ceo_tasks.evaluate_and_approve(self.ceo, "TODO: inject all outputs")

        # 2. Assemble Crew
        crew = Crew(
            agents=[self.strategy, self.marketing, self.finance, self.ceo],
            tasks=[t_strategy, t_marketing, t_finance, t_ceo_final],
            process=Process.sequential, # Can be modified to hierarchical if CEO delegates directly
            verbose=True
        )

        return crew.kickoff()
""",
    # ---------------------------------------------------------
    # 5. FRONTEND SUPABASE AUTH
    # ---------------------------------------------------------
    "frontend/src/lib/supabase.ts": """import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
""",
    "frontend/src/app/(auth)/login/page.tsx": """'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';
import { useAppStore } from '@/store';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const setUser = useAppStore((state) => state.setUser);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) {
      setError(error.message);
    } else {
      setUser(data.user);
      router.push('/dashboard');
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gray-50">
      <form onSubmit={handleLogin} className="w-96 rounded-lg bg-white p-8 shadow-md">
        <h1 className="mb-6 text-2xl font-bold">Login</h1>
        {error && <div className="mb-4 text-red-500">{error}</div>}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required className="mt-1 w-full rounded border p-2" />
        </div>
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required className="mt-1 w-full rounded border p-2" />
        </div>
        <button type="submit" className="w-full rounded bg-blue-600 p-2 text-white hover:bg-blue-700">Login</button>
      </form>
    </div>
  );
}
""",
    "frontend/src/app/(auth)/register/page.tsx": """'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabase';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    const { data, error } = await supabase.auth.signUp({ email, password });
    if (error) {
      setError(error.message);
    } else {
      router.push('/login');
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-gray-50">
      <form onSubmit={handleRegister} className="w-96 rounded-lg bg-white p-8 shadow-md">
        <h1 className="mb-6 text-2xl font-bold">Register</h1>
        {error && <div className="mb-4 text-red-500">{error}</div>}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required className="mt-1 w-full rounded border p-2" />
        </div>
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700">Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required className="mt-1 w-full rounded border p-2" />
        </div>
        <button type="submit" className="w-full rounded bg-green-600 p-2 text-white hover:bg-green-700">Register</button>
      </form>
    </div>
  );
}
""",
    "frontend/src/middleware.ts": """import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value,
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value,
            ...options,
          })
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value: '',
            ...options,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value: '',
            ...options,
          })
        },
      },
    }
  )

  const { data: { user } } = await supabase.auth.getUser()

  // Protected routes condition
  const isProtectedRoute = request.nextUrl.pathname.startsWith('/dashboard') || 
                           request.nextUrl.pathname.startsWith('/strategy') ||
                           request.nextUrl.pathname.startsWith('/analytics') ||
                           request.nextUrl.pathname.startsWith('/copilot') ||
                           request.nextUrl.pathname.startsWith('/campaigns');

  if (isProtectedRoute && !user) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return response
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
"""
}

# Create missing directories
import os
os.makedirs(os.path.join(root_dir, "backend/app/models"), exist_ok=True)
os.makedirs(os.path.join(root_dir, "backend/app/schemas"), exist_ok=True)
os.makedirs(os.path.join(root_dir, "backend/app/middleware"), exist_ok=True)


# Write files
for path, content in files.items():
    file_path = os.path.join(root_dir, path)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(content)

print("Phase 2 scaffolding completed successfully.")
