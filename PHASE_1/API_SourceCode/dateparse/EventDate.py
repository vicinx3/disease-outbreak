
# Private class
# Year, month assumed to always exist, day is a maybe
class EventDate():
	def __init__(self):
		self._year = None 
		self._month = None
		self._day = None 

	@property 
	def year(self):
		return self._year 

	@year.setter
	def year(self, value):
		self._year = int(value)

	@property 
	def month(self):
		return self._month 

	@month.setter
	def month(self, value):
		month = int(value) 
		if month < 1 or month > 12:
			raise ValueError()
		self._month = month

	@property 
	def day(self):
		return self._day
	
	@day.setter
	def day(self, value):
		day = int(value)
		if day < 1 or day > 31: 
			raise ValueError()
		self._day = day

	# Return string representation
	def to_string(self):
		def custom_str(value):
			return "%02d" % value if value is not None else "xx"

		(year, month, day) = map(custom_str, [self.year, self.month, self.day])
		return "%s-%s-%s xx:xx:xx" % (year, month, day)


	# Comparison functions
	# Assumes 'other' is of same class
	def less_than(self, other):
		if self.year < other.year: 
			return True 
		elif self.year == other.year:
			if self.month < other.month:
				return True 
			elif self.month == other.month:
				if self.day is None: 
					return False
				elif other.day is None:
					return True # The more 'certain' option
				elif self.day < other.day:
					return True 
		return False

	def greater_than(self, other):
		if self.year > other.year:
			return True 
		elif self.year == other.year: 
			if self.month > other.month:
				return True 
			elif self.month == other.month:
				if self.day is None: 
					return False
				elif other.day is None:
					return True
				elif self.day > other.day:
					return True
		return False