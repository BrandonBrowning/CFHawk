#!/usr/bin/env bash

function control_c {
    exit 1
}

function usage {
    >&2 echo "Usage: $0 [sleep-seconds]"
    exit 1
}

trap control_c SIGINT

sleep_seconds="60"
if [[ "$#" -eq "1" ]]; then
    if [[ "$1" == "--help" ]] || [[ "$1" == "--usage" ]]; then
        usage
    elif [[ "$1" =~ ^[0-9]+$ ]]; then
        sleep_seconds="$1"
    else
        >&2 echo "Did not recognize $1 as a number"
        exit 2
    fi
elif [[ "$#" -gt "1" ]]; then
    usage
fi

while true; do
    before_time="$(date +%s)"
    ./update-scoreboard.py
    after_time="$(date +%s)"
    actual_sleep_seconds="$(expr $sleep_seconds - $after_time + $before_time)"
    sleep "$actual_sleep_seconds"
done
