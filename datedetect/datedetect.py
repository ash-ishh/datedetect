__author__ = "Ash-Ishh.."
__version__ = "1.0.0"
__email__ = "mr.akc@outlook.com"


from functools import partial
import operator
import re

from datedetect.exceptions import InvalidArguments


def get_regex(_type, delimiter, _format):
    """
    This function returns regex of given date format.
    :param _type:
    :param delimiter: string
    :param _format: string
    :return: regex string
    """
    attributes = _format.split(delimiter) if delimiter else [_format]
    regex = []
    for attribute in attributes:
        try:
            regex.append(regex_patterns.get(_type)[attribute])
        except KeyError as _:
            regex.append(attribute)
    final_regex = regex_patterns.get(_type).get(delimiter, "").join(regex)
    return final_regex

regex_patterns = {
    "date": {
        "%d": r"(?:0[1-9]|1[0-9]|2[0-9]|3[0-1])(?!\d)",
        "%m": r"(?:0[1-9]|1[0-2])(?!\d)",
        "%b": r"(?:[a-z]{3})",
        "%B": r"(?:may|[a-z]{4,9})",
        "%Y": r"(?<!\d)\d{4}(?!\d)",
        "%y": r"(?<!\d)\d{2}(?!\d)",
        "%-d": r"(?:(?<!\d)[1-9]|1[0-9]|2[0-9]|3[0-1])(?!\d)",
        "%-m": r"(?:(?<!\d)[1-9]|1[0-2])(?!\d)",
        "/": r"\W"
    },
    "time": {
        "%H": r"(?:(?<!\d)0[0-9]|1[0-9]|2[0-3](?!\d))",
        "%I": r"(?:(?<!\d)0[0-9]|1[0-2](?!\d))",
        "%M": r"(?:(?<!\d)0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9](?!\d))",
        "%S": r"(?:(?<!\d)0[0-9]|1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9](?!\d))",
        "%f": r"(?<!\d)\d{6}(?!\d)",
        "%-H": r"(?:(?<!\d)1[0-9]|2[0-3]|[0-9](?!\d))",
        "%-M": r"(?:(?<!\d)1[0-9]|2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9](?!\d))",
        "%-S": r"(?:(?<!\d)1[0-9]2[0-9]|3[0-9]|4[0-9]|5[0-9]|[0-9](?!\d))",
        "/": r"(?:\.|:)",
    },
    "timezone": {
        "%z": r"(?:\+|\-)\d+:\d+",
    },
    "am_pm": {
        "%p": "(?:am|pm)",
    }
}

get_date_regex = partial(get_regex, "date", "/")
date_regex = {
    "%d/%m/%Y": get_date_regex("%d/%m/%Y"),
    "%m/%d/%Y": get_date_regex("%m/%d/%Y"),
    "%Y/%m/%d": get_date_regex("%Y/%m/%d"),
    "%b/%d/%Y": get_date_regex("%b/%d/%Y"),
    "%d/%b/%Y": get_date_regex("%d/%b/%Y"),
    "%d/%B/%Y": get_date_regex("%d/%B/%Y"),
    "%-d/%b/%Y": get_date_regex("%-d/%b/%Y"),
    "%-d/%-m/%Y": get_date_regex("%-d/%-m/%Y"),
    "%-m/%-d/%Y": get_date_regex("%-m/%-d/%Y"),
    "%Y/%-m/%-d": get_date_regex("%Y/%-m/%-d"),
    "%b/%-d/%Y": get_date_regex("%b/%-d/%Y"),
    "%B/%d//%Y": get_date_regex("%B/%d//%Y"),

    "%d/%m/%y": get_date_regex("%d/%m/%y"),
    "%m/%d/%y": get_date_regex("%m/%d/%y"),
    "%d/%b/%y": get_date_regex("%d/%b/%y"),
    "%d/%B/%y": get_date_regex("%d/%B/%y"),
    "%-d/%b/%y": get_date_regex("%-d/%b/%y"),
    "%-d/%-m/%y": get_date_regex("%-d/%-m/%y"),
    "%-m/%-d/%y": get_date_regex("%-m/%-d/%y"),
    "%b/%-d/%y": get_date_regex("%b/%-d/%y"),

    "%Y/%m": get_date_regex("%Y/%m"),
    "%b/%Y": get_date_regex("%b/%Y"),
    "%B/%Y": get_date_regex("%b/%Y"),

    "%Y": get_date_regex("%Y")
}

