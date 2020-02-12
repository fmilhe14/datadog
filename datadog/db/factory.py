from datadog.db.tinydb import TinyDatabase


def factory_db(database_type, **kwargs):
    """
    This method is a simple factory that will return a Database connnection depending on the worker type
    :param database_type: one of (local)
    :param kwargs: Parameters to instanciate a database connection
    :return:
    """
    if database_type == "local":
        return TinyDatabase(**kwargs)
    else:
        raise NotImplementedError("The only consumers implemented at the moment are : (LocalConsumer)")
