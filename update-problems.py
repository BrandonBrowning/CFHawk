import email
import imaplib
import os
import re
import toml

import api

def get_email_body(e):
    email_type = e.get_content_maintype()
    if email_type == 'multipart':
        for part in e.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif email_type == 'text':
        return e.get_payload()

def get_codeforces_problems(body):
    # todo: call api to map names for arbitrary problems
    # problems = list(re.findall('https?://codeforces\.com/contest/(\d+)/problem/(\w)', body))
    # if problems and len(problems) > 0:
    #     return problems

    contests = list(re.findall('https?://codeforces\.com/contest/(\d+)', body))
    if contests and len(contests) > 0:
        return api.get_contest_problems(contests[0])

    return []

mail = imaplib.IMAP4_SSL('imap.gmail.com')

username = os.getenv('EMAIL', 'scoreboard.acm.ua@gmail.com')
password = os.environ['EMAIL_PASSWORD']

mail.login(username, password)
mail.select('inbox')

_, ids_data = mail.search(None, 'All')
ids = ids_data[0].split(' ')
most_recent_id = sorted([int(x) for x in ids], reverse=True)[0]
_, message_data = mail.fetch(most_recent_id, '(RFC822)')
message_raw = message_data[0][1]
message = email.message_from_string(message_raw)
body = get_email_body(message).strip()
problems = get_codeforces_problems(body)

result = { 'problems': [{ 'contest_id': p[0], 'letter': p[1], 'name': p[2] } for p in problems] }
with open('problems.toml', 'w') as f:
    f.write(toml.dumps(result))
