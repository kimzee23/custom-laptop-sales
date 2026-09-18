# Compatibility Layer: Forwards to the Hexagonal Architecture application in src.main
from src.main import app, lifespan

__all__ = ["app", "lifespan"]