get_time_regex = partial(get_regex, "time", "/")
time_regex = {
    "%H/%M/%S/%f": get_time_regex("%H/%M/%S/%f"),
    "%-H/%-M/%-S/%f": get_time_regex("%-H/%-M/%-S/%f"),
    "%I/%M/%S/%f": get_time_regex("%I/%M/%S/%f"),
    "%H/%M:%S": get_time_regex("%H/%M/%S"),
    "%-H/%-M/%-S": get_time_regex("%-H/%-M/%-S"),
    "%I/%M:%S": get_time_regex("%I/%M/%S"),
    "%H/%M": get_time_regex("%H/%M"),
    "%-H/%-M": get_time_regex("%-H/%-M"),
    "%I/%M": get_time_regex("%I/%M")
}

get_am_pm_regex = partial(get_regex, "am_pm", None)
am_pm_regex = {
    "%p": get_am_pm_regex("%p")
}

get_timezone_regex = partial(get_regex, "timezone", None)
timezone_regex = {
    "%z": get_timezone_regex("%z"),
}

mapping = {
    "%d": "dd",
    "%-d": "d",
    "%m": "MM",
    "%-m": "M",
    "%b": "MMM",
    "%B": "MMMM",
    "%y": "yy",
    "%Y": "yyyy",
    "%H": "HH",
    "%-H": "H",
    "%M": "mm",
    "%-M": "m",
    "%f": "ffffff",
    "%S": "ss",
    "%-S": "s",
    "%z": "zzz",
    "%I": "h",
    "%p": "a"
}
display_name_regex = re.compile("|".join(map(re.escape, mapping.keys())))


def get_possible_formats(datetime, regex_mapping):
    """
    This function iterates through given mapping of possible regex and
    returns list of possible formats along with the matched string
    :param datetime:
    :param regex_mapping:
    :return: possible_formats, matched_string (tuple (list, str))
    """
    possible_formats = []
    matched_string = ""
    matched_string_len = 0
    for _format, regex in regex_mapping.items():
        regex = re.compile(regex)
        results = regex.findall(datetime)
        if results:
            possible_match = results[0]

            if len(possible_match) > matched_string_len:
                possible_formats = []
                matched_string = possible_match
                matched_string_len = len(matched_string)

            if len(possible_match) == matched_string_len:
                possible_formats.append(_format)

    return possible_formats, matched_string


def update_formats(formats, delimiters):
    """
    This function replaces generic format detected to user given
    string format
    Example:
        input: ['%d/%m/%Y %H/%M/%S/%f'] ['-','-','-',':',':','.']
        output: ['%d-%m-%Y %H:%M:%S.%f']
    Args:
        formats (list)
        delimiters (list)
    Output:
        formats (list)
    """
    for i, _format in enumerate(formats):
        for delimiter in delimiters:
            formats[i] = formats[i].replace("/", delimiter, 1)
    return formats


def update_date_formats(date_formats, detected, placeholder):
    """
    This function updated date placeholder with detected formats with proper delimiter.
    :param date_formats:
    :param detected:
    :param placeholder:
    :return:
    """
    date_delimiters = re.findall(r"\W", detected)
    date_formats = update_formats(date_formats, date_delimiters)
    date_updated_formats = [placeholder.replace("{DATE}", date_format) for date_format in date_formats]
    return date_updated_formats


def update_time_formats(time_formats, detected, placeholder):
    """
    This function updates time placeholder with detected formats with proper delimiter.
    :param time_formats:
    :param detected:
    :param placeholder:
    :return:
    """
    if time_formats:
        time_formats = [time_formats[0]]
    time_delimiters = re.findall(r"\W", detected)
    time_formats = update_formats(time_formats, time_delimiters)
    updated_time_formats = [placeholder.replace("{TIME}", time_format) for time_format in time_formats]
    return updated_time_formats


def update_am_pm_formats(am_pm_formats, _, placeholder):
    """
    This function replaces Am Pm placeholder
    :param am_pm_formats:
    :param _:
    :param placeholder:
    :return:
    """
    updated_am_pm_formats = [placeholder.replace("{AM_PM}", am_pm_format) for am_pm_format in am_pm_formats]
    return updated_am_pm_formats


def update_timezone_formats(timezone_formats, _, placeholder):
    """
    This function replaces Timezone placeholder with detected timezone
    :param timezone_formats:
    :param _:
    :param placeholder:
    :return:
    """
    updated_timezone_formats = [placeholder.replace("{TIMEZONE}", timezone_format) for timezone_format in
                                timezone_formats]
    return updated_timezone_formats


