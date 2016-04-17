
import requests

from easydict import EasyDict as edict

def get_user_contest_submissions(user, contest):
    url = 'http://codeforces.com/api/contest.status?contestId=%s&handle=%s&from=1&count=100' % (contest, user)
    return _get_result(url)

def get_contest_problems(contest):
    url = 'http://codeforces.com/api/contest.standings?contestId=%s&from=1&count=1' % contest
    data = _get_result(url)
    return [(p.contestId, p.index, p.name) for p in data.problems]

def _get_result(url):
    r = requests.get(url)
    data = edict(r.json())
    if data.status == 'OK':
        return data.result
    else:
        if data.comment:
            raise ValueError('Codeforces api call failed with message: %s' % data.comment)
        else:
            raise ValueError('Codeforces api call failed with no comment')

