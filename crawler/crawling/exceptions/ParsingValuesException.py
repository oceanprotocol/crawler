class ParsingValuesException(Exception):
    def __init__(self, field, message="Error while parsing"):
        self.field = field
        self.message = message
        super().__init__(self.message)
