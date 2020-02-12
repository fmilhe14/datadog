import pytest
from datetime import datetime
from datadog.utils.daterange import daterange


@pytest.mark.parametrize(
    "request_params,expected",
    [
        (
                (datetime(2020, 1, 1, 1), datetime(2020, 1, 1, 3)),
                [datetime(2020, 1, 1, 1), datetime(2020, 1, 1, 2), datetime(2020, 1, 1, 3)]
         ),
        (
                (datetime(2020, 1, 1, 1), datetime(2020, 1, 1, 1)),
                [datetime(2020, 1, 1, 1)]
        ),
    ]
)
def test_date_range(request_params, expected):

    date_range = daterange(*request_params)

    assert list(date_range) == expected


