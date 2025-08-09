class BaseApiException(Exception):
    def __init__(self, success: bool = None, code: str = None, data: dict = None):
        self.success = success
        self.code = code
        self.data = data
        super().__init__(f"success: {self.success}, code: {self.code}, data: {self.data}")

    def __str__(self):
        data = {
            "success": self.success,
            "code": self.code,
            "data": self.data,
        }
        return str(data)


class GenericApiException(BaseApiException):
    def __init__(self, success=False, code="OK", data=None):
        super().__init__(success=success, code=code, data=data)


class ExternalApiResponseWrapper(BaseApiException):
    def __init__(self, success=True, code="OK", data=None):
        super().__init__(success=success, code=code, data=data)