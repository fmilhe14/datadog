import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from datadog.clients.wikimedia import WikimediaDownloader

@pytest.mark.parametrize(
    "request_params,expected",
    [
        (
                [(".a", "page", 1, 0), (".a", "page", 1, 0), (".c", "page", 1, 0)],
                [(".a", "page", 2, 0), (".c", "page", 1, 0)]
         ),
        (
                [(".a", "page", 1, 0), (".b", "page", 1, 0), (".c", "page", 1, 0)],
                [(".a", "page", 1, 0), (".b", "page", 1, 0), (".c", "page", 1, 0)]
         ),

    ]
)
def test_aggregate_pages_views(request_params, expected):

    downloader = WikimediaDownloader()

    df = pd.DataFrame(request_params, columns=downloader.COLUMNS)
    new_df = downloader.aggregate_pages_views(df)

    assert_frame_equal(new_df, pd.DataFrame(expected, columns=downloader.COLUMNS), check_dtype=False)


@pytest.mark.parametrize(
    "request_params,expected",
    [
        (
                [(".a", "page", 1), (".b", "page", 1), (".c", "page", 1)],
                [(".a", "page", 1), (".b", "page", 1), (".c", "page", 1)]
         ),
        (
                [(".a", "page", 2), (".a", "page2", 1), (".c", "page", 1)],
                [(".a", "page", 2), (".c", "page", 1)]
         ),

    ]
)
def test_return_top_pages_views(request_params, expected):

    downloader = WikimediaDownloader()

    df = pd.DataFrame(request_params, columns=downloader.COLUMNS[0:3])
    new_df = downloader.return_top_pages_views(df, 1)

    assert_frame_equal(new_df, pd.DataFrame(expected, columns=downloader.COLUMNS[0:3]), check_dtype=False)


@pytest.mark.parametrize(
    "request_params,expected",
    [
        (
                [(".a", "page", 1), (".b", "page", 1), (".c", "page", 1)],
                [(".b", "page", 1), (".c", "page", 1)]
         ),
        (
                [(".a", "page", 2), (".a", "page2", 1), (".c", "page", 1)],
                [(".c", "page", 1)]
         ),
        (
                [(".d", "page", 1), (".b", "page", 1), (".c", "page", 1)],
                [(".d", "page", 1), (".b", "page", 1), (".c", "page", 1)]
        ),

    ]
)
def test_filter_blacklist(request_params, expected):

    downloader = WikimediaDownloader()
    downloader.blacklist = pd.DataFrame([(".a", "page"), (".a", "page2")], columns=downloader.COLUMNS[0:2])

    df = pd.DataFrame(request_params, columns=downloader.COLUMNS[0:3])
    new_df = downloader.filter_blacklist(df)

    assert_frame_equal(new_df, pd.DataFrame(expected, columns=downloader.COLUMNS[0:3]), check_dtype=False)
