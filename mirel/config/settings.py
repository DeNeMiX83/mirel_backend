import os
from dataclasses import dataclass, field


@dataclass
class PostgresSettings:
    host: str = field(init=False)
    port: int = field(init=False)
    user: str = field(init=False)
    password: str = field(init=False)
    database: str = field(init=False)
    url: str = field(init=False)

    def __post_init__(self):
        self.host = os.getenv("POSTGRES_HOST")
        self.port = os.getenv("POSTGRES_PORT")
        self.user = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD")
        self.database = os.getenv("POSTGRES_DB")
        self.url = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(  # noqa E501
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )


@dataclass
class YandexDiskSettings:
    app_id: str = field(init=False)
    app_secret: str = field(init=False)
    token: str = field(init=False)
    folder: str = field(init=False)

    def __post_init__(self):
        self.app_id = os.getenv("YANDEX_APP_ID")
        self.app_secret = os.getenv("YANDEX_APP_SECRET")
        self.token = os.getenv("YANDEX_TOKEN")
        self.folder = os.getenv("YANDEX_FOLDER_FOR_SAVE")


@dataclass
class Settings:
    domain: str = field(init=False)
    host: str = field(init=False)
    port: int = field(init=False)
    root_path: str = field(init=False)

    docs_url: str = field(init=False)

    path_to_folder_for_save_image: str = field(init=False)

    link_to_image: str = field(init=False)

    postgres: PostgresSettings = field(
        init=False, default_factory=PostgresSettings  # noqa E501
    )
    yandex_disk: YandexDiskSettings = field(
        init=False, default_factory=YandexDiskSettings
    )

    def __post_init__(self):
        self.domain = os.getenv("DOMAIN")
        self.host = os.getenv("HOST")
        self.port = os.getenv("BACKEND_PORT")
        self.root_path = os.getenv("ROOT_PATH")
        self.api_url = os.getenv("API_URL")
        self.docs_url = os.getenv("DOCS_URL")
        self.path_to_folder_for_save_image = os.getenv(
            "PATH_TO_FOLDER_FOR_SAVE_IMAGE"
        )
        self.link_to_image = "{domain}{api_url}/images".format(
            domain=self.domain, api_url=self.api_url
        )
