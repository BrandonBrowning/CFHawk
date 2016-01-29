#!/usr/bin/env python2

import os
from datetime import datetime

import toml
from easydict import EasyDict as edict
from scrape import gen_submissions, Problem, StudentWeek
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

with open('config.toml') as f:
    config = edict(toml.loads(f.read()))

title = config.ui.title
css = ["css/bootstrap.min.css", "css/font-awesome.min.css", "css/site.css"]
js = ["js/jquery.min.js", "http://d3js.org/d3.v3.min.js", "js/site.js"]
winner_text = 'TODO Winner Text!'

engine = Engine(loader=FileLoader([config.template.input_path]), extensions=[CoreExtension()])
index_template = engine.get_template(config.template.index_local_path)

week_problems = [Problem(p.id, (p.set, p.letter), p.name) for p in config.problems]

def completed_to_icon_html(correct):
	return "<i class=\"{0} icon-3x\"></i>".format("icon-ok" if correct else "icon-remove")

def gen_correct_problem_mapping(submissions, week_problemids):
	accepted_submissions = set([s.problem.problemid for s in submissions if s.verdict == 'Accepted'])
	for problemid in week_problemids:
		completed = problemid in accepted_submissions

		yield (problemid, completed, completed_to_icon_html(completed))

profile_names = [person.handle for person in config.people]
def gen_people(profile_names, week_problem):
	week_problemids = [p.problemid for p in week_problems]
	for person in profile_names:
		submissions = list(gen_submissions(person))
		correct_mapping = gen_correct_problem_mapping(submissions, week_problemids)
		student_week = StudentWeek(person, sorted(correct_mapping))

		yield student_week

people = list(sorted(gen_people(profile_names, week_problems), key=lambda sw: sum(map(lambda t: -t[1], sw.correct))))
render_values = {
	'title': title,
	'css': css,
	'js': js,
	'winner_text': winner_text,
	'week_problems': week_problems,
	'people': people
}

def output_file(filename):
	return os.path.join(config.template.output_path, filename)

with open(output_file('index.html'), 'w') as f:
	f.write(index_template.render(render_values))

with open(output_file('last_modified.json'), 'w') as f:
	f.write('"{0}"'.format(datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
