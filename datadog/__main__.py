from datadog.api import app
from datadog.workers.factory import factory_worker
from datadog.queues.factory import factory_queue
from datadog.writers.factory import factory_writer
from datadog.db.factory import factory_db


def create_queue(config):
    queue_type = config["queue"]["type"]
    queue_args = config["queue"]["args"]
    return factory_queue(type=queue_type, **queue_args)


def create_workers(config, queue, db):

    worker_type = config["workers"]["type"]
    num_workers = config["workers"]["num_workers"]
    writer_type = config["workers"]["writer"]["writer_type"]
    writer_path = config["workers"]["writer"]["writer_path"]

    workers = []

    for _ in range(num_workers):
        worker = factory_worker(worker_type=worker_type,
                                queue=queue,
                                writer=factory_writer(writer_type, writer_path),
                                db=db
                                )
        worker.daemon = True
        worker.start()
        workers.append(worker)
    return workers


def create_database(config):

    db_type = config["db"]["type"]
    args = config["db"]["args"]

    return factory_db(db_type, **args)


if __name__ == '__main__':

    config = {
        "host": "0.0.0.0",
        "port": "8080",
        "queue": {
            "type": "local",
            "args": {
                "maxsize": -1
            }
        },
        "workers": {
            "type": "local",
            "num_workers": 2,
            "writer": {
                "writer_type": "local",
                "writer_path": "./data/reports"
            }
        },
        "db": {
            "type": "local",
            "args": {
                "database": "./data/db/db.json"
            }
        }
    }

    queue = create_queue(config)
    db = create_database(config)
    app = app.create_app(queue, db)
    workers = create_workers(config, queue, db)

    try:
        app.run(host=config["host"], port=config["port"], debug=True)
    except KeyboardInterrupt:
        print("Stopping workers ...")
        for worker in workers:
            worker.exit_scheduled = True
        for worker in workers:
            worker.join()
        print("Workers stopped !")
