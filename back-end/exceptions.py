class InvalidModelProperties(Exception):
    def __init__(self):
        super().__init__('Unable to create new DB object due to invalid properties.')

class InitialDataInsertionException(Exception):
    def __init__(self):
        super().__init__('Unable to insert initial data to database.')