import sys 
import datetime
import string 
import re
from pprint import pprint
from dateparser import search
from nltk.tokenize import word_tokenize, sent_tokenize
from enum import Enum
from calendar import month_name
from .EventDate import EventDate

def get_event_date(text, date):
	article_date = datetime.datetime.strptime(date, r'%Y-%m-%d')

	sentences = [k for k, v in get_relevant_sentences(text, article_date)]

	# For each sentence, grab dates
	event_dates = []
	for sentence in sentences:
		# Prepare for parsing
		sentence = add_helper_words(sentence)
		date_strings = filter_sentence_to_dates(sentence, article_date.year)

		# Use dateparser parsing 
		event_dates += parse_dates(date_strings, article_date)

	# print(list(map(lambda x: x.to_string(), event_dates)))
	date_string = generate_date_range(event_dates, article_date)
	# print(date_string)
	return date_string

# Get sentences that have relevant case information
def get_relevant_sentences(text, article_date):
	sentences = {s: 0 for s in preprocess_sentences(sent_tokenize(text))}

	# Rank each sentence
	for sentence in sentences.keys(): 
		sentences[sentence] = rank_sentence(sentence, article_date)

	# pprint(sentences)
	result = list(filter(lambda x: x[1][0] >= 100, sentences.items()))
	if len(result) == 0: 
		result = list(filter(lambda x: x[1][1], sentences.items()))
		result.sort(key=lambda x: x[1][0], reverse=True)
		# pprint(result)
		result = result[:1]
	return result


def preprocess_sentences(sentences):
	pattern = re.compile(r"(\d+)-(\d+)")
	def repl(obj):
		return obj.group(1) + " – " + obj.group(2)

	return [re.sub(pattern, repl, sentence) for sentence in sentences]


month_number = {v: int(k) + 1 for k, v in enumerate(month_name[1:])}
# Give a rank/score to sentence
def rank_sentence(sentence, article_date):
	words = word_tokenize(sentence)
	words = list(filter(lambda token: token not in string.punctuation, words))
	
	running_score = 0

	# Check if dates exist 
	curr_month = article_date.month
	curr_year = article_date.year
	found_month = False 
	for index, word in enumerate(words):
		# Check month/date existence and recency 
		if word in month_name[1:]: # First element is empty string 
			found_month = True 
			month_num = month_number[word]
			recency = (month_num - curr_month + 11) % 12 # 11 = most recent, 0 = least 
			if recency > 7:
				running_score += 40
			elif recency > 6: 
				running_score += 20 
			else: 
				running_score -= 200
			
			# Check if year follows the month 
			if index + 1 < len(words):
				next_word = words[index + 1]
				try: 
					next_num = int(next_word)
					if next_num == curr_year or (curr_month < 3 and next_num == curr_year - 1): 
						running_score += 30
					elif next_num > 1990 and next_num < curr_year:
						running_score -= 500
				except:
					pass 
		if word.isdigit():
			num = int(word)
			if num > 1990 and num < curr_year and curr_month >= 3:
				running_score -= 500
	running_score += 30 if found_month else -200
	
	# Check if keywords exist
	words = [word.lower() for word in words]
	scores = {
		"case": 60,
		"cases": 60,
		"outbreak": 50,
		"confirmed": 40,
		"confirm": 40,
		"reported": 50, 
		"notified": 30,
		"occurred": 20, 
		"new": 60, 
		"additional": 40,
		"first": 50,
		"second": 50, 
		"year-old": 60, 
		"male": 40, 
		"males": 30,
		"female": 40,
		"females": 30,
		"developed": 30, 
		"hospitalized": 30, 
		"experienced": 30,
		"total": -140,
		"administered": -50,
		"lower": -100
	}
	keywords = list(scores.keys())
	for keyword in keywords: 
		if keyword in words: 
			running_score += scores[keyword]

	# Penalise if absent 
	absent = [
		"case",
		"cases",
		"outbreak",
		"occurred",
		"hospitalized"
	]
	exists = False
	for word in absent:
		if word in words:
			exists = True 
			break 
	if not exists:
		running_score -= 90
	return running_score, found_month, exists

