

class Writer:
    """
    A writer is responsible for persisting data in a file at a certain path.
    """

    def __init__(self, path):
        self.path = path.rstrip("/")

    def write(self, content, file_name):
        raise NotImplementedError("Writer must implement write method")