def stitch_formats(_, placeholder, data):
    """
    The possible formats are located in chunks
    this function stiches them as per given input string with proper delimiters
    :param _:
    :param placeholder:
    :param data:
    :return:
    """
    date = data.get("date")
    date_detected = date.get("detected")
    date_formats = date.get("formats")
    updated_date_formats = update_date_formats(date_formats, date_detected, placeholder)

    # TODO: check if placeholder pattern in updated format if not return if yes process
    final_formats = updated_date_formats

    time = data.get("time")
    time_detected = time.get("detected")
    time_formats = time.get("formats")

    updated_time_formats = []
    if time_detected:
        for date_format in updated_date_formats:
            updated_time_formats.extend(update_time_formats(time_formats, time_detected, date_format))
        final_formats = updated_time_formats

    am_pm = data.get("am_pm")
    am_pm_detected = am_pm.get("detected")
    am_pm_formats = am_pm.get("formats")
    updated_am_pm_formats = []
    if am_pm_detected:
        for time_format in updated_time_formats:
            updated_am_pm_formats.extend(update_am_pm_formats(am_pm_formats, am_pm_detected, time_format))
        final_formats = updated_am_pm_formats

    timezone = data.get("timezone")
    timezone_detected = timezone.get("detected")
    timezone_formats = timezone.get("formats")
    updated_timezone_formats = []
    if timezone_detected:
        for am_pm_format in updated_time_formats:
            updated_timezone_formats.extend(update_timezone_formats(timezone_formats, timezone_detected, am_pm_format))
        final_formats = updated_timezone_formats

    return final_formats


def get_display_name(_format, _mapping, display_name_regex):
    """
    This function returns display name of python format strings
    e.g: %I -> H, %H -> HH
    :param _format:
    :param _mapping:
    :param display_name_regex:
    :return:
    """
    return display_name_regex.sub(lambda match: _mapping[match.group(0)], _format)


def get_possible_datetime_format_codes(datetime):
    """
    This function returns list of possible python date format codes of given string with common delimiter /.
    :param datetime: string
    :return:
    """
    datetime = datetime.lower()
    datetime_original = datetime
    timezone_formats, timezone = get_possible_formats(datetime, timezone_regex)
    datetime = datetime.replace(timezone, "{TIMEZONE}") if timezone else datetime
    time_formats, time = get_possible_formats(datetime, time_regex)
    datetime = datetime.replace(time, "{TIME}") if time else datetime
    am_pm_formats, am_pm = get_possible_formats(datetime, am_pm_regex)
    datetime = datetime.replace(am_pm, "{AM_PM}") if am_pm else datetime
    date_formats, date = get_possible_formats(datetime, date_regex)
    datetime = datetime.replace(date, "{DATE}") if date else datetime

    stitch_payload = {
        "date": {
            "detected": date,
            "formats": date_formats,
        },
        "time": {
            "detected": time,
            "formats": time_formats,
        },
        "am_pm": {
            "detected": am_pm,
            "formats": am_pm_formats,
        },
        "timezone": {
            "detected": timezone,
            "formats": timezone_formats,
        },
    }
    stitched_formats = stitch_formats(datetime_original, datetime, stitch_payload)
    return stitched_formats


def get_possible_datetimes_format_codes(datetimes, verbose):
    """
    Get possible datetimes formats takes sample list of strings
    and matches with supported regex of dates and returns matched cases
    at the output user will get dictionary with possible formats as keys
    and its count as value

    Args:
        datetimes (list)
        verbose
    Output:
        possible_formats_count (dict)
        verbose (bool)
    """
    possible_formats_count = {}
    for datetime in datetimes:
        possible_formats = get_possible_datetime_format_codes(datetime)
        for possible_format in possible_formats:
            if possible_format not in possible_formats_count:
                possible_formats_count[possible_format] = 1
            else:
                possible_formats_count[possible_format] += 1

    if not verbose:
        max_count = max(set(list(possible_formats_count.values()))) if possible_formats_count else 0
        possible_formats = [_format for _format, count in possible_formats_count.items() if count == max_count]
        return possible_formats

    possible_formats_list = list(possible_formats_count.items())
    possible_formats_list.sort(key=operator.itemgetter(1), reverse=True)
    sorted_possible_formats = []
    for _format, count in possible_formats_list:
        sorted_possible_formats.append({
            "format": _format,
            "display_name": get_display_name(_format, mapping, display_name_regex),
            "count": count,
        })
    return sorted_possible_formats


def get_format_codes(user_input, verbose=False):
    if isinstance(user_input, list):
        datetimes = user_input
    elif isinstance(user_input, str):
        datetimes = [user_input]
    else:
        raise InvalidArguments("Please provide string or list as input.")
    result = get_possible_datetimes_format_codes(datetimes, verbose)
    return result


if __name__ == "__main__":
    test = get_format_codes(['2012-12-18'], verbose=True)
    print(test)
