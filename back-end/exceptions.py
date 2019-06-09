class InvalidModelProperties(Exception):
    def __init__(self):
        super().__init__('Unable to create new DB object due to invalid properties.')