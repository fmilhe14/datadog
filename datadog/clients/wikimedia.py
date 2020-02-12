import pandas as pd

from datadog.utils.constants import DATE_FORMAT


class WikimediaDownloader:
    """
    The aim of this class id to download a specific pageviews report.
    It also provides some method to aggregate, filter the output of the download.
    """

    URL = 'https://dumps.wikimedia.org/other/pageviews/{year}/{year}-{month}/pageviews-{dsnodash}-{hour}0000.gz'
    COLUMNS = ["domain_code", "page_title", "count_views", "total_response_size"]
    BLACKLIST_URL = "https://s3.amazonaws.com/dd-interview-data/data_engineer/wikipedia/blacklist_domains_and_pages" #TODO ADD IN CONFIG

    def download_blacklist(self):
        if not self.blacklist:
            self.blacklist = pd.read_csv(self.BLACKLIST_URL, header=None, delimiter=" ", names=self.COLUMNS[0:2])

    def download(self, date):
        """
        This method will download a report for a specific date and return a pandas dataframe
        :param date:
        :return: pandas Dataframe
        """

        dsnodash = date.strftime(DATE_FORMAT)
        year = date.year
        month = "0"+str(date.month) if date.month < 10 else date.month
        hour = "0"+str(date.hour) if date.hour < 10 else date.hour

        url = self.URL.format(
            year=year,
            month=month,
            hour=hour,
            dsnodash=dsnodash
        )

        df = pd.read_csv(url, compression="gzip", delimiter=" ", names=self.COLUMNS)

        df[self.COLUMNS[0]] = df[self.COLUMNS[0]].str.lower()
        df[self.COLUMNS[1]] = df[self.COLUMNS[1]].str.lower()
        del df['total_response_size']

        return df

    def aggregate_pages_views(self, df):
        """
        This method will aggregate the page_views for each pair (domain, page_title)
        :param df:
        :return: pandas Dataframe
        """

        aggregated_df = df.groupby([self.COLUMNS[0], self.COLUMNS[1]], as_index=False).sum()
        return aggregated_df

    def return_top_pages_views(self, df, n):
        """
        This method will return the top n pages for each domain.
        :param df:
        :param n: The number of results to return.
        :return: pandas Dataframe
        """
        return df.groupby(self.COLUMNS[0]).apply(lambda x: x.nlargest(n, self.COLUMNS[2])).reset_index(drop=True)

    def filter_blacklist(self, df):
        """
        This method will apply the blacklist to the dataframe df in order to delete all the tuples
        (domain, page_title) blacklisted elements.
        :param df:
        :return: pandas Dataframe
        """

        dfe = pd.merge(df, self.blacklist, how='left', on=[self.COLUMNS[0], self.COLUMNS[1]], indicator=True)
        dfe = dfe[dfe["_merge"] == 'left_only']
        del dfe["_merge"]
        dfe.reset_index(drop=True, inplace=True)
        return dfe




