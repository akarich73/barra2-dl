import pytest

from pandas import Timestamp

from barra2_dl import helpers

@pytest.mark.parametrize(('start_datetime', 'end_datetime', 'expected'), [
                            ('1/1/2023','1/1/2024',
                            [Timestamp('2023-01-01 00:00:00'),
                            Timestamp('2023-02-01 00:00:00'),
                            Timestamp('2023-03-01 00:00:00'),
                            Timestamp('2023-04-01 00:00:00'),
                            Timestamp('2023-05-01 00:00:00'),
                            Timestamp('2023-06-01 00:00:00'),
                            Timestamp('2023-07-01 00:00:00'),
                            Timestamp('2023-08-01 00:00:00'),
                            Timestamp('2023-09-01 00:00:00'),
                            Timestamp('2023-10-01 00:00:00'),
                            Timestamp('2023-11-01 00:00:00'),
                            Timestamp('2023-12-01 00:00:00'),
                            Timestamp('2024-01-01 00:00:00')]
                           ),
])
def test_list_months(start_datetime: str, end_datetime: str, expected: list) -> None:
    """Test with parametrization."""
    assert helpers.list_months(start_datetime, end_datetime) == expected

