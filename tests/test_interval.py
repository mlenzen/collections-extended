from datetime import date, datetime

import pytest

from collections_extended.interval import Month, Week, Day


def test_containing():
	assert Month.containing(date(2016, 5, 23)) == Month(year=2016, month=5)
	assert Day.containing(datetime(2016, 5, 23, 12, 0, 0)) == Day(2016, 5, 23)


def test_starting():
	pass


def test_divide():
	pass
