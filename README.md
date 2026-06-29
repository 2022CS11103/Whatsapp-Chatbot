# Whatsapp-Chatbot
┌─────────────────────────────────────────────────────────────┐
│                      Clients                                 │
│  React Dashboard  │  WhatsApp (Meta Cloud API)  │  Admin UI  │
└───────────┬──────────────────┬─────────────────────┬────────┘
            │                  │                     │
            ▼                  ▼                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI (API Layer)                       │
│   Routers → Schemas (Pydantic v2) → Auth Middleware          │
└───────────┬───────────────────────────────────────────────────┘
            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer                             │
│  BusinessService, FAQService, KnowledgeBaseService,           │
│  ConversationService, AgentService, AnalyticsService          │
└───────────┬───────────────────────────────────┬───────────────┘
            ▼                                   ▼
┌──────────────────────────┐     ┌─────────────────────────────┐
│   Repository Layer        │     │   AI / Agent Layer           │
│  (SQLAlchemy, async)      │     │  LangGraph orchestration      │
│  - BusinessRepo            │     │  - RAG retriever (Qdrant)     │
│  - FAQRepo                  │     │  - Tool calling (booking,    │
│  - ConversationRepo          │     │    lead capture, handoff)   │
│  - LeadRepo                   │     │  - Provider adapter         │
└───────────┬────────────────┘     │    (OpenAI/Gemini/Claude)    │
            ▼                       │  - Guardrails + citation      │
┌──────────────────────────┐       │    enforcement                │
│  PostgreSQL (source of    │       └──────────┬────────────────────┘
│  truth) + Redis (cache,   │                  ▼
│  session memory, rate     │       ┌─────────────────────────────┐
│  limit) + Qdrant (vectors)│       │  Background Jobs (APScheduler│
└──────────────────────────┘       │  + Celery): doc ingestion,    │
                                    │  embedding, reminders, digests │
                                    └─────────────────────────────┘
