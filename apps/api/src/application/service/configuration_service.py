import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from src.domain.model.configuration import ConfigurationCategory, SavedConfiguration
from src.application.ports.inbound.configuration_usecase import ConfigurationUseCase
from src.application.ports.outbound.configuration_repository_port import ConfigurationRepositoryPort
from src.application.ports.outbound.product_repository_port import ProductRepositoryPort

class ConfigurationService(ConfigurationUseCase):
    def __init__(
        self,
        config_repository: ConfigurationRepositoryPort,
        product_repository: Optional[ProductRepositoryPort] = None
    ):
        self.config_repo = config_repository
        self.product_repo = product_repository

    async def get_configuration_categories(self, product_id: Optional[str] = None) -> List[ConfigurationCategory]:
        return await self.config_repo.list_categories_with_options()

    async def calculate_price(
        self,
        product_id: Optional[str] = None,
        base_price: Optional[float] = None,
        selected_option_ids: List[str] = None,
        artwork: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        selected_option_ids = selected_option_ids or []
        product_title = "Custom Laptop"
        calc_base_price = base_price or 1000000.0

        if product_id and self.product_repo:
            prod = await self.product_repo.get_by_id(product_id)
            if not prod:
                prod = await self.product_repo.get_by_slug(product_id)
            if prod:
                product_title = prod.title
                calc_base_price = prod.base_price

        options = await self.config_repo.get_options_by_ids([opt for opt in selected_option_ids if opt])
        breakdown_items = []
        modifiers_total = 0.0
        for opt in options:
            if opt.price_modifier != 0:
                breakdown_items.append({
                    "name": opt.name,
                    "category": opt.code,
                    "modifier": opt.price_modifier
                })
            modifiers_total += opt.price_modifier

        artwork_price = 0.0
        if artwork and (artwork.get("image_url") or artwork.get("custom_text")):
            artwork_price = 35000.0
            breakdown_items.append({
                "name": "Custom Precision UV Artwork / Text Engraving",
                "category": "Artwork",
                "modifier": artwork_price
            })

        subtotal = calc_base_price + modifiers_total + artwork_price
        shipping = 0.0
        discount = 0.0
        total = subtotal + shipping - discount

        return {
            "product_id": product_id,
            "product_title": product_title,
            "base_price": calc_base_price,
            "items": breakdown_items,
            "modifiers_total": modifiers_total,
            "subtotal": subtotal,
            "shipping": shipping,
            "discount": discount,
            "total": total,
            "total_price": total,
            "currency": "NGN",
            "currency_symbol": "₦"
        }

    async def save_user_configuration(
        self,
        user_id: str,
        title: str,
        product_id: str,
        image_url: Optional[str],
        total_price: float,
        configuration_snapshot: Dict[str, Any],
        specs_summary: Dict[str, Any]
    ) -> SavedConfiguration:
        saved_config = SavedConfiguration(
            id=str(uuid.uuid4()),
            user_id=user_id,
            title=title,
            product_id=product_id,
            image_url=image_url,
            total_price=total_price,
            configuration_snapshot=configuration_snapshot,
            specs_summary=specs_summary,
            created_at=datetime.now(timezone.utc)
        )
        return await self.config_repo.save_configuration(saved_config)

    async def get_saved_configurations(self, user_id: Optional[str] = None) -> List[SavedConfiguration]:
        return await self.config_repo.get_saved_configurations_by_user(user_id)
