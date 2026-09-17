from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import Category, Brand, Product, ConfigurationCategory, ConfigurationOption, Review, Promotion, User
from app.core.security import hash_password

CATEGORIES_DATA = [
    {
        "id": "cat-gaming",
        "name": "Gaming Laptops",
        "slug": "gaming-laptops",
        "description": "High-refresh screens, dedicated RTX GPUs, and extreme cooling.",
        "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=600&q=80",
        "icon": "Gamepad2",
        "display_order": 1
    },
    {
        "id": "cat-professional",
        "name": "Professional Laptops",
        "slug": "professional-laptops",
        "description": "Color-accurate OLED screens, long battery life, workstation power.",
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=600&q=80",
        "icon": "Briefcase",
        "display_order": 2
    },
    {
        "id": "cat-student",
        "name": "Student Laptops",
        "slug": "student-laptops",
        "description": "Lightweight, reliable, all-day battery life at budget-friendly prices.",
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=600&q=80",
        "icon": "GraduationCap",
        "display_order": 3
    },
    {
        "id": "cat-everyday",
        "name": "Everyday Laptops",
        "slug": "everyday-laptops",
        "description": "Sleek, responsive laptops for home browsing, movies, and daily tasks.",
        "image_url": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=600&q=80",
        "icon": "Laptop",
        "display_order": 4
    },
    {
        "id": "cat-macbooks",
        "name": "MacBooks & Ultrabooks",
        "slug": "macbooks-ultrabooks",
        "description": "Ultra-thin aluminium unibody laptops with incredible efficiency.",
        "image_url": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=600&q=80",
        "icon": "Sparkles",
        "display_order": 5
    },
    {
        "id": "cat-accessories",
        "name": "Laptop Accessories",
        "slug": "accessories",
        "description": "Sleeves, cooling pads, docks, high-speed chargers, and wireless mice.",
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=600&q=80",
        "icon": "Headphones",
        "display_order": 6
    }
]

