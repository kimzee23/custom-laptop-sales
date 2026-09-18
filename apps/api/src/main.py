import os
import uuid
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.infrastructure.config.settings import settings
from src.infrastructure.adapters.outbound.persistence.database import async_engine, Base, AsyncSessionLocal
from src.domain.exception.base import DomainException
from src.infrastructure.adapters.inbound.rest.exception_handlers import (
    domain_exception_handler, http_exception_handler, global_exception_handler
)

# Inbound Driving REST Controllers
from src.infrastructure.adapters.inbound.rest.controllers.auth_controller import router as auth_router
from src.infrastructure.adapters.inbound.rest.controllers.product_controller import router as product_router
from src.infrastructure.adapters.inbound.rest.controllers.configuration_controller import router as config_router
from src.infrastructure.adapters.inbound.rest.controllers.cart_controller import router as cart_router
from src.infrastructure.adapters.inbound.rest.controllers.order_controller import router as order_router
from src.infrastructure.adapters.inbound.rest.controllers.payment_controller import router as payment_router
from src.infrastructure.adapters.inbound.rest.controllers.artwork_controller import router as artwork_router
from src.infrastructure.adapters.inbound.rest.controllers.review_controller import router as review_router
from src.infrastructure.adapters.inbound.rest.controllers.analytics_controller import router as analytics_router
from src.infrastructure.adapters.inbound.rest.controllers.admin_controller import router as admin_router
from src.infrastructure.adapters.inbound.rest.controllers.health_controller import router as health_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schemas & seed database
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        from app.seed_data import seed_database
        async with AsyncSessionLocal() as session:
            await seed_database(session)
    except Exception as e:
        print(f"Database initialization note: {e}")

    yield

    await async_engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Hexagonal Architecture (Ports & Adapters) API for Custom Laptop Sales",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Mount Static Files for Uploads & Artwork
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if not os.path.exists(static_dir):
    static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "static")
os.makedirs(os.path.join(static_dir, "uploads", "artwork"), exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# CORS Setup
cors_origins = settings.cors_origins if hasattr(settings, "cors_origins") else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if "*" not in cors_origins else ["*"],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request ID & Timing Middleware
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response

# Exception Handlers
app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Mount API Driving Routers
app.include_router(health_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(product_router, prefix=settings.API_V1_STR)
app.include_router(config_router, prefix=settings.API_V1_STR)
app.include_router(cart_router, prefix=settings.API_V1_STR)
app.include_router(order_router, prefix=settings.API_V1_STR)
app.include_router(payment_router, prefix=settings.API_V1_STR)
app.include_router(artwork_router, prefix=settings.API_V1_STR)
app.include_router(review_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} (Hexagonal Architecture)",
        "version": settings.VERSION,
        "docs": "/docs",
        "api_v1": settings.API_V1_STR
    }
