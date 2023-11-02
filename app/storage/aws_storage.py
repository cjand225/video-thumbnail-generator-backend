import aioboto3
from botocore.exceptions import ClientError
from typing import Union
from app.storage.storage_provider import StorageProvider
from app.config import get_config

class AWSStorage(StorageProvider):
    """
    A class for handling storage operations in AWS S3.
    
    This class provides asynchronous methods to interact with AWS S3, including
    operations for reading, writing, deleting files and checking their existence.
    """

    BUCKET_NAME = get_config().BUCKET_NAME
    """
    str: The name of the S3 bucket to interact with. Loaded from configuration.
    """

    async def write_file(self, file_path: str, content: Union[bytes, str]) -> bool:
        """
        Asynchronously writes a file to S3.

        Args:
            file_path (str): The S3 key where the file will be stored.
            content (Union[bytes, str]): The content of the file to be stored.
        
        Returns:
            bool: True if the file was written successfully, False otherwise.
        """
        try:
            session = aioboto3.Session()
            async with session.client('s3') as s3:
                if isinstance(content, str):
                    content = content.encode('utf-8')
                await s3.put_object(Bucket=self.BUCKET_NAME, Key=file_path, Body=content)
            return True
        except ClientError as e:
            print(f"Error writing file {file_path}: {str(e)}")
            return False

    async def read_file(self, file_path: str) -> bytes:
        """
        Asynchronously reads a file from S3.

        Args:
            file_path (str): The S3 key of the file to read.
        
        Returns:
            bytes: The content of the file as bytes, or an empty bytes object if an error occurred.
        """
        try:
            session = aioboto3.Session()
            async with session.client('s3') as s3:
                response = await s3.get_object(Bucket=self.BUCKET_NAME, Key=file_path)
                content = await response['Body'].read()
                return content
        except ClientError as e:
            print(f"Error reading file {file_path}: {str(e)}")
            return b''

    async def delete_file(self, file_path: str) -> bool:
        """
        Asynchronously deletes a file from S3.

        Args:
            file_path (str): The S3 key of the file to delete.
        
        Returns:
            bool: True if the file was deleted successfully, False otherwise.
        """
        try:
            session = aioboto3.Session()
            async with session.client('s3') as s3:
                await s3.delete_object(Bucket=self.BUCKET_NAME, Key=file_path)
            return True
        except ClientError as e:
            print(f"Error deleting file {file_path}: {str(e)}")
            return False

    async def file_exists(self, file_path: str) -> bool:
        """
        Asynchronously checks if a file exists in S3.

        Args:
            file_path (str): The S3 key of the file to check.
        
        Returns:
            bool: True if the file exists, False otherwise.
        """
        try:
            session = aioboto3.Session()
            async with session.client('s3') as s3:
                await s3.head_object(Bucket=self.BUCKET_NAME, Key=file_path)
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == '404':
                return False
            print(f"Error checking if file {file_path} exists: {str(e)}")
            return False

    async def directory_exists(self, directory_path: str) -> bool:
        """
        Asynchronously checks if a directory exists in S3.

        This is determined by checking if there are any objects in S3
        with keys starting with the given directory path.

        Args:
            directory_path (str): The S3 key prefix of the directory to check.
        
        Returns:
            bool: True if the directory exists, False otherwise.
        """
        try:
            session = aioboto3.Session()
            async with session.client('s3') as s3:
                result = await s3.list_objects_v2(Bucket=self.BUCKET_NAME, Prefix=directory_path, MaxKeys=1)
                return 'Contents' in result
        except ClientError as e:
            print(f"Error checking if directory {directory_path} exists: {str(e)}")
            return False

    async def delete_directory(self, directory_path: str) -> bool:
        """
        Asynchronously deletes a directory from S3.

        This deletes all objects in S3 with keys starting with the given directory path.

        Args:
            directory_path (str): The S3 key prefix of the directory to delete.
        
        Returns:
            bool: True if the directory was deleted successfully, False otherwise.
        """
        try:
            session = aioboto3.Session()
            async with session.client('s3') as s3:
                objects_to_delete = []
                paginator = s3.get_paginator('list_objects_v2')
                async for result in paginator.paginate(Bucket=self.BUCKET_NAME, Prefix=directory_path):
                    if 'Contents' in result:
                        for obj in result['Contents']:
                            objects_to_delete.append({'Key': obj['Key']})

                if objects_to_delete:
                    await s3.delete_objects(Bucket=self.BUCKET_NAME, Delete={'Objects': objects_to_delete})
            return True
        except ClientError as e:
            print(f"Error deleting directory {directory_path}: {str(e)}")
            return False