BRANDS_DATA = [
    {"id": "brand-titanforge", "name": "TitanForge", "slug": "titanforge", "logo_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=120&q=80"},
    {"id": "brand-aerocraft", "name": "AeroCraft", "slug": "aerocraft", "logo_url": "https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=120&q=80"},
    {"id": "brand-zenith", "name": "Zenith", "slug": "zenith", "logo_url": "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?auto=format&fit=crop&w=120&q=80"},
    {"id": "brand-novablade", "name": "NovaBlade", "slug": "novablade", "logo_url": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=120&q=80"}
]

CONFIGURATION_CATEGORIES_DATA = [
    {
        "id": "cfg-color",
        "code": "color",
        "name": "Chassis Finish & Color",
        "display_order": 1,
        "is_required": True,
        "options": [
            {"id": "opt-color-arctic", "code": "arctic-blue", "name": "Arctic Blue (Metallic)", "price_modifier": 20000, "display_order": 1, "metadata_json": {"hex": "#1769FF", "badge": "Popular"}},
            {"id": "opt-color-cloud", "code": "cloud-white", "name": "Cloud White (Ceramic Finish)", "price_modifier": 15000, "display_order": 2, "metadata_json": {"hex": "#FFFFFF", "badge": "New"}},
            {"id": "opt-color-silver", "code": "pure-silver", "name": "Pure Silver (Anodized)", "price_modifier": 0, "display_order": 3, "metadata_json": {"hex": "#DCE6F5", "badge": "Standard"}},
            {"id": "opt-color-midnight", "code": "midnight-navy", "name": "Midnight Navy (Deep Matte)", "price_modifier": 25000, "display_order": 4, "metadata_json": {"hex": "#0B1F3A", "badge": "Premium"}},
            {"id": "opt-color-crimson", "code": "crimson-red", "name": "Cyber Crimson (Stealth)", "price_modifier": 30000, "display_order": 5, "metadata_json": {"hex": "#D92D20", "badge": "Special"}}
        ]
    },
    {
        "id": "cfg-ram",
        "code": "ram",
        "name": "System Memory (RAM)",
        "display_order": 2,
        "is_required": True,
        "options": [
            {"id": "opt-ram-16", "code": "16gb-ddr5", "name": "16GB DDR5 5600MHz (Dual Channel)", "price_modifier": 0, "display_order": 1, "metadata_json": {"speed": "5600MHz", "default": True}},
            {"id": "opt-ram-32", "code": "32gb-ddr5", "name": "32GB DDR5 5600MHz (High Performance)", "price_modifier": 90000, "display_order": 2, "metadata_json": {"speed": "5600MHz", "recommended": True}},
            {"id": "opt-ram-64", "code": "64gb-ddr5", "name": "64GB DDR5 6000MHz (Workstation Ready)", "price_modifier": 210000, "display_order": 3, "metadata_json": {"speed": "6000MHz"}}
        ]
    },
    {
        "id": "cfg-storage",
        "code": "storage",
        "name": "Solid State Drive (Storage)",
        "display_order": 3,
        "is_required": True,
        "options": [
            {"id": "opt-ssd-1tb", "code": "1tb-nvme", "name": "1TB PCIe 4.0 NVMe M.2 SSD (5000MB/s)", "price_modifier": 0, "display_order": 1, "metadata_json": {"default": True}},
            {"id": "opt-ssd-2tb", "code": "2tb-nvme", "name": "2TB PCIe 4.0 NVMe M.2 SSD (7400MB/s Pro)", "price_modifier": 130000, "display_order": 2, "metadata_json": {"recommended": True}},
            {"id": "opt-ssd-4tb", "code": "4tb-nvme", "name": "4TB (Dual 2TB Raid 0 Extreme NVMe)", "price_modifier": 280000, "display_order": 3, "metadata_json": {}}
        ]
    },
    {
        "id": "cfg-gpu",
        "code": "gpu",
        "name": "Graphics Processor (GPU)",
        "display_order": 4,
        "is_required": False,
        "options": [
            {"id": "opt-gpu-rtx4060", "code": "rtx-4060", "name": "NVIDIA GeForce RTX 4060 8GB GDDR6 (140W TGP)", "price_modifier": 0, "display_order": 1, "metadata_json": {"default": True}},
            {"id": "opt-gpu-rtx4070", "code": "rtx-4070", "name": "NVIDIA GeForce RTX 4070 8GB GDDR6 (AI Boost)", "price_modifier": 320000, "display_order": 2, "metadata_json": {"recommended": True}},
            {"id": "opt-gpu-rtx4080", "code": "rtx-4080", "name": "NVIDIA GeForce RTX 4080 12GB GDDR6X (Studio Max)", "price_modifier": 680000, "display_order": 3, "metadata_json": {}}
        ]
    },
    {
        "id": "cfg-display",
        "code": "display",
        "name": "Display Panel",
        "display_order": 5,
        "is_required": False,
        "options": [
            {"id": "opt-disp-ips", "code": "qhd-165hz", "name": "16\" QHD+ (2560x1600) 165Hz IPS 100% sRGB", "price_modifier": 0, "display_order": 1, "metadata_json": {"default": True}},
            {"id": "opt-disp-oled", "code": "4k-oled-120hz", "name": "16\" 3.2K OLED 120Hz 100% DCI-P3 500 nits HDR", "price_modifier": 160000, "display_order": 2, "metadata_json": {"recommended": True}}
        ]
    },
    {
        "id": "cfg-keyboard",
        "code": "keyboard",
        "name": "Keyboard & Trackpad",
        "display_order": 6,
        "is_required": False,
        "options": [
            {"id": "opt-kb-backlit", "code": "white-backlit", "name": "Clean White Backlit Island Keyboard", "price_modifier": 0, "display_order": 1, "metadata_json": {"default": True}},
            {"id": "opt-kb-rgb", "code": "per-key-rgb", "name": "Per-Key RGB Mechanical Switch Keyboard", "price_modifier": 45000, "display_order": 2, "metadata_json": {}}
        ]
    },
    {
        "id": "cfg-artwork",
        "code": "artwork",
        "name": "Custom Lid Artwork & Laser Engraving",
        "display_order": 7,
        "is_required": False,
        "options": [
            {"id": "opt-art-none", "code": "no-artwork", "name": "Standard Clean Chassis (No Artwork)", "price_modifier": 0, "display_order": 1, "metadata_json": {"default": True}},
            {"id": "opt-art-custom", "code": "custom-artwork-uv", "name": "Custom Precision UV Print / Artwork Engraving", "price_modifier": 35000, "display_order": 2, "metadata_json": {"has_uploader": True}}
        ]
    }
]

PRODUCTS_DATA = [
    {
        "id": "prod-titanforge-predator-16",
        "title": "TitanForge Predator 16 Pro Gaming Laptop",
        "slug": "titanforge-predator-16-pro",
        "description": "Crafted for intense esports and compute workloads. Features state-of-the-art dual liquid-metal cooling, customizable per-key lighting, and modular upgrade bays.",
        "short_description": "Intel Core i9 14th Gen, RTX 4070/4080, 240Hz QHD+ Display",
        "category_id": "cat-gaming",
        "brand_id": "brand-titanforge",
        "base_price": 1450000.0,
        "original_price": 1680000.0,
        "discount_percentage": 14,
        "is_featured": True,
        "is_flash_deal": True,
        "is_best_seller": True,
        "is_customizable": True,
        "stock": 18,
        "rating": 4.9,
        "review_count": 48,
        "image_url": "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1541807084-5c52b6b3adef?auto=format&fit=crop&w=800&q=80"
        ],
        "specs": {
            "processor": "Intel Core i9-14900HX (24 Cores, up to 5.8GHz)",
            "ram": "32GB DDR5 5600MHz",
            "storage": "1TB Gen4 NVMe SSD",
            "gpu": "NVIDIA GeForce RTX 4070 8GB GDDR6",
            "display": "16.0\" QHD+ (2560x1600) 240Hz 500-nit",
            "battery": "99.9Wh (Fast Charge 50% in 30min)",
            "weight": "2.25 kg"
        }
    },
    {
        "id": "prod-aerocraft-studiomaster-16",
        "title": "AeroCraft StudioMaster 16 OLED Creator Laptop",
        "slug": "aerocraft-studiomaster-16-oled",
        "description": "Engineered for designers, video editors, and 3D animators. Factory color-calibrated Delta E < 1 OLED display with 100% DCI-P3 gamut and CNC aluminium unibody.",
        "short_description": "AMD Ryzen 9 7945HX, RTX 4060/4070, 3.2K 120Hz OLED",
        "category_id": "cat-professional",
        "brand_id": "brand-aerocraft",
        "base_price": 1280000.0,
        "original_price": 1420000.0,
        "discount_percentage": 10,
        "is_featured": True,
        "is_flash_deal": False,
        "is_best_seller": True,
        "is_customizable": True,
        "stock": 14,
        "rating": 4.8,
        "review_count": 36,
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80"
        ],
        "specs": {
            "processor": "AMD Ryzen 9 7945HX (16 Cores, 32 Threads)",
            "ram": "32GB DDR5 Dual Channel",
            "storage": "1TB Pro PCIe 4.0 SSD",
            "gpu": "NVIDIA GeForce RTX 4060 Studio Edition",
            "display": "16.0\" 3.2K OLED 120Hz 100% DCI-P3",
            "battery": "90Wh (11 Hours battery)",
            "weight": "1.89 kg"
        }
    },
    {
        "id": "prod-zenith-campusbook-14",
        "title": "Zenith CampusBook Slim 14 Student Edition",
        "slug": "zenith-campusbook-slim-14",
        "description": "Ultraportable featherweight laptop designed for students and mobile professionals. Features silent fanless mode, spill-resistant keyboard, and fast USB-C PD charging.",
        "short_description": "Intel Core i5 13th Gen, 16GB RAM, 512GB NVMe SSD, 14\" FHD+",
        "category_id": "cat-student",
        "brand_id": "brand-zenith",
        "base_price": 540000.0,
        "original_price": 620000.0,
        "discount_percentage": 13,
        "is_featured": True,
        "is_flash_deal": True,
        "is_best_seller": False,
        "is_customizable": True,
        "stock": 25,
        "rating": 4.7,
        "review_count": 62,
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=800&q=80"
        ],
        "specs": {
            "processor": "Intel Core i5-13420H (10 Cores, up to 4.6GHz)",
            "ram": "16GB LPDDR5",
            "storage": "512GB PCIe NVMe SSD",
            "gpu": "Intel Iris Xe Graphics",
            "display": "14.0\" FHD+ (1920x1200) IPS Anti-Glare",
            "battery": "65Wh (14 Hours runtime)",
            "weight": "1.32 kg"
        }
    },
    {
        "id": "prod-aerocraft-real-air-15",
        "title": "AeroCraft Real Air 15 Unibody Ultrabook",
        "slug": "aerocraft-real-air-15",
        "description": "Aerospace-grade aluminium chassis with edge-to-edge Liquid Retina style display, force-touch haptic trackpad, and quad spatial audio speakers.",
        "short_description": "Next-Gen ARM / Intel Ultra 7, 32GB RAM, 1TB SSD, 18hr Battery",
        "category_id": "cat-macbooks",
        "brand_id": "brand-aerocraft",
        "base_price": 980000.0,
        "original_price": 1150000.0,
        "discount_percentage": 15,
        "is_featured": True,
        "is_flash_deal": False,
        "is_best_seller": True,
        "is_customizable": True,
        "stock": 19,
        "rating": 4.9,
        "review_count": 89,
        "image_url": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=800&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=800&q=80"
        ],
        "specs": {
            "processor": "Intel Core Ultra 7 155H with NPU AI Engine",
            "ram": "32GB LPDDR5X 7467MHz",
            "storage": "1TB Gen4 SSD",
            "gpu": "Intel Arc Graphics 8-Cores",
            "display": "15.3\" 2.8K 120Hz Liquid IPS 500 nits",
            "battery": "72Wh (18 Hours runtime)",
            "weight": "1.49 kg"
        }
    },
    {
        "id": "prod-novablade-fusion-15",
        "title": "NovaBlade Fusion 15 Everyday Workhorse",
        "slug": "novablade-fusion-15",
        "description": "The perfect balance of power, durability, and daily comfort. Ergonomic soft-touch deck, full numeric keypad, and comprehensive legacy and USB4 ports.",
        "short_description": "AMD Ryzen 7 7730U, 16GB RAM, 1TB SSD, 15.6\" IPS Display",
        "category_id": "cat-everyday",
        "brand_id": "brand-novablade",
        "base_price": 620000.0,
        "original_price": 700000.0,
        "discount_percentage": 11,
        "is_featured": False,
        "is_flash_deal": True,
        "is_best_seller": False,
        "is_customizable": True,
        "stock": 30,
        "rating": 4.6,
        "review_count": 27,
        "image_url": "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=800&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1525547719571-a2d4ac8945e2?auto=format&fit=crop&w=800&q=80"
        ],
        "specs": {
            "processor": "AMD Ryzen 7 7730U (8 Cores, 16 Threads)",
            "ram": "16GB DDR4 3200MHz",
            "storage": "1TB NVMe SSD",
            "gpu": "AMD Radeon Graphics",
            "display": "15.6\" FHD (1920x1080) IPS Anti-Glare",
            "battery": "54Wh (9 Hours runtime)",
            "weight": "1.75 kg"
        }
    },
    {
        "id": "prod-acc-dock-thunderbolt",
        "title": "AeroCraft 14-in-1 Dual 4K Thunderbolt Dock",
        "slug": "aerocraft-thunderbolt-dock",
        "description": "Single-cable power and display connectivity. Supports dual 4K 60Hz displays, 100W Power Delivery charging, Gigabit Ethernet, SD 4.0 card reader, and 4x USB 3.2 ports.",
        "short_description": "100W PD charging, Dual 4K 60Hz DisplayPort/HDMI, Gigabit LAN",
        "category_id": "cat-accessories",
        "brand_id": "brand-aerocraft",
        "base_price": 145000.0,
        "original_price": 180000.0,
        "discount_percentage": 19,
        "is_featured": True,
        "is_flash_deal": False,
        "is_best_seller": True,
        "is_customizable": False,
        "stock": 50,
        "rating": 4.9,
        "review_count": 74,
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=800&q=80",
        "gallery_images": [
            "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=800&q=80"
        ],
        "specs": {
            "ports": "2x HDMI 2.1, 1x DP 1.4, 4x USB-A, 2x USB-C, RJ45",
            "power": "100W Host PD Pass-through",
            "material": "Anodized Space Gray Aluminium"
        }
    }
]

