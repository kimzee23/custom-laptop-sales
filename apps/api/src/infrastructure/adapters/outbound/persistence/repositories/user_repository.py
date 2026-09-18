from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.domain.model.user import User, Address
from src.application.ports.outbound.user_repository_port import UserRepositoryPort
from src.infrastructure.adapters.outbound.persistence.entities.models import UserEntity, AddressEntity

class UserRepository(UserRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_domain(self, entity: UserEntity) -> User:
        addresses = []
        if "addresses" in entity.__dict__:
            addresses = [
                Address(
                    id=addr.id,
                    user_id=addr.user_id,
                    title=addr.title,
                    full_name=addr.full_name,
                    phone=addr.phone,
                    street=addr.street,
                    city=addr.city,
                    state=addr.state,
                    country=addr.country,
                    is_default=addr.is_default,
                    created_at=addr.created_at
                )
                for addr in entity.addresses
            ]
        return User(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            hashed_password=entity.hashed_password,
            phone=entity.phone,
            avatar_url=entity.avatar_url,
            role=entity.role,
            reward_points=entity.reward_points,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            addresses=addresses
        )

    async def get_by_id(self, user_id: str) -> Optional[User]:
        stmt = select(UserEntity).where(UserEntity.id == user_id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        return self._to_domain(entity) if entity else None

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserEntity).where(UserEntity.email == email)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        return self._to_domain(entity) if entity else None

    async def save(self, user: User) -> User:
        stmt = select(UserEntity).where(UserEntity.id == user.id)
        res = await self.session.execute(stmt)
        entity = res.scalar_one_or_none()
        if not entity:
            entity = UserEntity(
                id=user.id,
                name=user.name,
                email=user.email,
                hashed_password=user.hashed_password,
                phone=user.phone,
                avatar_url=user.avatar_url,
                role=user.role,
                reward_points=user.reward_points,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            self.session.add(entity)
        else:
            entity.name = user.name
            entity.email = user.email
            entity.hashed_password = user.hashed_password
            entity.phone = user.phone
            entity.avatar_url = user.avatar_url
            entity.role = user.role
            entity.reward_points = user.reward_points
            entity.updated_at = user.updated_at

        await self.session.commit()
        await self.session.refresh(entity)
        return self._to_domain(entity)

    async def list_users(self, skip: int = 0, limit: int = 50) -> List[User]:
        stmt = select(UserEntity).offset(skip).limit(limit)
        res = await self.session.execute(stmt)
        entities = res.scalars().all()
        return [self._to_domain(e) for e in entities]
