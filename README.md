
CFHawk
======

Scoreboard and information retriever from codeforces.com for UA ACM SIGCOMP


Installation
============

Ubuntu
-----

Not fully tested, but this is the general idea

    sudo apt-get install python python-pip libxml2-dev libxslt1-dev python-dev
    sudo pip install -r requirements.txt


Operation
=========

Run `./update-scoreboard.py` at whatever interval you want to update the scoreboard.

Note: this should probably be no more than once a minute due to the amount of scraping


Host the static files in the configured output directory using the webserver of your choice.

If you want, you can run `python -m SimpleHTTPServer` in the directory and it should work.


Configuration
=============

Create a file resembling the following at `config.toml`

```
[ui]
title = "ACMUA - SIGCOMP - Scoreboard"

[template]
input_path = "template"
output_path = "output"
index_local_path = "index.html"

[[problems]]
id = 41188
set = "599"
letter = "A"
name = "Patrick and Shopping"

[[problems]]
id = 41189
set = "599"
letter = "B"
name = "Spongebob and Joke"

[[problems]]
id = 41190
set = "599"
letter = "C"
name = "Day at the Beach"

[[problems]]
id = 41191
set = "599"
letter = "D"
name = "Spongebob and Squares"

[[people]]
handle = "t.wynn"
name = "Thomas Wynn"

[[people]]
handle = "amb288"
name = "Aaron Battershell"

[[people]]
handle = "DrChickenSalad"
name = "Brandon Browning"
```
