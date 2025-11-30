from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, computed_field, SecretStr


class Database(BaseModel):
    host: str
    port: str
    name: str
    user: str
    password: SecretStr

    @computed_field
    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"


class MessageBroker(BaseModel):
    user: str
    password: str


class Minio(BaseModel):
    admin_user: str
    admin_password: str
    port: str


class Settings(BaseSettings):
    database: Database
    message_broker: MessageBroker
    minio: Minio
    fastapi_port: str

    model_config = SettingsConfigDict(
        env_file=[".env"], extra="ignore", env_nested_delimiter="__"
    )


settings = Settings()
