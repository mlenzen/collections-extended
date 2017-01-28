from abc import ABCMeta, abstractmethod
from datetime import date, datetime, timedelta

class FixedInterval():



class Hour(FixedInterval):

	@property
	def delta(cls):
		return timedelta(hours=1)
