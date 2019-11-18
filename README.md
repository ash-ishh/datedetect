### datedetect

Get possible string format codes of the given datetime object.

Supports Python 3.6+.

````python
>>> import datedetect

>>> datedetect.get_format_codes("1997-11-04 12:00:00.123456+5:30")
['%Y-%m-%d %H:%M:%S.%f%z']

>>> datedetect.get_format_codes(["1997-11-04 12:00:00.123456+5:30"], verbose=True)
# verbose True for display name and count of matches
[{'format': '%Y-%m-%d %H:%M:%S.%f%z', 'display_name': 'yyyy-MM-dd HH:mm:ss.ffffffzzz', 'count': 1}]

>>> datedetect.get_format_codes(["10-10-2019", "10-12-2019", "21-1-2019"], verbose=True)
# first two can be both dd-MM-yyyy, MM-dd-yyyy, d-M-yyyy, M-d-yyyy
# second can be dd-MM-yyyy d-M-yyyy MM-dd-yyyy M-dd-yyyy
# third one is d-M-yyyy
[{'format': '%-d-%-m-%Y', 'display_name': 'd-M-yyyy', 'count': 3},
 {'format': '%d-%m-%Y', 'display_name': 'dd-MM-yyyy', 'count': 2},
 {'format': '%m-%d-%Y', 'display_name': 'MM-dd-yyyy', 'count': 2},
 {'format': '%-m-%-d-%Y', 'display_name': 'M-d-yyyy', 'count': 2}]
````

