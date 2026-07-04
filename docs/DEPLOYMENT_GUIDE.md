# Deployment Guide

## 1. Backend (Render)
- Connect repository to Render.
- Set Build Command: `pip install -r backend/requirements.txt`
- Set Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment Variables required: `DATABASE_URL`, `SUPABASE_JWT_SECRET`, `GOOGLE_API_KEY`.

## 2. Frontend (Vercel)
- Connect repository to Vercel.
- Framework Preset: Next.js
- Root Directory: `frontend`
- Environment Variables required: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`, `NEXT_PUBLIC_API_URL`.

## 3. Database (Supabase)
- Run Alembic migrations locally with the `DATABASE_URL` pointing to your Supabase Postgres instance.
`cd backend && alembic upgrade head`
