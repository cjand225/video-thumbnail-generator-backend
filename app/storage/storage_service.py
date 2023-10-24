from typing import Union
from app.storage.storage_provider import StorageProvider

class StorageService:
    """
    A service class that abstracts file storage operations, allowing for
    easy interchangeability between different storage providers.
    
    Attributes:
        storage_provider (StorageProvider): An instance of a class implementing
            the StorageProvider interface, providing file storage services.
    """

    def __init__(self, storage_provider: StorageProvider):
        """
        Initializes the StorageService with a specific storage provider.

        Args:
            storage_provider (StorageProvider): An instance of a class implementing
                the StorageProvider interface, providing file storage services.
        """
        self.storage_provider = storage_provider
    
    async def write_file(self, file_path: str, content: Union[bytes, str]) -> bool:
        """
        Writes content to a file at the specified path asynchronously.

        Args:
            file_path (str): The path where the file should be written.
            content (Union[bytes, str]): The content to be written to the file.

        Returns:
            bool: True if the write operation was successful, False otherwise.
        """
        try:
            await self.storage_provider.write_file(file_path, content)
            return True
        except Exception as e:
            print(f"Failed to write file: {str(e)}")
            return False
    
    async def read_file(self, file_path: str) -> bytes:
        """
        Reads and returns the content of a file at the specified path asynchronously.

        Args:
            file_path (str): The path of the file to read.

        Returns:
            bytes: The content of the file.
        """
        return await self.storage_provider.read_file(file_path)
    
    async def delete_file(self, file_path: str) -> bool:
        """
        Deletes a file at the specified path asynchronously.

        Args:
            file_path (str): The path of the file to delete.

        Returns:
            bool: True if the delete operation was successful, False otherwise.
        """
        try:
            await self.storage_provider.delete_file(file_path)
            return True
        except Exception as e:
            print(f"Failed to delete file: {str(e)}")
            return False
    
    async def file_exists(self, file_path: str) -> bool:
        """
        Checks asynchronously if a file exists at the specified path.

        Args:
            file_path (str): The path of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return await self.storage_provider.file_exists(file_path)

    async def directory_exists(self, directory_path: str) -> bool:
        """
        Checks asynchronously if a directory exists at the specified path.

        Args:
            directory_path (str): The path of the directory to check.

        Returns:
            bool: True if the directory exists, False otherwise.
        """
        return await self.storage_provider.directory_exists(directory_path)

    async def delete_directory(self, directory_path: str) -> bool:
        """
        Deletes a directory at the specified path asynchronously.

        Args:
            directory_path (str): The path of the directory to delete.

        Returns:
            bool: True if the delete operation was successful, False otherwise.
        """
        return await self.storage_provider.delete_directory(directory_path)
