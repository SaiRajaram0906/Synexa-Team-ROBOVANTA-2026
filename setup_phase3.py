import os
import textwrap

root_dir = "/home/ruban/Documents/robovantha/hackathon/synexa-growth-os"

files = {
    # ---------------------------------------------------------
    # 1. ALEMBIC MIGRATIONS LAYER
    # ---------------------------------------------------------
    "backend/alembic.ini": """[alembic]
script_location = alembic
sqlalchemy.url = %(DATABASE_URL)s

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""",
    "backend/alembic/env.py": """from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
from dotenv import load_dotenv

load_dotenv()
from app.models.base import Base
# Import all models to ensure they are registered with Base.metadata
from app.models.domain import User, Business, BusinessDocument, BusinessAnalysis, Strategy, Campaign, Recommendation, KPIMetric, Memory, ChatHistory, AgentLog

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
db_url = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost/db")
config.set_main_option("sqlalchemy.url", db_url)

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
""",
    "backend/alembic/script.py.mako": """\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"\"\"
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
""",
    "backend/app/db.py": """from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:password@localhost/db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""",
    # ---------------------------------------------------------
    # 2. BACKEND API & SERVICES LAYER
    # ---------------------------------------------------------
    "backend/app/repositories/base.py": """from sqlalchemy.orm import Session
from uuid import UUID

class BaseRepository:
    def __init__(self, db: Session, model):
        self.db = db
        self.model = model
    
    def get_by_id(self, id: UUID):
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self):
        return self.db.query(self.model).all()
    
    def create(self, obj_in: dict):
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj
""",
    "backend/app/services/business_service.py": """from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository
from app.models.domain import Business
from uuid import UUID

class BusinessService:
    def __init__(self, db: Session):
        self.repo = BaseRepository(db, Business)
    
    def create_business(self, user_id: str, data: dict):
        data["user_id"] = user_id
        return self.repo.create(data)
        
    def get_business(self, business_id: UUID):
        return self.repo.get_by_id(business_id)
        
    def get_all_businesses(self):
        return self.repo.get_all()
""",
    "backend/app/services/ai_service.py": """class AIService:
    def __init__(self):
        pass
        
    def run_strategy_agent(self, business_id: str):
        # TODO: Trigger LangGraph/CrewAI execution for strategy
        return {"status": "success", "message": "Strategy generation triggered (TODO)"}
        
    def chat_with_copilot(self, business_id: str, message: str):
        # TODO: Pipe message to CEO Agent in CrewAI
        return {"response": "This is a placeholder response from the CEO Agent."}
""",
    "backend/app/api/v1/business.py": """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db import get_db
from app.services.business_service import BusinessService
from app.middleware.auth import get_current_user

router = APIRouter()

@router.post("/")
def create_business(data: dict, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = BusinessService(db)
    return service.create_business(current_user["id"], data)

@router.get("/")
def get_businesses(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = BusinessService(db)
    return service.get_all_businesses()

@router.get("/{id}")
def get_business(id: UUID, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    service = BusinessService(db)
    return service.get_business(id)
""",
    "backend/app/api/v1/analysis.py": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.middleware.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/start")
def start_analysis(business_id: str, current_user: dict = Depends(get_current_user)):
    # TODO: Implement trigger for analysis workflow
    return {"status": "started"}

@router.get("/{id}")
def get_analysis(id: str, current_user: dict = Depends(get_current_user)):
    return {"TODO": "Return analysis results"}
""",
    "backend/app/api/v1/strategy.py": """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.middleware.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/generate")
def generate_strategy(business_id: str, current_user: dict = Depends(get_current_user)):
    service = AIService()
    return service.run_strategy_agent(business_id)

@router.get("/")
def get_strategy(business_id: str, current_user: dict = Depends(get_current_user)):
    return {"TODO": "Return generated strategies"}
""",
    "backend/app/api/v1/dashboard.py": """from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user

router = APIRouter()

@router.get("/")
def get_dashboard_summary(business_id: str, current_user: dict = Depends(get_current_user)):
    return {"TODO": "Return high level dashboard stats"}

@router.get("/kpis")
def get_kpis(business_id: str, current_user: dict = Depends(get_current_user)):
    return {"TODO": "Return KPI metrics"}
""",
    "backend/app/api/v1/copilot.py": """from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/chat")
def chat_copilot(data: dict, current_user: dict = Depends(get_current_user)):
    service = AIService()
    return service.chat_with_copilot(data.get("business_id"), data.get("message"))
""",
    "backend/app/main.py": """from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.business import router as business_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.copilot import router as copilot_router
from app.api.v1.strategy import router as strategy_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.documents import router as documents_router

app = FastAPI(title="Synexa Growth OS API")

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(business_router, prefix="/api/v1/business", tags=["Business"])
app.include_router(analysis_router, prefix="/api/v1/analysis", tags=["Analysis"])
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(strategy_router, prefix="/api/v1/strategy", tags=["Strategy"])
app.include_router(copilot_router, prefix="/api/v1/copilot", tags=["Copilot"])
app.include_router(analytics_router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(documents_router, prefix="/api/v1/documents", tags=["Documents"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
""",

    # ---------------------------------------------------------
    # 3. FRONTEND DASHBOARD FOUNDATION
    # ---------------------------------------------------------
    "frontend/src/components/layout/Navbar.tsx": """import { useAppStore } from '@/store';

export default function Navbar() {
  const user = useAppStore((state) => state.user);
  return (
    <nav className="flex items-center justify-between bg-white px-6 py-4 shadow-sm">
      <div className="font-bold text-xl text-blue-600">Synexa Growth OS</div>
      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-600">{user?.email || 'User'}</span>
        <button className="rounded bg-gray-100 px-3 py-1 text-sm hover:bg-gray-200">Logout</button>
      </div>
    </nav>
  );
}
""",
    "frontend/src/components/layout/Sidebar.tsx": """import Link from 'next/link';

export default function Sidebar() {
  const links = [
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Discovery', href: '/discovery' },
    { name: 'Analysis', href: '/analysis' },
    { name: 'Strategy', href: '/strategy' },
    { name: 'Campaigns', href: '/campaigns' },
    { name: 'Analytics', href: '/analytics' },
    { name: 'AI Copilot', href: '/copilot' },
    { name: 'Settings', href: '/settings' },
  ];

  return (
    <aside className="w-64 bg-gray-900 text-white min-h-screen p-4 flex flex-col gap-2">
      {links.map((link) => (
        <Link key={link.name} href={link.href} className="p-2 hover:bg-gray-800 rounded">
          {link.name}
        </Link>
      ))}
    </aside>
  );
}
""",
    "frontend/src/app/(dashboard)/layout.tsx": """import Sidebar from '@/components/layout/Sidebar';
import Navbar from '@/components/layout/Navbar';

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen overflow-hidden bg-gray-50">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
""",
    "frontend/src/components/dashboard/KPICharts.tsx": """'use client';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

const data = [
  { name: 'Jan', revenue: 4000, leads: 2400 },
  { name: 'Feb', revenue: 3000, leads: 1398 },
  { name: 'Mar', revenue: 2000, leads: 9800 },
  { name: 'Apr', revenue: 2780, leads: 3908 },
  { name: 'May', revenue: 1890, leads: 4800 },
  { name: 'Jun', revenue: 2390, leads: 3800 },
];

export function RevenueTrend() {
  return (
    <div className="h-64 w-full bg-white p-4 shadow rounded-lg">
      <h3 className="mb-4 font-semibold text-gray-700">Revenue Trend</h3>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="revenue" stroke="#2563eb" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export function LeadFunnel() {
  return (
    <div className="h-64 w-full bg-white p-4 shadow rounded-lg">
      <h3 className="mb-4 font-semibold text-gray-700">Lead Generation</h3>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="leads" fill="#16a34a" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
""",
    "frontend/src/app/(dashboard)/dashboard/page.tsx": """import { RevenueTrend, LeadFunnel } from '@/components/dashboard/KPICharts';

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Executive Dashboard</h1>
      
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
        <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Business Health</h3>
          <p className="mt-2 text-3xl font-semibold text-green-600">Excellent</p>
        </div>
        <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Growth Score</h3>
          <p className="mt-2 text-3xl font-semibold text-blue-600">84/100</p>
        </div>
        <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Revenue Opportunity</h3>
          <p className="mt-2 text-3xl font-semibold text-gray-900">$124,500</p>
        </div>
        <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-100">
          <h3 className="text-sm font-medium text-gray-500">Risk Alerts</h3>
          <p className="mt-2 text-3xl font-semibold text-red-600">2 Warnings</p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <RevenueTrend />
        <LeadFunnel />
      </div>

      <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-100">
        <h2 className="mb-4 text-xl font-bold">AI Executive Summary</h2>
        <p className="text-gray-600">
          TODO: This panel will display the final output from the CEO Agent, summarizing the findings from Marketing, Finance, and Operations regarding current campaigns.
        </p>
      </div>
    </div>
  );
}
"""
}

# Ensure directories exist
os.makedirs(os.path.join(root_dir, "backend/alembic/versions"), exist_ok=True)
os.makedirs(os.path.join(root_dir, "backend/app/api/v1"), exist_ok=True)
os.makedirs(os.path.join(root_dir, "backend/app/services"), exist_ok=True)
os.makedirs(os.path.join(root_dir, "backend/app/repositories"), exist_ok=True)
os.makedirs(os.path.join(root_dir, "frontend/src/components/layout"), exist_ok=True)
os.makedirs(os.path.join(root_dir, "frontend/src/components/dashboard"), exist_ok=True)
os.makedirs(os.path.join(root_dir, "frontend/src/app/(dashboard)/dashboard"), exist_ok=True)

# Write files
for path, content in files.items():
    file_path = os.path.join(root_dir, path)
    with open(file_path, "w") as f:
        f.write(content)

print("Phase 3 components generated successfully.")
