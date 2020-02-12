from queue import Queue


def factory_queue(type, **kwargs):
    """
    This method is a factory that will return a queue depending on the type/
    :param type: one of (local)
    :param kwargs: Parameters to instanciate the queue
    :return: a Queue
    """
    if type == "local":
        return Queue(**kwargs)
    else:
        raise NotImplementedError("The only queues implemented at the moment are : (Queue)")