# For helping the dateparser module extract dates 
# Expects an array of word strings
def add_helper_words(sentence):
	special_words = [
		"–",
		"to",
		"through",
		"and"
	]
	words = word_tokenize(sentence)
	def filter_punctuation(token):
		return token not in string.punctuation or token is "-"
	words = list(filter(filter_punctuation, words))

	for i, word in enumerate(words):
		if word.isdigit():
			# Check special word 
			cond0 = i < len(words) - 1 and words[i+1].lower() in special_words
			
			# Check 2 words after for 'number'
			cond1 = i < len(words) - 2 and words[i+2].isdigit()
			
			# Check 3 words after for month 
			month_names = [month for month in month_name[1:]]
			cond2 = i < len(words) - 3 and words[i+3] in month_names

			if cond0 and cond1 and cond2: 
				# Insert month 
				month = words[i+3]
				words.insert(i+1, month)
		
		if word in month_name[1:]:
			cond0 = i < len(words) - 1 and words[i+1].lower () in special_words
			cond1 = i < len(words) - 2 and words[i+2] in month_name[1:]
			cond2 = i < len(words) - 3 and words[i+3].isdigit() #and int(words[i+3]) > 1990
			if cond0 and cond1 and cond2:
				year = words[i+3]
				words.insert(i+1, year)

	return ' '.join(words)

def filter_sentence_to_dates(sentence, article_year):
	words = word_tokenize(sentence)
	words = list(filter(lambda token: token not in [','], words))

	def good_day(day, month): 
		if not day.isdigit(): 
			return False 
		day = int(day)
		day_count = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		return day > 0 and day <= day_count[month_number[month]]

	def good_year(year):
		if not year.isdigit():
			return False 
		year = int(year)
		return year >= 1990 and year <= article_year

	date_strings = []
	for i, word in enumerate(words):
		# Assuming relevant dates will always have month in name 
		if word in month_name[1:]:
			# day month year 
			if i > 0 and good_day(words[i-1], word) and i+1 < len(words) and good_year(words[i+1]):
				lower, upper = i-1, i+1

			# month year
			elif i+1 < len(words) and good_year(words[i+1]):
				lower, upper = i, i+1

			# day month 
			elif i > 0 and good_day(words[i-1], word):
				lower, upper = i-1, i

			# month day year
			elif i+2 < len(words) and good_day(words[i+1], word) and good_year(words[i+2]):
				lower, upper = i, i+2			

			# month day
			elif i+1 < len(words) and good_day(words[i+1], word):
				lower, upper = i, i+1
			else: 
				lower, upper = i, i
			# lower = i-1 if i > 0  and good_day(words[i-1], word) else i
			# upper  = i+1 if i+1 < len(words) and good_year(words[i+1]) else i
			date_strings.append(' '.join(words[lower:(upper+1)]))
	# print(words, date_strings)
	return date_strings

# Array of date strings 
def parse_dates(date_strings, article_date):
	settings = {
		'RELATIVE_BASE': article_date,
		'PREFER_DATES_FROM': 'past'
	}

	event_dates = []
	for date_string in date_strings:
		results = search.search_dates(date_string, settings=settings)
		for result in results:
			event_dates.append(decompose_date(result[0], result[1]))
	
	return event_dates 

def decompose_date(date_string, date):
	components = date_string.split()
	event_date = EventDate()
	
	if str(date.year) in components:
		components.remove(str(date.year))
	event_date.year = date.year

	# Month should always be in components
	components.remove(month_name[date.month])
	event_date.month = date.month 

	# Last remaining component (if applicable) should be day
	if str(date.day) in components: 
		event_date.day = date.day 

	return event_date

def generate_date_range(event_dates, article_date):
	if len(event_dates) == 0:
		return "%d-%02d-%02d xx:xx:xx" % (article_date.year, article_date.month, article_date.day)

	lower = None
	upper = None 

	for event_date in event_dates: 
		if lower is None and upper is None: 
			lower = event_date
			upper = event_date
			continue 
		if event_date.less_than(lower):
			lower = event_date
		if event_date.greater_than(upper):
			upper = event_date
	
	if lower.to_string() == upper.to_string(): 
		return lower.to_string()
	else:
		return "%s to %s" % (lower.to_string(), upper.to_string())

if __name__ == "__main__":
	if len(sys.argv) < 4:
		pass
	elif len(sys.argv) == 4: 
		with open('example.txt') as f: 
			contents = f.read().replace('\n', ' ').replace('\r', ' ')
			get_event_date(contents,  "%s-%s-%s" % (sys.argv[1], sys.argv[2], sys.argv[3]))
	else: 
		get_event_date(sys.argv[1], "%s-%s-%s" % (sys.argv[2], sys.argv[3], sys.argv[4]))