from datadog.db.base import BaseDb
from datadog.utils.constants import DATE_FORMAT_WITH_HOURS
from tinydb import TinyDB, Query


class TinyDatabase(BaseDb):

    def __init__(self, database):
        self.db = TinyDB(database)

    def get(self, date):
        query = Query()
        date_str = date.strftime(DATE_FORMAT_WITH_HOURS)
        doc = self.db.get(query.date == date_str)
        return doc

    def insert(self, document):
        document["date"] = document["date"].strftime(DATE_FORMAT_WITH_HOURS)
        self.db.insert(document)

    def update(self, date, new_data):
        query = Query()
        date_str = date.strftime(DATE_FORMAT_WITH_HOURS)
        self.db.upsert(new_data, query.date == date_str)
