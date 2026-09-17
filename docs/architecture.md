# System Architecture

## Overview

The Custom Laptop E-Commerce Platform is architected as a **modular monolith** with a modern decoupled frontend.

```
┌─────────────────────────────────────────────────────────┐
│                    Next.js Storefront                   │
│   (Marketplace Shell, 3D Configurator, Zustand Stores)  │
└───────────────────────────┬─────────────────────────────┘
                            │ REST / JSON
┌───────────────────────────▼─────────────────────────────┐
│                    FastAPI Backend                      │
│ ┌──────────────┬──────────────────┬──────────────────┐  │
│ │   Products   │  Configurations  │   Cart & Orders  │  │
│ ├──────────────┼──────────────────┼──────────────────┤  │
│ │   Payments   │     Artwork      │    Inventory     │  │
│ └──────────────┴──────────────────┴──────────────────┘  │
└───────────────────────────┬─────────────────────────────┘
             ┌──────────────┴──────────────┐
             ▼                             ▼
    PostgreSQL Database              Redis Cache
```

## Core Principles
1. **Authoritative Backend Pricing**: The backend calculates all final prices based on base product price + option modifiers + artwork + shipping. Client prices are never trusted.
2. **Modular Configuration Engine**: Products are models with configurable dimensions (Color, RAM, Storage, CPU, GPU, Display, Keyboard, Artwork, Accessories).
3. **Optimized Storefront Performance**: Fast initial marketplace render; 3D viewer components lazy-loaded on demand.
