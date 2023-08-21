from datetime import datetime


class RamEvent:
    def __init__(self, id: int, ref: str, key: str, type: int,
                 status: str, payload: bytes, retry_count: int, create_time: datetime, update_time: datetime) -> None:
        self.id = id
        self.ref = ref
        self.key = key
        self.type = type
        self.status = status
        self.retry_count = retry_count
        self.payload = payload
        self.create_time = create_time
        self.update_time = update_time

    def __str__(self):
        return f"id={self.id} ref={self.ref} key={self.key} type={self.type} status={self.status}"


