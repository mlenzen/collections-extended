"""An Interval is a length of time.

An instance if Interval is a specific length of time. Classes of
"""
from abc import ABCMeta, abstractmethod
import calendar
from datetime import date, datetime, timedelta


class Interval(meta=ABCMeta):
	"""A length of time."""

	def __init__(self, beg):
		self._beg = beg

	@property
	def beg(self):
		return self._beg

	@property
	def end(self):
		return self.beg + self.delta

	@property
	@abstractmethod
	def delta(self):
		raise NotImplementedError()

	@property
	def tzinfo(self):
		return self.beg.tzinfo

	def next(self):
		return self.beginning(self.end)

	def prev(self):
		return self.ending(self.beg)

	def pace(self, dt=None):
		"""Return how far through this month d is.

		If d isn't passed use datetime.now()
		"""
		if dt is None:
			raise NotImplementedError('Need to get a tz aware datetime if self has tzinfo')
			d = datetime.now()
		if dt < self.beg:
			return 0.0
		elif dt > self.end:
			return 1.0
		else:
			return (dt - self.start) / self.delta

	# Classmethods

	@classmethod
	@abstractmethod
	def beginning(cls, beg):
		"""Return a TimeSpan of this Interval beginning on `beg`."""
		raise NotImplementedError()

	@classmethod
	@abstractmethod
	def ending(cls, end):
		"""Return a TimeSpan of this Interval ending on `end`."""
		raise NotImplementedError()


class _FixedMeta(ABCMeta):

	@property
	@abstractmethod
	def delta(self):
		raise NotImplementedError()


class FixedInterval(Interval, meta=_FixedMeta):
	"""A Interval of a fixed length."""

	@classmethod
	def beginning(cls, beg):
		return cls(beg)

	@classmethod
	def ending(cls, end):
		return cls(end - cls.delta)

	@classmethod
	def __div__(cls, other):
		return cls(cls.delta / other)

	@staticmethod
	def factory(td):

		class _cls(FixedInterval):
			delta = td

		return _cls


class ProperInterval(Interval, meta=ABCMeta):
	"""A Interval representing a span on a clock or calendar, eg. a month or hour.

	This is in contrast to a Interval starting at an abitrary point time.
	1:00-2:00 can be a ProperInterval while 1:14-2:14 cannot.
	"""

	@classmethod
	@abstractmethod
	def containing(self, dt):
		"""Return the instance of this Interval containing passed datetime."""
		raise NotImplementedError()


# Specifics


class Day(ProperInterval, FixedInterval):

	@property
	def delta


Century = ProperInterval()
Decade = ProperInterval()
Year = ProperInterval()
Quarter = ProperInterval()
# Month = ProperInterval()
Week = ProperInterval()
Day = ProperInterval()
Hour = ProperInterval()
Minute = ProperInterval()
Second = ProperInterval()
Microsecond = ProperInterval()
Millisecond = ProperInterval()


class Month(ProperInterval):

	def __init__(self, year, month, tzinfo=None):
		super().__init__(tzinfo)
		if not 0 < month <= 12:
			raise ValueError('Invalid month')
		self._year = int(year)
		self._month = int(month)

	@property
	def year(self):
		return self._year

	@property
	def month(self):
		return self._month

	@property
	def beg(self):
		return self.datetime(1, tzinfo=self.tzinfo)

	@property
	def end(self):
		return self.datetime(self.num_days(), tzinfo=self.tzinfo)

	@property
	def delta(self):
		return timedelta(days=self.num_days())

	@classmethod
	def containing(cls, d):
		return cls(d.year, d.month, d.tzinfo)

	def num_days(self):
		return calendar.monthrange(self.year, self.month)[1]

	def date(self, day):
		"""Return a date for the day of the month.

		num can be a negative number to count back from the end of the month.
		eg. date(-1) is the last day of the month.
		"""
		if day < 0:
			day += self.num_days() + 1
		return date(self.year, self.month, day)

	def datetime(self, day, *args, **kwargs):
		return datetime(self.year, self.month, day, *args, **kwargs)

	def next(self):
		if self.month == 12:
			return Month(self.year + 1, 1, self.tzinfo)
		else:
			return Month(self.year, self.month + 1, self.tzinfo)

	def __eq__(self, other):
		if isinstance(other, Month):
			return (self.year, self.month) == (other.year, other.month)
		else:
			return False

	def __lt__(self, other):
		if isinstance(other, Month):
			return (self.year, self.month) < (other.year, other.month)
		else:
			return NotImplemented

	def __sub__(self, other):
		"""Return the number of months between two months."""
		# TODO should this return an integer?
		return 12 * (self.year - other.year) + self.month - other.month

	def dates(self):
		"""Generate the dates in this month."""
		for i in range(self.num_days()):
			yield self.date(i + 1)


class Week(ProperFixedInterval):

	@property
	def delta(self):
		return timedelta(weeks=1)

	@classmethod
	def containing(cls, dt, weekstart=calendar.MONDAY):
		beg = dt.replace(hour=0, minute=0, second=0, microsecond=0)
		days = (dt.weekday() + 7 - weekstart) % 7
		dt -= timedelta(days=days)
		return TimeSpan(beg, cls)


class Day(ProperFixedInterval):

	@property
	def delta(self):
		return timedelta(days=1)

	@classmethod
	def containing(cls, dt):
		beg = dt.replace(hour=0, minute=0, second=0, microsecond=0)
		return TimeSpan(beg, cls)
