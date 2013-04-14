
import scrape

people = ['ermiar', 'DrChickenSalad']

for person in people:
	subs = list(scrape.gen_submissions(person))
	correct = set([s.problemid for s in subs if s.verdict == 'Accepted'])
	week_problems = set([1798, 969])
	scoreboard = [(p, p in correct) for p in week_problems]
	print('{0}: {1}'.format(person, scoreboard))