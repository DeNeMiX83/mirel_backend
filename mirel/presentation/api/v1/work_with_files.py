from os.path import join
import uuid
from fastapi import UploadFile


async def save_file(
    new_file: UploadFile, folder: str, extension_name: str = ""
) -> str:
    old_filename = new_file.filename
    if old_filename is None:
        raise ValueError("Нету имени файла")
    file_extension = old_filename.split(".")[1]
    filename = f"{extension_name}_{str(uuid.uuid4())}" + "." + file_extension
    filename = join(folder, filename)
    with open(filename, "wb") as f:
        content = await new_file.read()
        f.write(content)
    return filename
