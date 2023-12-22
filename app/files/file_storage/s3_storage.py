from typing import Protocol, IO, Any

from botocore.exceptions import ClientError

from app.files.file_storage.base import AbstractFileStorage, FileT, File


class BotoClientProtocol(Protocol):
    async def upload_fileobj(self, f: IO, bucket_name: str, object_name: str):
        pass

    async def generate_presigned_url(
            self,
            ClientMethod: str,
            Params: dict = None,
            ExpiresIn: int = 3600,
            HttpMethod: str = None,
    ) -> str:
        pass

    async def get_object(self, Bucket: str, Key: str) -> dict[str, Any]:
        pass


class S3Storage(AbstractFileStorage):
    def __init__(self, boto_client: BotoClientProtocol, bucket_name: str):
        self.boto_client = boto_client
        self.bucket_name = bucket_name

    async def get_object_url(self, object_key: str, expiration=3600) -> str:
        """Generate a presigned URL to share an S3 object

        :param object_key: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """
        try:
            response = await self.boto_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_key,
                },
                ExpiresIn=expiration
            )
        except ClientError as e:
            raise
        return response

    async def upload(self, body: FileT, key: str, mime_type: str) -> str:
        await self.boto_client.upload_fileobj(body, self.bucket_name, key)
        return await self.get_object_url(key)

    async def get_file(self, key: str) -> File:
        download_file = await self.boto_client.get_object(self.bucket_name, key)

        body = download_file.pop("Body")

        file = File(
            body=body,
            additional_data=download_file,
        )

        return file
