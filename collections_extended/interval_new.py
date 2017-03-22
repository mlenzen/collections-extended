from abc import ABCMeta, abstractmethod
import calendar
from datetime import datetime, date, timedelta, tzinfo

# TODO handle tzinfo on Year, Quarter & Month
# TODO multiply a FixedIntervalType to get a new one


class Interval():
	"""An Interval is a specific timespan, with fixed beginning and end datetimes.

	At least 2 of beg, end and delta must be passed to determine the interval.
	If all 3 are passed, then `end - beg == delta`.

	Args:
		beg: The start of the interval, inclusive.
		end: The end of the interval, exclusive.
		delta: The length of the interval.
	"""

	def __init__(
			self,
			beg: datetime = None,
			end: datetime = None,
			delta: timedelta = None,
			):
		if beg:
			self._beg = beg
			if delta:
				self._delta = delta
				if end and self.end != end:
					raise ValueError('delta != end - beg')
			else:
				if not end:
					raise ValueError('Must pass at least 2 of beg, end & delta')
				self._delta = end - beg
		else:
			if not end and delta:
				raise ValueError('Must pass at least 2 of beg, end & delta')
			self._beg = end - delta
			self._delta = delta

	@property
	def beg(self) -> datetime:
		return self._beg

	@property
	def end(self) -> datetime:
		return self.beg + self.delta

	@property
	def delta(self) -> timedelta:
		return self._delta

	@property
	def tzinfo(self) -> tzinfo:
		return self.beg.tzinfo

	def __contains__(self, d: datetime):
		return self.beg <= d < self.end

	def __eq__(self, other):
		if not isinstance(other, Interval):
			return False
		return (self.beg, self.end) == (other.beg, other.end)

	def pace(self, dt=None) -> float:
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

	def divide(self, interval_type, extras_action='raise'):
		"""

		extras_action can be 'raise', 'ignore', or 'partial'
		'raise' - raise an Exception if the passed IntervalType does not evenly
			divide this Interval.
		'ignore' - ignore parts of this Interval to divide self into subintervals
			of interval_type
		'partial' - return partial intervals not matching interval_type where
			necessary
		"""
		# TODO
		raise NotImplementedError


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

	def __lt__(self, other):
		if not isinstance(other, type(self)):
			return NotImplemented
		return self.beg < other.beg

	def next(self):
		return self.beginning(self.end)

	def prev(self):
		# TODO infinite recursion with ending
		return self.ending(self.beg)

	@classmethod
	def first_after(cls, dt: datetime):
		"""Return the first ProperInterval following datetime."""
		return cls.containing(dt).next()

	@classmethod
	def last_before(cls, dt: datetime):
		"""Return last ProperInterval before datetime."""
		return cls.containing(dt).prev()


class Year(ProperInterval):

	def __init__(self, year: int, tzinfo: tzinfo = None):
		self._year = year
		self._tzinfo = tzinfo

	def __str__(self):
		return str(self.year)

	@property
	def year(self) -> int:
		return self._year

	@property
	def tzinfo(self) -> tzinfo:
		return self._tzinfo

	@property
	def beg(self) -> datetime:
		return datetime(self.year, 1, 1, tzinfo=self.tzinfo)

	@property
	def end(self) -> datetime:
		return datetime(self.year + 1, 1, 1, tzinfo=self.tzinfo)

	@property
	def delta(self) -> timedelta:
		return self.end - self.beg

	@classmethod
	def containing(cls, d: date):
		if isinstance(d, datetime):
			tzinfo = d.tzinfo
		else:
			tzinfo = None
		return cls(d.year, tzinfo=tzinfo)

	def isleap(self):
		return calendar.isleap(self.year)

	def date(self, month, day):
		return date(self.year, month, day)

	def datetime(self, *args, **kwargs):
		if 'tzinfo' not in kwargs:
			kwargs['tzinfo'] = self.tzinfo
		return datetime(self.year, *args, **kwargs)


class Quarter(ProperInterval):

	def __init__(self, year: int, quarter: int, tzinfo: tzinfo = None):
		if not (1 <= quarter <= 4):
			raise ValueError
		self._year = year
		self._quarter = quarter
		self._tzinfo = tzinfo

	def __str__(self):
		return '{self.year}-Q{self.quarter}'.format(self=self)

	@property
	def year(self) -> int:
		return self._year

	@property
	def quarter(self) -> int:
		return self._quarter

	@property
	def tzinfo(self) -> tzinfo:
		return self._tzinfo

	@property
	def beg(self) -> datetime:
		month = (self.quarter - 1) * 3 + 1
		return datetime(self.year, month, 1, tzinfo=self.tzinfo)

	@property
	def end(self) -> datetime:
		if self.quarter == 4:
			year = self.year + 1
			month = 1
		else:
			year = self.year
			month = self.quarter * 3 + 1
		return datetime(year, month, tzinfo=self.tzinfo)

	@property
	def delta(self) -> timedelta:
		return self.end - self.beg

	@classmethod
	def containing(cls, d: date):
		if isinstance(d, datetime):
			tzinfo = d.tzinfo
		else:
			tzinfo = None
		quarter = d.month // 3 + 1
		return cls(d.year, quarter, tzinfo=tzinfo)


