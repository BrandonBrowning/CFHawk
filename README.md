
CFHawk
======

Scoreboard and information retriever from codeforces.com for UA ACM SIGCOMP


Installation
============

Ubuntu
-----

Not fully tested, but this is the general idea

    sudo apt-get install python python-pip
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
announcement = "SIGCOMP Scoreboard"
title = "SIGCOMP Scoreboard"

[template]
input_path = "template"
output_path = "output"
index_local_path = "index.html"

[week]
contest_id = "618"

[[week.problems]]
letter = "A"
name = "Slime Combining"

[[week.problems]]
letter = "B"
name = "Guess the Permutation"

[[week.problems]]
letter = "C"
name = "Constellation"

[[week.problems]]
set = "618"
letter = "D"
name = "Hamiltonian Spanning Tree"

[[week.problems]]
set = "618"
letter = "E"
name = "Robot Arm"

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
