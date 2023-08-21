class EventStatus:
    # Sender's event status
    SCHEDULED_FOR_SEND = "SCHEDULED_FOR_SEND"
    SENDING = "SENDING"
    SENT = "SENT"
    FAILED_SEND = "FAILED_SEND"
    # Receiver's event status
    CREATED = "CREATED"
    HANDLING = "HANDLING"
    DONE = "DONE"
    FAILED_HANDLE = "FAILED_HANDLE"
    PENDING_LIST = [SCHEDULED_FOR_SEND, SENDING, CREATED, HANDLING]
    SENDER_LIST = [SCHEDULED_FOR_SEND, SENDING, SENT, FAILED_SEND]
    RECEIVER_LIST = [CREATED, HANDLING, DONE, FAILED_HANDLE]
    FINISHED_LIST = [SENT, DONE]
    FAILED_LIST = [FAILED_SEND, FAILED_HANDLE]

    @classmethod
    def get_failure(cls, status):
        if status in cls.SENDER_LIST:
            return cls.FAILED_SEND
        else:
            return cls.FAILED_HANDLE

    @classmethod
    def get_success(cls, status):
        if status in cls.SENDER_LIST:
            return cls.SENT
        else:
            return cls.DONE

    @classmethod
    def get_running(cls, status):
        if status in cls.SENDER_LIST:
            return cls.SENDING
        else:
            return cls.HANDLING

    @classmethod
    def get_standby(cls, status):
        if status in cls.SENDER_LIST:
            return cls.SCHEDULED_FOR_SEND
        else:
            return cls.CREATED


class EventActionStatus:
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCEEDED = "SUCCEEDED"
    TIMED_OUT = "TIMED_OUT"


class DefaultConfig:
    # common config
    USE_PROMETHEUS = True
    # database method config
    DB_ENABLE_HANDLE_MESSAGE = True
    DB_POLL_PERIOD = 0.1  # seconds
    DB_POLL_LIMIT = 1000
    DB_MAX_RETRY = 5
    DB_SENDER_TIMEOUT = 10  # seconds
    DB_HANDLER_TIMEOUT = 20  # seconds
    DB_BACKOFF = 5  # second
    DB_ENABLE_HANDLE_RETENTION = False
    DB_RETENTION_HANDLE_PERIOD = 300  # seconds
    DB_RETENTION_TIME = 30  # days
    DB_RETENTION_LIMIT_PER_DELETE = 1000
    DB_RETENTION_TABLES = ["ram_event_actions", "ram_events"]
    # kafka method config
    KAFKA_MAX_NUMBER_PARTITION = 1
    KAFKA_ENABLE_HANDLE_MESSAGE = True
    KAFKA_POLL_LIMIT = 5
    KAFKA_SESSION_TIMEOUT_MS = 300000
    KAFKA_ENABLE_RETRY = False
    KAFKA_RETRY_DURATIONS = []
    KAFKA_ENABLE_DLQ = True
