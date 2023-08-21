import os

from app.core.config import settings
from app.storage.storage_handler import StorageHandler


class FsHandler(StorageHandler):
    
    def __init__(self):
        self.directory = settings.FS_DIRECTORY
    
    def get_path(self, file_name):
        return self.directory + "/" + file_name
    
    def check_file_name_exists(self, file_name):
        return os.path.isfile(self.get_path(file_name))
    
    def read(self, file_name: str) -> bytes:
        f = open(self.get_path(file_name), "rb")
        return f.read()
    
    def write(self, file_name: str, content: bytes):
        with open(self.get_path(file_name), "wb") as binary_file:
            binary_file.write(content)
