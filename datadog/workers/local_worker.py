
from datadog.clients.wikimedia import WikimediaDownloader
from datadog.workers.base import Worker
from datadog.utils.constants import FAILED, SUCCESS

class LocalConsumer(Worker):

    def __init__(self, *args, **kwargs):
        super(LocalConsumer, self).__init__(**kwargs)
        self.wikimedia_downloader = WikimediaDownloader()
        self.wikimedia_downloader.download_blacklist()

    def run(self):
        while True:
            if not self.queue.empty():

                try:
                    message = self.queue.get()
                    print('Getting ' + str(message)+ ' : ' + ' items in queue')

                    date = message
                    task = self.db.get(date)

                    if task.get("status") != SUCCESS:
                        df = self.wikimedia_downloader.download(date)
                        filtered_df = self.wikimedia_downloader.filter_blacklist(df)
                        aggregated_df = self.wikimedia_downloader.aggregate_pages_views(filtered_df)
                        top_25_page_views = self.wikimedia_downloader.return_top_pages_views(aggregated_df, 25)
                        content = top_25_page_views.to_csv(index=False)
                        path = self.writer.write(content, f"{date}.csv")

                        print(f"Successfully exported for date {date}")

                        self.db.update(date, {"status": SUCCESS, "data_path": path})

                except Exception as err:
                    print(f"An issue occurred while consuming {message} : {err}")

                    try_count = task.get("try_count")
                    max_tries = task.get("max_tries")

                    if try_count < max_tries:
                        print(f"Message {message} will be reprocessed as it failed {try_count} and did not"
                              f" reached the {max_tries} limit")
                        self.db.update(date, {"status": FAILED, "try_count": try_count + 1})
                        self.queue.put(message)
