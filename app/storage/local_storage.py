import aiofiles
import aiofiles.os
from typing import Union
from app.storage.storage_provider import StorageProvider

class LocalStorage(StorageProvider):
    """
    A class that implements local file storage operations.

    This class provides methods to perform create, read, delete, and check
    operations on files stored locally on the server's file system.
    """

    @staticmethod
    async def write_file(file_path: str, content: Union[bytes, str]):
        """
        Writes content to a file at the specified file path asynchronously.

        If the content is a string, it is encoded to bytes before writing.
        
        Args:
            file_path (str): The path of the file to write the content to.
            content (Union[bytes, str]): The content to be written to the file. Can be either bytes or a string.

        Raises:
            OSError: If there is an issue opening or writing to the file.
        """
        async with aiofiles.open(file_path, "wb") as f:
            if isinstance(content, str):
                content = content.encode()
            await f.write(content)

    @staticmethod
    async def read_file(file_path: str) -> bytes:
        """
        Reads and returns the content of a file at the specified file path asynchronously.

        Args:
            file_path (str): The path of the file to read the content from.

        Returns:
            bytes: The content of the file.

        Raises:
            OSError: If there is an issue opening or reading from the file.
        """
        async with aiofiles.open(file_path, "rb") as f:
            return await f.read()

    @staticmethod
    async def delete_file(file_path: str):
        """
        Deletes a file at the specified file path.

        Args:
            file_path (str): The path of the file to delete.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If there is insufficient permission to delete the file.
        """
        await aiofiles.os.remove(file_path)

    @staticmethod
    async def file_exists(file_path: str) -> bool:
        """
        Checks if a file exists at the specified file path.

        Args:
            file_path (str): The path of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return await aiofiles.os.path.isfile(file_path)
