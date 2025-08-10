from enum import Enum

class StatusCode(Enum):
    SUCCESS = "200"
    BAD_REQUEST = "400"
    UNAUTHORIZED = "401"
    FORBIDDEN = "403"
    NOT_FOUND = "404"
    INTERNAL_SERVER_ERROR = "500"
    MISSING_INPUT = 'MISSING_INPUT'
    MISSING_CREDENTIALS = 'MISSING_CREDENTIALS'
    INVALID_CREDENTIALS = 'INVALID_CREDENTIALS'
    USER_NOT_REGISTERED = 'USER_NOT_REGISTERED'
    NOT_IMPLEMENTED = 'NOT_IMPLEMENTED'

    def __str__(self):
        return self.value


class JwtErrorCode(Enum):
    TOKEN_EXPIRED = 'TOKEN_EXPIRED'
    INVALID_TOKEN = 'INVALID_TOKEN'

    def __str__(self):
        return self.value
    

class WalletType(Enum):
    CUSTODIAL = 'custodial'
    NON_CUSTODIAL = 'non_custodial'

    def __str__(self):
        return self.value


class StorageType(Enum):
    HOT = 'hot'
    COLD = 'cold'

    def __str__(self):
        return self.value