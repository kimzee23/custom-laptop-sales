from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from src.domain.model.configuration import ConfigurationCategory, ConfigurationOption, SavedConfiguration

class ConfigurationRepositoryPort(ABC):
    @abstractmethod
    async def list_categories_with_options(self) -> List[ConfigurationCategory]:
        pass

    @abstractmethod
    async def get_options_by_ids(self, option_ids: List[str]) -> List[ConfigurationOption]:
        pass

    @abstractmethod
    async def save_configuration(self, saved_config: SavedConfiguration) -> SavedConfiguration:
        pass

    @abstractmethod
    async def get_saved_configurations_by_user(self, user_id: str) -> List[SavedConfiguration]:
        pass

    @abstractmethod
    async def add_configuration_option(self, option: ConfigurationOption) -> ConfigurationOption:
        pass
