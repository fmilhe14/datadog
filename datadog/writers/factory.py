from datadog.writers.local_writer import LocalWriter


def factory_writer(type, path):
    """
    This method is a factory that will return a writer depending on the type/
    :param type: one of (local)
    :param kwargs: Parameters to instanciate the writer
    :return: a Writer
    """
    if type == "local":
        return LocalWriter(path=path)
