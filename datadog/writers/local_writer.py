from datadog.writers.base import Writer


class LocalWriter(Writer):
    """
    The local writer will write on local disk
    """

    def __init__(self, **kwargs):
        super(LocalWriter, self).__init__(**kwargs)

    def write(self, content, file_name):
        """
        This method will write the content in the file path/file_name
        :param content: str
        :param file_name: str
        :return: str, The full path to the data
        """
        try:
            file_name = file_name.lstrip("/")
            full_path = f"{self.path}/{file_name}"
            with open(f"{self.path}/{file_name}", "w") as file:
                file.write(content)
                return full_path
        except Exception as err:
            message = f"Could not write content to file {file_name} : {err}"
            print(message)
            raise Exception(message)
