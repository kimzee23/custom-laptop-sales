from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.domain.model.configuration import ConfigurationCategory, ConfigurationOption, SavedConfiguration
from src.application.ports.outbound.configuration_repository_port import ConfigurationRepositoryPort
from src.infrastructure.adapters.outbound.persistence.entities.models import (
    ConfigurationCategoryEntity, ConfigurationOptionEntity, SavedConfigurationEntity
)

class ConfigurationRepository(ConfigurationRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def list_categories_with_options(self) -> List[ConfigurationCategory]:
        stmt = select(ConfigurationCategoryEntity).options(
            selectinload(ConfigurationCategoryEntity.options)
        ).order_by(ConfigurationCategoryEntity.display_order)
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        return [
            ConfigurationCategory(
                id=c.id,
                code=c.code,
                name=c.name,
                display_order=c.display_order,
                is_required=c.is_required,
                options=[
                    ConfigurationOption(
                        id=opt.id,
                        category_id=opt.category_id,
                        code=opt.code,
                        name=opt.name,
                        price_modifier=opt.price_modifier,
                        stock=opt.stock,
                        is_active=opt.is_active,
                        display_order=opt.display_order,
                        metadata_json=opt.metadata_json or {}
                    )
                    for opt in sorted(c.options, key=lambda x: x.display_order)
                    if opt.is_active
                ]
            )
            for c in entities
        ]

    async def get_options_by_ids(self, option_ids: List[str]) -> List[ConfigurationOption]:
        if not option_ids:
            return []
        stmt = select(ConfigurationOptionEntity).where(ConfigurationOptionEntity.id.in_(option_ids))
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        return [
            ConfigurationOption(
                id=opt.id,
                category_id=opt.category_id,
                code=opt.code,
                name=opt.name,
                price_modifier=opt.price_modifier,
                stock=opt.stock,
                is_active=opt.is_active,
                display_order=opt.display_order,
                metadata_json=opt.metadata_json or {}
            )
            for opt in entities
        ]

    async def save_configuration(self, saved_config: SavedConfiguration) -> SavedConfiguration:
        entity = SavedConfigurationEntity(
            id=saved_config.id,
            user_id=saved_config.user_id,
            title=saved_config.title,
            product_id=saved_config.product_id,
            image_url=saved_config.image_url,
            total_price=saved_config.total_price,
            configuration_snapshot=saved_config.configuration_snapshot,
            specs_summary=saved_config.specs_summary,
            created_at=saved_config.created_at
        )
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return saved_config

    async def get_saved_configurations_by_user(self, user_id: Optional[str] = None) -> List[SavedConfiguration]:
        stmt = select(SavedConfigurationEntity)
        if user_id:
            stmt = stmt.where(SavedConfigurationEntity.user_id == user_id)
        stmt = stmt.order_by(SavedConfigurationEntity.created_at.desc())
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        return [
            SavedConfiguration(
                id=e.id,
                user_id=e.user_id,
                title=e.title,
                product_id=e.product_id,
                image_url=e.image_url,
                total_price=e.total_price,
                configuration_snapshot=e.configuration_snapshot or {},
                specs_summary=e.specs_summary or {},
                created_at=e.created_at
            )
            for e in entities
        ]

    async def add_configuration_option(self, option: ConfigurationOption) -> ConfigurationOption:
        entity = ConfigurationOptionEntity(
            id=option.id,
            category_id=option.category_id,
            code=option.code,
            name=option.name,
            price_modifier=option.price_modifier,
            stock=option.stock,
            is_active=option.is_active,
            display_order=option.display_order,
            metadata_json=option.metadata_json
        )
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return option
