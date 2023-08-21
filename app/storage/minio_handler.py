import logging
import random
from datetime import datetime, timedelta
from io import BytesIO

from fastapi import Depends
from minio import Minio
from slugify import slugify

from app.core.config import settings
from app.dependencies import lang_header
from app.i18n.lang import MultiLanguage
from app.storage.storage_handler import StorageHandler

logger = logging.getLogger()


def normalize_file_name(file_name):
    # try:
    file_name = " ".join(file_name.strip().split())
    file_ext = file_name.split('.')[-1]
    file_name = ".".join(file_name.split('.')[:-1])
    file_name = slugify(file_name)
    file_name = file_name[:100]
    file_name = file_name + '.' + file_ext
    return file_name


class MinioHandler(StorageHandler):
    __instance = None

    def __init__(self,
                 lang: MultiLanguage = Depends(lang_header),
                 ):
        self.minio_url = settings.MINIO_ENDPOINT
        self.access_key = settings.MINIO_ACCESS_KEY
        self.secret_key = settings.MINIO_SECRET_KEY
        self.bucket_name = settings.BUCKET_NAME
        self.__client = None
        self.lang = lang

    @property
    def client(self) -> Minio:
        if not self.__client:
            self.__client = Minio(
                self.minio_url,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=False,
            )
            if not self.__client.bucket_exists(self.bucket_name):
                self.__client.make_bucket(self.bucket_name)
        return self.__client

    # def make_bucket(self) -> str:
    #     if not self.client.bucket_exists(self.bucket_name):
    #         self.client.make_bucket(self.bucket_name)
    #     return self.bucket_name

    def check_file_name_exists(self, file_name):
        try:
            self.client.stat_object(bucket_name=self.bucket_name, object_name=file_name)
            return True
        except Exception as e:
            logger.debug(e)
            return False

    def read(self, file_name: str) -> bytes:
        return self.client.get_object(self.bucket_name, file_name).read()

    def write(self, file_name: str, content: bytes):
        self.client.put_object(bucket_name=self.bucket_name,
                               object_name=file_name,
                               data=BytesIO(content),
                               length=-1,
                               part_size=10 * 1024 * 1024
                               )

    def put_object_to_minio(self, content_type, file_data, object_name):
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=file_data,
            content_type=content_type,
            length=-1,
            part_size=10 * 1024 * 1024
        )

    def presigned_get_object(self, bucket_name, object_name):
        # Request URL expired after 7 days
        url = self.client.presigned_get_object(
            bucket_name=bucket_name,
            object_name=object_name,
            expires=timedelta(days=7)
        )
        return url

    def put_object(self, file_data, file_name, content_type):
        file_name = normalize_file_name(file_name)
        datetime_prefix = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        object_name = f"{datetime_prefix}___{file_name}"
        while self.check_file_name_exists(file_name=object_name):
            random_prefix = random.randint(1, 1000)
            object_name = f"{datetime_prefix}___{random_prefix}___{file_name}"

        self.put_object_to_minio(content_type, file_data, object_name)

        url = self.presigned_get_object(
            bucket_name=self.bucket_name, object_name=object_name)
        data_file = {
            'bucket_name': self.bucket_name,
            'file_name': object_name,
            'url': url
        }
        return data_file


def from_file_type_to_mime_type(file_type: str) -> str:
    FILE_TYPE_TO_MIME = {
        'rar': 'application/vnd.rar',
        'zip': 'application/zip',
        'png': 'image/png',
        'pdf': 'application/pdf',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    }

    return FILE_TYPE_TO_MIME.get(file_type, 'application/octet-stream')
