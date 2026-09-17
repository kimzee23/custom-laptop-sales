import uuid
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.core.config import settings
from app.core.database import async_engine, Base, AsyncSessionLocal
from app.seed_data import seed_database
from app.modules.health.router import router as health_router
from app.modules.products.router import router as products_router
from app.modules.configurations.router import router as configurations_router
from app.modules.payments.router import router as payments_router
from app.modules.orders.router import router as orders_router
from app.modules.cart.router import router as cart_router
from app.modules.artwork.router import router as artwork_router
from app.modules.reviews.router import router as reviews_router
from app.modules.admin.router import router as admin_router
from app.modules.auth.router import router as auth_router
from app.modules.analytics.router import router as analytics_router
from fastapi.staticfiles import StaticFiles
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB schemas & seed data
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        async with AsyncSessionLocal() as session:
            await seed_database(session)
    except Exception as e:
        print(f"Database initialization warning (will use in-memory seed if needed): {e}")
    
    yield
    
    await async_engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="High-performance backend API for the Custom Laptop E-Commerce Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Mount Static Files for Uploads & Artwork
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
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

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "An unexpected internal server error occurred.",
            "code": "INTERNAL_SERVER_ERROR",
            "detail": str(exc) if settings.DEBUG else None
        }
    )

# Mount API Routers
app.include_router(health_router, prefix=settings.API_V1_STR)
app.include_router(products_router, prefix=settings.API_V1_STR)
app.include_router(configurations_router, prefix=settings.API_V1_STR)
app.include_router(cart_router, prefix=settings.API_V1_STR)
app.include_router(orders_router, prefix=settings.API_V1_STR)
app.include_router(payments_router, prefix=settings.API_V1_STR)
app.include_router(artwork_router, prefix=settings.API_V1_STR)
app.include_router(reviews_router, prefix=settings.API_V1_STR)
app.include_router(admin_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(analytics_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "api_v1": settings.API_V1_STR
    }