class Month(ProperInterval):

	def __init__(self, year: int, month: int, tzinfo: tzinfo = None):
		if not (1 <= month <= 12):
			raise ValueError
		self._year = year
		self._month = month
		self._tzinfo = tzinfo

	@property
	def year(self) -> int:
		return self._year

	@property
	def month(self) -> int:
		return self._month

	@property
	def tzinfo(self) -> tzinfo:
		return self._tzinfo

	@property
	def beg(self) -> datetime:
		return datetime(self.year, self.month, 1, tzinfo=self.tzinfo)

	@property
	def end(self) -> datetime:
		# return self.beg + self.delta
		if self.month == 12:
			year = self.year + 1
			month = 1
		else:
			year = self.year
			month = self.month + 1
		return datetime(year, month, tzinfo=self.tzinfo)

	@property
	def delta(self):
		return timedelta(days=self.num_days())

	def num_days(self):
		return calendar.monthrange(self.year, self.month)[1]

	@classmethod
	def containing(cls, d: date):
		if isinstance(d, datetime):
			tzinfo = d.tzinfo
		else:
			tzinfo = None
		return cls(d.year, d.month, tzinfo=tzinfo)

	def name(self):
		# TODO
		raise NotImplementedError

	def abbr(self):
		# TODO
		raise NotImplementedError


class FixedIntervalType(ABCMeta):

	@property
	@abstractmethod
	def delta(self) -> timedelta:
		raise NotImplementedError()


class FixedInterval(Interval, metaclass=FixedIntervalType):
	"""A Interval of a fixed length."""

	def __init__(self, beg: datetime):
		self._beg = beg

	@property
	def end(self) -> datetime:
		return self.beg + self.delta

	def next(self):
		return self.beginning(self.end)

	def prev(self):
		return self.ending(self.beg)

	@classmethod
	def beginning(cls, d: datetime):
		"""Return the instance of this class beginning at datetime d."""
		return cls(d)

	@classmethod
	def ending(cls, d: datetime):
		"""Return the instance of this class ending at datetime d."""
		return cls(d - cls.delta)

	@classmethod
	def create(cls, td: timedelta):
		print('hello')
		return type('CustomInterval', (cls, ), {'delta': td})


class Week(ProperInterval, FixedInterval):

	delta = timedelta(days=7)

	@classmethod
	def containing(cls, d: date, starts_on: int = None):
		if not starts_on:
			starts_on = calendar.firstweekday()
		if isinstance(d, datetime):
			d = d.date()
		days = (d.weekday() + 7 - starts_on) % 7
		d -= timedelta(days=days)
		return cls(d)


class Day(ProperInterval, FixedInterval):

	delta = timedelta(days=1)

	@classmethod
	def containing(cls, d: date):
		d = datetime(d.year, d.month, d.day)
		return cls(d)

	def name(self):
		# TODO
		raise NotImplementedError

	def abbr(self):
		# TODO
		raise NotImplementedError


class Hour(ProperInterval, FixedInterval):

	delta = timedelta(hours=1)

	@classmethod
	def containing(cls, dt: datetime):
		dt = dt.replace(minute=0, second=0, microsecond=0)
		return cls(dt)


class Minute(ProperInterval, FixedInterval):

	delta = timedelta(minutes=1)

	@classmethod
	def containing(cls, dt: datetime):
		dt = dt.replace(second=0, microsecond=0)
		return cls(dt)


class Second(ProperInterval, FixedInterval):

	delta = timedelta(seconds=1)

	@classmethod
	def containing(cls, dt: datetime):
		dt = dt.replace(microsecond=0)
		return cls(dt)


class MilliSecond(ProperInterval, FixedInterval):

	delta = timedelta(microseconds=1000)

	@classmethod
	def containing(cls, dt: datetime):
		microsecond = round(dt.microsecond, -3)
		dt = dt.replace(microsecond=microsecond)
		return cls(dt)


class MicroSecond(ProperInterval, FixedInterval):

	delta = timedelta(microseconds=1)

	@classmethod
	def containing(cls, dt: datetime):
		return cls(dt)
