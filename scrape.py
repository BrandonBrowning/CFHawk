
import re
import urllib2
from datetime import datetime
from lxml import etree

class Problem:
	def __init__(self, problemid=None, urlid=None, name=None):
		self.problemid = problemid
		self.urlid = urlid # (123, B)
		self.name = name

	@property
	def url(self):
		return "http://codeforces.com/problemset/problem/{0}/{1}".format(self.urlid[0], self.urlid[1])

	@property
	def urlname(self):
		return "{0}{1}".format(self.urlid[0], self.urlid[1]) if self.urlid else ""

class Submission:
	def __init__(self):
		self.submissionid = None
		self.date = None
		self.problem = None
		self.language = None
		self.verdict = None
		self.time = None # ms
		self.memory = None # KB

class StudentWeek:
	def __init__(self, name=None, correct=[], participantid=None):
		self.name = name
		self.correct = correct
		self.participantid = participantid

	@property
	def url(self):
		return "http://codeforces.com/profile/{0}".format(self.name)

def extract_string(tree, xpath_query):
	results = tree.xpath(xpath_query)
	if results:
		return results[0].strip()
	else:
		return None

def serialize_verdict(verdict_text):
	if verdict_text is None:
		return None
	elif verdict_text == 'verdict-accepted':
		return 'Accepted'
	elif verdict_text == 'verdict-rejected':
		return 'Rejected'
	elif verdict_text == 'Compilation error':
		return 'Compilation Error'
	else:
		raise ValueError('Given verdict not known ({0})'.format(verdict_text))

def extract_problem_urlid_and_name(problem_title):
	match = re.search('^(\d+)(\w) - (.*)$', problem_title)
	if not match:
		return (None, None)
	else:
		groups = match.groups()

		if len(groups) == 3:
			urlid = (groups[0], groups[1])
			name = groups[2]
			return (urlid, name)

def gen_submissions(username):
	url = 'http://codeforces.com/submissions/{0}'.format(username)
	response = urllib2.urlopen(url)
	tree = etree.parse(response, etree.HTMLParser())
	submissions = tree.xpath('//tr[@data-submission-id]')
	for submission in submissions:
		result = Submission()

		result.submissionid = int(extract_string(submission, 'td[1]/a/text()'))
		result.date = extract_string(submission, 'td[2]/text()')
		result.language = extract_string(submission, 'td[5]/text()')
		result.verdict = serialize_verdict(extract_string(submission, 'td[6]/span/@class'))
		result.time = int(extract_string(submission, 'td[7]/text()').replace(' ms', ''))
		result.memory = int(extract_string(submission, 'td[8]/text()').replace(' KB', ''))

		problem = Problem()
		problem.problemid = int(extract_string(submission, 'td[4]/@data-problemid'))
		submission_problem_cell_text = extract_string(submission, 'td[4]/a/text()')
		problem.urlid, problem.description = extract_problem_urlid_and_name(submission_problem_cell_text)

		result.problem = problem

		if not result.verdict:
			result.verdict = serialize_verdict(extract_string(submission, 'td[6]/a/text()'))

		yield result
