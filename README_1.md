# Synexa Growth OS

**An AI Business Growth Operating System**

Built by **Team ROBOVANTA** for a 24-hour AI Hackathon.

---

## What This Is

Synexa Growth OS is not a CRM and not a chatbot. It's an AI-powered executive layer for small and medium businesses: a set of collaborating AI agents that analyze a business, generate growth strategy, and surface prioritized recommendations — the way an internal leadership team would, rather than a dashboard that just visualizes data.

## The Problem

SMBs have data but not decision-making capacity. CRMs store customer records. BI tools render charts. Chatbots answer isolated questions. None of them reason across departments (marketing, sales, finance, operations) to produce a single prioritized action plan. Business owners are left to do that synthesis manually.

## The Solution

The user submits business information. Synexa builds a structured **Business Context** from it, routes that context to specialized AI agents, and each agent returns a department-level recommendation. A **Decision Engine** then reconciles conflicting recommendations (e.g., Marketing wants to increase ad spend, Finance flags budget risk, Ops flags capacity limits) into one ranked, explainable action plan, surfaced on a business health dashboard.

## Built in This Hackathon (MVP Scope)

To keep the demo reliable within a 24-hour build window, this MVP implements a deliberately focused slice of the full vision:

- **Business Context Builder** — structured intake of business profile, goals, and current KPIs into a single context object used by every agent
- **3 specialized agents** — Marketing, Sales, Finance (Operations/Customer Success are roadmap items, see below)
- **Decision Engine (rules-based)** — each agent returns a recommendation with a confidence score and resource requirement; conflicts are flagged against explicit thresholds (e.g., requested spend vs. available budget) rather than an opaque LLM arbiter. This keeps the reasoning inspectable and demoable on stage.
- **Business Health Dashboard** — growth score, revenue opportunity, and risk alerts rendered from agent output
- **Seeded historical data** — a small set of past KPIs and recommendations pre-loaded into the database so the "recommendations consider history" mechanism can be shown working, rather than claiming live-learning that a 12-hour build can't actually demonstrate

## Roadmap (Post-Hackathon / Full Vision)

These are explicitly **not** implemented in the hackathon build and are called out here for transparency with judges:

- Operations Agent and Customer Success Agent
- ChromaDB-backed knowledge retrieval over uploaded business documents
- CrewAI-orchestrated multi-agent collaboration (hackathon build uses direct, independently-invoked agent calls for reliability and latency)
- LLM-based confidence scoring and conflict resolution in the Decision Engine
- True closed-loop learning from real (not seeded) outcome data over time

## Architecture

```
User
  ↓
Next.js Frontend
  ↓
FastAPI Backend
  ↓
Business Context Builder
  ↓
Specialized Agents (Marketing / Sales / Finance)
  ↓
Decision Engine (rules-based scoring + conflict flags)
  ↓
Supabase (PostgreSQL)
  ↓
Dashboard
```

Frontend never talks to the AI layer directly — all agent calls are proxied through the backend to keep AI logic decoupled from business logic and to control cost/rate-limiting centrally.

## Tech Stack

**Frontend:** Next.js 15, React 19, TypeScript, Tailwind CSS, shadcn/ui, Recharts, TanStack Query, Zustand
**Backend:** FastAPI, Python, Pydantic, SQLAlchemy
**AI:** Google Gemini API
**Database:** Supabase (PostgreSQL)
**Deployment:** Vercel (frontend), Render (backend)

## Team

**Team ROBOVANTA** — 2026

## Getting Started

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

Environment variables required — see `.env.example` in each directory.