PROMOTIONS_DATA = [
    {
        "id": "promo-techfest-2026",
        "title": "RealTech Cyberfest Launch 50K Off",
        "code": "CYBERBUILD50K",
        "description": "Get ₦50,000 instant discount on custom configured gaming and creator laptops.",
        "discount_type": "fixed",
        "discount_value": 50000.0,
        "banner_url": "https://images.unsplash.com/photo-1550745165-9bc0b252726f?auto=format&fit=crop&w=1200&q=80",
        "is_active": True
    },
    {
        "id": "promo-student-verified",
        "title": "Student & Academic Discount",
        "code": "STUDENT10",
        "description": "Verified university students and researchers receive 10% off portable workstations.",
        "discount_type": "percentage",
        "discount_value": 10.0,
        "banner_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=1200&q=80",
        "is_active": True
    },
    {
        "id": "promo-free-laser-engrave",
        "title": "Complimentary Custom UV & Laser Engraving",
        "code": "FREECUSTOM",
        "description": "Upload your custom logo or initials for free precision lid engraving with code FREECUSTOM.",
        "discount_type": "fixed",
        "discount_value": 35000.0,
        "banner_url": "https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?auto=format&fit=crop&w=1200&q=80",
        "is_active": True
    }
]

async def seed_database(db: AsyncSession):
    # Check if already seeded
    existing_cats = await db.execute(select(Category))
    if existing_cats.scalars().first():
        # Check if promotions seeded
        existing_promos = await db.execute(select(Promotion))
        if not existing_promos.scalars().first():
            for p in PROMOTIONS_DATA:
                db.add(Promotion(**p))
            await db.commit()

        # Check if admin user seeded
        existing_admin = await db.execute(select(User).where(User.email == "admin@realtech.ng"))
        if not existing_admin.scalars().first():
            db.add(User(
                id="usr-admin-001",
                name="System Administrator",
                email="admin@realtech.ng",
                hashed_password=hash_password("AdminPass123!"),
                phone="+234 800 000 0001",
                role="admin",
                reward_points=10000
            ))
            db.add(User(
                id="usr-customer-001",
                name="Amina Bello",
                email="customer@realtech.ng",
                hashed_password=hash_password("CustomerPass123!"),
                phone="+234 803 123 4567",
                role="customer",
                reward_points=1200
            ))
            await db.commit()
        return

    # Seed Categories
    for cat_data in CATEGORIES_DATA:
        db.add(Category(**cat_data))

    # Seed Brands
    for brand_data in BRANDS_DATA:
        db.add(Brand(**brand_data))

    # Seed Configuration Categories & Options
    for cfg_cat_data in CONFIGURATION_CATEGORIES_DATA:
        options_data = cfg_cat_data.get("options", [])
        cfg_cat = ConfigurationCategory(
            id=cfg_cat_data["id"],
            code=cfg_cat_data["code"],
            name=cfg_cat_data["name"],
            display_order=cfg_cat_data["display_order"],
            is_required=cfg_cat_data["is_required"]
        )
        db.add(cfg_cat)
        for opt_data in options_data:
            opt = ConfigurationOption(
                id=opt_data["id"],
                category_id=cfg_cat.id,
                code=opt_data["code"],
                name=opt_data["name"],
                price_modifier=opt_data["price_modifier"],
                display_order=opt_data["display_order"],
                metadata_json=opt_data.get("metadata_json", {})
            )
            db.add(opt)

    # Seed Products
    for prod_data in PRODUCTS_DATA:
        db.add(Product(**prod_data))

    # Seed Promotions
    for promo_data in PROMOTIONS_DATA:
        db.add(Promotion(**promo_data))

    # Seed Default Users
    db.add(User(
        id="usr-admin-001",
        name="System Administrator",
        email="admin@realtech.ng",
        hashed_password=hash_password("AdminPass123!"),
        phone="+234 800 000 0001",
        role="admin",
        reward_points=10000
    ))
    db.add(User(
        id="usr-customer-001",
        name="Amina Bello",
        email="customer@realtech.ng",
        hashed_password=hash_password("CustomerPass123!"),
        phone="+234 803 123 4567",
        role="customer",
        reward_points=1200
    ))

    await db.commit()
