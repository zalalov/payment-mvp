class InvalidModelProperties(Exception):
    def __init__(self, message=None):
        super(InvalidModelProperties, self).__init__(
            message if message else 'Unable to create new DB object due to invalid properties.')


class InitialDataInsertionException(Exception):
    def __init__(self, message=None):
        super(InitialDataInsertionException, self).__init__(
            message if message else 'Unable to insert initial data to database.'
        )


class InvalidDBSchemeStateException(Exception):
    def __init__(self, message=None):
        super(InvalidDBSchemeStateException, self).__init__(message if message else 'DB Scheme is invalid.')


class DBQueryExecutionFailedException(Exception):
    def __init__(self, message=None):
        super(DBQueryExecutionFailedException, self).__init__(message if message else 'Unable to execute DB query.')


class DBRecordNotFound(Exception):
    def __init__(self, message=None):
        super(DBRecordNotFound, self).__init__(message if message else 'Record not found in DB.')


class PermissionDeniedException(Exception):
    def __init__(self, message=None):
        super(PermissionDeniedException, self).__init__(message if message else 'Permission denied.')


class AccountHasntEnoughMoneyException(Exception):
    def __init__(self, message=None):
        super(AccountHasntEnoughMoneyException, self).__init__(
            message if message else 'No enough money in the account.'
        )


class TransferDifferentCurrenciesException(Exception):
    def __init__(self, message=None):
        super(TransferDifferentCurrenciesException, self).__init__(
            message if message else 'Unable to make transfer between different currency accounts.'
        )


class InvalidJSONRequest(Exception):
    def __init__(self, message=None):
        super(InvalidJSONRequest, self).__init__(message if message else 'Invalid JSON in request.')
