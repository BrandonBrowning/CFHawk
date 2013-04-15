
from scrape import gen_submissions, Problem, StudentWeek
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

title = 'ACMUA - SIGCOMP - Leaderboard'
css = ["css/bootstrap.min.css", "css/font-awesome.min.css", "css/site.css"]
js = ["js/jquery.min.js", "http://d3js.org/d3.v3.min.js", "js/site.js"]
winner_text = 'TODO'

template_path = 'template/'
engine = Engine(loader=FileLoader([template_path]), extensions=[CoreExtension()])

index_template = engine.get_template('index.html')

week_problems_unsorted = [Problem(1798, ('223', 'C'), 'Partial Sums'), Problem(969, ('158', 'A'), 'Next Round')]
week_problems = set(sorted(week_problems_unsorted, key=lambda p: p.problemid))

def completed_to_icon_html(correct):
	return "<i class=\"{0} icon-3x\"></i>".format("icon-ok" if correct else "icon-remove")

def gen_correct_problem_mapping(submissions, week_problemids):
	accepted_submissions = set([s.problem.problemid for s in submissions if s.verdict == 'Accepted'])
	for problemid in week_problemids:
		completed = problemid in accepted_submissions
		yield (problemid, completed, completed_to_icon_html(completed))

profile_names = ['ermiar', 'DrChickenSalad']
def gen_people(profile_names, week_problem):
	week_problemids = [p.problemid for p in week_problems]
	for person in profile_names:
		submissions = list(gen_submissions(person))
		correct_mapping = gen_correct_problem_mapping(submissions, week_problemids)
		student_week = StudentWeek(person, sorted(correct_mapping))

		print('{0}: {1}'.format(student_week.name, student_week.correct))
		yield student_week

people = list(gen_people(profile_names, week_problems))
render_values = {
	'title': title,
	'css': css,
	'js': js,
	'winner_text': winner_text,
	'week_problems': week_problems,
	'people': people
}

with open('output/index.html', 'w') as f:
	f.write(index_template.render(render_values))