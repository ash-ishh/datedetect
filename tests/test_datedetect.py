from datedetect import get_format_codes
from functools import partial
from itertools import chain


def append_string_to_elements(_list, string):
    """
    This function appends given string at the end of each element in array
    Args:
        _list: (list)
        string: (str)
    Returns:
        (list)
    """
    return [f"{element}{string}" for element in _list]


def test_all_supported_datetimes():
    test_cases_date = {
        "%d/%m/%Y": "04/11/1997",
        "%m/%d/%Y": "11/04/1997",
        "%Y/%m/%d": "1997/11/04",
        "%b/%d/%Y": "Nov/04/1997",
        "%d/%b/%Y": "04/Nov/1997",
        "%-d/%b/%Y": "2/Nov/1997",
        "%d/%B/%Y": "04/November/1997",
        "%-d/%-m/%Y": "2/2/1997",
        "%-m/%-d/%Y": "2/2/1997",
        "%Y/%-m/%-d": "1997/2/2",
        "%b-%-d-%Y": "Nov-2-1997",
    }

    test_cases_time = {
        "%H:%M": "08:20",
        "%H:%M:%S": "08:20:00",
        "%H:%M:%S.%f": "08:20:00.123456",
        "%-H:%-M": "8:8",
        "%-H:%-M:%-S": "8:2:0",
        "%-H:%-M:%-S.%f": "8:2:0.123456",
    }

    test_cases_timezone = {
        "%z": "+05:30",
    }

    test_cases_invalid = {
        "test": "04111997",
    }

    # Generating test cases with combinations of date, time and timezone
    append_time_to_date = partial(append_string_to_elements, list(test_cases_date.values()))
    append_time_format_to_date_format = partial(append_string_to_elements, list(test_cases_date.keys()))
    test_cases_time_with_space = [f" {time}" for time in list(test_cases_time.values())]
    test_cases_time_format_with_space = [f" {time}" for time in list(test_cases_time.keys())]
    test_cases_date_time = list(chain(*map(append_time_to_date, test_cases_time_with_space)))
    test_cases_date_time_format = list(
        chain(*map(append_time_format_to_date_format, test_cases_time_format_with_space)))

    append_timezone_into_date_time = partial(append_string_to_elements, list(test_cases_date_time))
    append_timezone_format_into_date_time_format = partial(append_string_to_elements, list(test_cases_date_time_format))
    test_cases_date_time_timezone = list(
        chain(*map(append_timezone_into_date_time, list(test_cases_timezone.values()))))
    test_cases_date_time_timezone_format = list(chain(*map(append_timezone_format_into_date_time_format,
                                                           list(test_cases_timezone.keys()))))
    test_cases = list(test_cases_date.values()) + test_cases_date_time + test_cases_date_time_timezone
    test_cases_format = list(
        test_cases_date.keys()) + test_cases_date_time_format + test_cases_date_time_timezone_format

    test_cases_dict = dict(list(zip(test_cases_format, test_cases)))
    failed = []
    for _format, date in test_cases_dict.items():
        possible_datetime_formats = get_format_codes(date)
        if not _format in possible_datetime_formats:
            failed.append((date, _format))

    print(failed)
    assert len(failed) == 0


