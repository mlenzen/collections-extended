from abc import ABCMeta, abstractmethod
import calendar
from datetime import datetime, date, time, timedelta


class Interval():
	"""An Interval is a specific timespan, with fixed beginning and end datetimes.

	Args:
		beg: The start of the interval, inclusive.
		end: The end of the interval, exclusive.
	"""

	def __init__(self, beg, end):
		self._beg = beg
		self._delta = end - beg

	@property
	def beg(self):
		return self._beg

	@property
	def end(self):
		return self._beg + self._delta

	@property
	def delta(self):
		return self._delta

	@property
	def tzinfo(self):
		return self.beg.tzinfo

	def __contains__(self, d: datetime):
		return self.beg <= d < self.end

	def pace(self, dt=None):
		"""Return how far through this interval dt is.

		If dt isn't passed use datetime.now()
		"""
		if dt is None:
			dt = datetime.now(self.tzinfo)
		if dt < self.beg:
			return 0.0
		elif dt > self.end:
			return 1.0
		else:
			return (dt - self.start) / self.delta


class ProperInterval(Interval, metaclass=ABCMeta):
	"""A Interval representing a span on a clock or calendar, eg. a month or hour.

	This is in contrast to a Interval starting at an abitrary point time.
	1:00-2:00 can be a ProperInterval while 1:14-2:14 cannot.
	"""

	@classmethod
	@abstractmethod
	def containing(cls, d: datetime):
		"""Return the instance of this class containing datetime d."""
		raise NotImplementedError

	@classmethod
	def beginning(cls, d: datetime):
		"""Return the instance of this class beginning at datetime d."""
		interval = cls.containing(d)
		if interval.beg != d:
			raise ValueError('d is not the beggining of a {cls}'.format(cls=cls))
		return interval

	@classmethod
	def ending(cls, d: datetime):
		"""Return the instance of this class ending at datetime d."""
		# TODO infinite recursion with prev
		return cls.beginning(d).prev()

	def next(self):
		return self.beginning(self.end)

	def prev(self):
		# TODO infinite recursion with ending
		return self.ending(self.beg)


class Year(ProperInterval):

	def __init__(self, year: int):
		self._year = year

	def __str__(self):
		return str(self.year)

	@property
	def year(self):
		return self._year

	@property
	def beg(self):
		return datetime(self.year, 1, 1)

	@property
	def end(self):
		return datetime(self.year + 1, 1, 1)

	@classmethod
	def containing(cls, d: date):
		return cls(d.year)


class Quarter(ProperInterval):

	def __init__(self, year: int, quarter: int):
		if not (1 <= quarter <= 4):
			raise ValueError
		self._year = year
		self._quarter = quarter

	def __str__(self):
		return '{self.year}-Q{self.quarter}'.format(self=self)

	@property
	def year(self):
		return self._year

	@property
	def quarter(self):
		return self._quarter

	@property
	def beg(self):
		month = (self.quarter - 1) * 3 + 1
		return datetime(self.year, month, 1)

	@property
	def end(self):
		if self.quarter == 4:
			year = self.year + 1
			month = 1
		else:
			year = self.year
			month = self.quarter * 3 + 1
		return datetime(year, month)

	@classmethod
	def containing(cls, d: date):
		quarter = d.month // 3 + 1
		return cls(d.year, quarter)


class Month(ProperInterval):

	def __init__(self, year: int, month: int):
		if not (1 <= month <= 12):
			raise ValueError
		self._year = year
		self._month = month

	@property
	def year(self):
		return self._year

	@property
	def month(self):
		return self._month

	@property
	def beg(self):
		return datetime(self.year, self.month, 1)

	@property
	def end(self):
		if self.month == 12:
			year = self.year + 1
			month = 1
		else:
			year = self.year
			month = self.month + 1
		return datetime(year, month)

	# @property
	# def delta(self):
	# 	return timedelta(days=self.num_days())
	#
	# def num_days(self):
	# 	return calendar.monthrange(self.year, self.month)[1]

	@classmethod
	def containing(cls, d: date):
		return cls(d.year, d.month)


class _FixedMeta(ABCMeta):

	@property
	@abstractmethod
	def delta(self):
		raise NotImplementedError()


class FixedInterval(Interval, metaclass=_FixedMeta):
	"""A Interval of a fixed length."""

	def __init__(self, beg: datetime):
		self._beg = beg

	@property
	def end(self):
		return self.beg + self.delta


class Week(FixedInterval, ProperInterval):

	delta = timedelta(days=7)

	@classmethod
	def containing(cls, d: date, starts_on=None):
		if not starts_on:
			starts_on = calendar.firstweekday()
		if isinstance(d, datetime):
			d = d.date()
		days = (d.weekday() + 7 - starts_on) % 7
		d -= timedelta(days=days)
		return cls(d)


class Day(FixedInterval, ProperInterval):

	delta = timedelta(days=1)

	@classmethod
	def containing(cls, d: date):
		d = datetime(d.year, d.month, d.day)
		return cls(d)


class Hour(FixedInterval, ProperInterval):

	delta = timedelta(hours=1)

	@classmethod
	def containing(cls, d: datetime):
		d = d.replace(minute=0, second=0, microsecond=0)
		return cls(d)


class Minute(FixedInterval, ProperInterval):

	delta = timedelta(minutes=1)

	@classmethod
	def containing(cls, d: datetime):
		d = d.replace(second=0, microsecond=0)
		return cls(d)


class Second(FixedInterval, ProperInterval):

	delta = timedelta(seconds=1)

	@classmethod
	def containing(cls, d: datetime):
		d = d.replace(microsecond=0)
		return cls(d)


class MilliSecond(FixedInterval, ProperInterval):

	delta = timedelta(microseconds=1000)

	@classmethod
	def containing(cls, d: datetime):
		microsecond = round(d.microsecond, -3)
		d = d.replace(microsecond=microsecond)
		return cls(d)


class MicroSecond(FixedInterval, ProperInterval):

	delta = timedelta(microseconds=1)

	@classmethod
	def containing(cls, d: datetime):
		return cls(d)
