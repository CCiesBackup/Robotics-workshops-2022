class MessageProcessingException(Exception):

    def __init__(self):
        super().__init__("Processing mismatch! Couldn't process the payload properly! :(")

