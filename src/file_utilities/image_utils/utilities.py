class ImageConversionError(Exception):
    def __init__(self, message="An error occurred during image conversion", *args):
        self.message = message
        super().__init__(self.message, *args)
