import os
from pydantic_settings import BaseSettings, SettingsConfigDict, YamlConfigSettingsSource, PydanticBaseSettingsSource
from typing import Type, Tuple

class Settings(BaseSettings):
    # API Keys for local development
    gemini_api_key: str = "AIzaSyC0JpVze60XWsIYmnMZ1gdP4oZHFzeON7g"  # Your Gemini API key
    
    # Google Cloud settings (can be dummy values for local development)
    project_id: str
    location: str
    gemini_model_name: str
    embedding_model_name: str
    image_generation_model_name: str
    database: str
    collection: str
    test_collection: str
    top_k: int
    port: int = 8080
    
    # Local development mode
    local_mode: bool = True

    model_config = SettingsConfigDict(
        yaml_file="config_local.yaml", yaml_file_encoding="utf-8"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,  # First, try init_settings (from constructor)
            YamlConfigSettingsSource(settings_cls),  # Then, try YAML
            env_settings,  # Finally, try environment variables
        )
    
def get_settings() -> Settings:
    return Settings()
