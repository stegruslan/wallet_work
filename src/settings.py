"""Файл, хранящий глобальные настройки проекта."""

from pydantic_settings import BaseSettings


class SettingsConf(BaseSettings):
    """Класс хранящий все настройки."""

    DB_DIALECT: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    class Config:
        """Конфиг настроек."""

        case_sensitive = True
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = SettingsConf()
