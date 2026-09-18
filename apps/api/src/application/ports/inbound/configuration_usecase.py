from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from src.domain.model.configuration import ConfigurationCategory, SavedConfiguration

class ConfigurationUseCase(ABC):
    @abstractmethod
    async def get_configuration_categories(self, product_id: Optional[str] = None) -> List[ConfigurationCategory]:
        pass

    @abstractmethod
    async def calculate_price(self, base_price: float, selected_option_ids: List[str]) -> Dict[str, Any]:
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def get_saved_configurations(self, user_id: str) -> List[SavedConfiguration]:
        pass
