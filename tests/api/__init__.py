class MockResponse:
    def __init__(self, text: str, status_code: str):
        self.text = text
        self.status_code = status_code
