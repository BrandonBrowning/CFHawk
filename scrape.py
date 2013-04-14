
import urllib2
from lxml import etree

class Submission:
	def __init__(self):
		self.submissionid = None
		self.date = None
		self.problemid = None
		self.language = None
		self.verdict = None
		self.time = None # ms
		self.memory = None # KB

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

def gen_submissions(username):
	url = 'http://codeforces.com/submissions/{0}'.format(username)
	response = urllib2.urlopen(url)
	tree = etree.parse(response, etree.HTMLParser())
	submissions = tree.xpath('//tr[@data-submission-id]')
	for submission in submissions:
		result = Submission()

		result.submissionid = int(extract_string(submission, 'td[1]/a/text()'))
		result.date = extract_string(submission, 'td[2]/text()')
		result.problemid = int(extract_string(submission, 'td[4]/@data-problemid'))
		result.language = extract_string(submission, 'td[5]/text()')
		result.verdict = serialize_verdict(extract_string(submission, 'td[6]/span/@class'))
		result.time = int(extract_string(submission, 'td[7]/text()').replace(' ms', ''))
		result.memory = int(extract_string(submission, 'td[8]/text()').replace(' KB', ''))

		if not result.verdict:
			result.verdict = serialize_verdict(extract_string(submission, 'td[6]/a/text()'))

		yield result
