from os.path import basename, join
from os import remove
from PIL import Image
from mirel.core.protocols import ImageEditor


class ImageEditorImpl(ImageEditor):
    def __init__(self, folder: str):
        self._folder = folder

    async def optimize(self, path_to_image: str) -> str:
        image = Image.open(path_to_image)
        filename = basename(path_to_image)
        filename, old_ext = filename.split(".")

        if image.info:
            image_without_metadata = Image.new(image.mode, image.size)
            image_without_metadata.putdata(list(image.getdata()))
            image = image_without_metadata

        jpeg_image = image.convert("RGB")
        path_to_new_image = join(self._folder, f"{filename}.jpg")

        jpeg_image.save(path_to_new_image)
        if old_ext != "jpg":
            remove(path_to_image)

        return path_to_new_image
