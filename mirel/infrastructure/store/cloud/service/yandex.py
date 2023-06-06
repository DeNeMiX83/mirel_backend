from os.path import basename, join
from os import remove
import yadisk
from yadisk.exceptions import PathNotFoundError
from mirel.config.settings import Settings
from mirel.infrastructure.store.cloud.protocols import Service


class YandexDiskService(Service):
    def __init__(self, settings: Settings):
        self._yadick = yadisk.YaDisk(token=settings.yandex_disk.token)
        self._folder = settings.yandex_disk.folder
        self._folder_for_save = settings.path_to_folder_for_save_image
        self._link_for_image = settings.link_to_image

    async def create_image(self, path_to_image: str) -> str:
        filename = basename(path_to_image)
        path_for_disk = join(self._folder, filename)

        self._yadick.upload(path_to_image, path_for_disk)
        remove(path_to_image)

        return f"{self._link_for_image}/{filename}"

    async def get_image(self, filename: str) -> str:
        path_to_image = join(self._folder, filename)
        path_for_save = join(self._folder_for_save, filename)
        try:
            self._yadick.download(path_to_image, path_for_save)
        except PathNotFoundError:
            raise
        return path_for_save
