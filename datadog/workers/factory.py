from datadog.workers.local_worker import LocalConsumer


def factory_worker(worker_type, **kwargs):
    """
    This method is a factory that will return a worker depending on the type/
    :param type: one of (local)
    :param kwargs: Parameters to instanciate the worker
    :return: a Worker
    """

    if worker_type == "local":
        return LocalConsumer(**kwargs)
    else:
        raise NotImplementedError("The only consumers implemented at the moment are : (LocalConsumer)")
