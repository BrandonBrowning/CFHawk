#!/usr/bin/env python2

import api
from model import Person, Problem

import hashlib
import os
import toml
from datetime import datetime
from easydict import EasyDict as edict
from wheezy.template.engine import Engine
from wheezy.template.ext.core import CoreExtension
from wheezy.template.loader import FileLoader

def calculate_sha1(s):
    sha1 = hashlib.sha1()
    sha1.update(s)

    return sha1.digest()

def log(s):
    print('[%s] %s' % (datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'), s))

with open('config.toml') as f:
    config = edict(toml.loads(f.read()))

announcement = config.ui.announcement
title = config.ui.title
people = [Person(p.handle, p.name) for p in config.people]
problems = [Problem(config.week.contest_id, p.letter, p.name) for p in config.week.problems]

contest_ids = set(p.contest_id for p in problems)
assert len(contest_ids) == 1
contest_id = int(contest_ids.pop())

solves = dict()
for person in people:
    response = api.get_user_contest_submissions(person.handle, contest_id)
    solves[person] = set(s.problem.index for s in response if s.problem.contestId == contest_id and s.verdict == 'OK')

people = sorted(people, key=lambda p: len(solves[p]), reverse=True)

template_input_path = config.template.input_path
engine = Engine(
    loader=FileLoader([template_input_path]),
    extensions=[CoreExtension()])

index_template = engine.get_template(config.template.index_local_path)
model = {
    'announcement': announcement,
    'people': people,
    'problems': problems,
    'solves': solves,
    'title': title
}
index_html = index_template.render(model)

with open(os.path.join(config.template.output_path, 'index.html'), 'r') as f:
    existing_index_html = f.read()

updated_file = calculate_sha1(index_html) != calculate_sha1(existing_index_html)

if updated_file:
    with open(os.path.join(config.template.output_path, 'index.html'), 'w') as f:
        f.write(index_html)

    with open(os.path.join(config.template.output_path, 'last_modified.json'), 'w') as f:
        f.write('"%s"' % datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))

    log('Updated to new index.html')
else:
    log('No changes to index.html')
