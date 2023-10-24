from abc import ABC, abstractmethod
from typing import Union

class StorageProvider(ABC):
    """
    An abstract base class defining the interface for storage operations.

    This class provides abstract methods for writing, reading, deleting files,
    and checking if a file exists. Concrete implementations of this class should
    provide the specific details for these operations.
    """

    @staticmethod
    @abstractmethod
    async def write_file(file_path: str, content: Union[bytes, str]):
        """
        Writes content to a file asynchronously.

        Args:
            file_path (str): The path of the file to write the content to.
            content (Union[bytes, str]): The content to be written to the file. Can be either bytes or a string.

        Raises:
            NotImplementedError: If this method is not implemented by the concrete class.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def read_file(file_path: str) -> bytes:
        """
        Reads and returns the content of a file asynchronously.

        Args:
            file_path (str): The path of the file to read the content from.

        Returns:
            bytes: The content of the file.

        Raises:
            NotImplementedError: If this method is not implemented by the concrete class.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def delete_file(file_path: str):
        """
        Deletes a file.

        Args:
            file_path (str): The path of the file to delete.

        Raises:
            NotImplementedError: If this method is not implemented by the concrete class.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def file_exists(file_path: str) -> bool:
        """
        Checks if a file exists.

        Args:
            file_path (str): The path of the file to check.

        Returns:
            bool: True if the file exists, False otherwise.

        Raises:
            NotImplementedError: If this method is not implemented by the concrete class.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def directory_exists(directory_path: str) -> bool:
        """
        Checks if a directory exists.

        Args:
            directory_path (str): The path of the directory to check.

        Returns:
            bool: True if the directory exists, False otherwise.

        Raises:
            NotImplementedError: If this method is not implemented by the concrete class.
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def delete_directory(directory_path: str) -> bool:
        """
        Deletes a directory and all its contents.

        Args:
            directory_path (str): The path of the directory to delete.

        Returns:
            bool: True if the directory is sucessfully deleted, False otherwise.

        Raises:
            NotImplementedError: If this method is not implemented by the concrete class.
        """
        raise NotImplementedError
