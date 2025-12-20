from pydantic import BaseModel, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


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


class ObjectStore(BaseModel):
    incoming: str
    processed: str

    @computed_field
    @property
    def bucket_names(self) -> set[str]:
        return {self.incoming, self.processed}


class Minio(BaseModel):
    admin_user: str
    admin_password: str
    port: str
    scheme: str = "http"

    @computed_field
    @property
    def endpoint(self) -> str:
        return f"{self.scheme}://minio:{self.port}"


class Settings(BaseSettings):
    database: Database
    message_broker: MessageBroker
    minio: Minio
    fastapi_port: str
    object_store: ObjectStore

    model_config = SettingsConfigDict(
        env_file=[".env"], extra="ignore", env_nested_delimiter="__"
    )


settings = Settings()
