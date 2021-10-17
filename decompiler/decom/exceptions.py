class CommandLineOptions(Exception):
    def __init__(self, message, parser, *args, **kwargs):
        self.message = message
        self.parser = parser
        super().__init__(message, *args, **kwargs)
