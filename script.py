#
# This example uses Pagerduty's Events API to trigger, acknowledge and resolve
# an incident.
#
# CLI usage: python script.py integration_key

import requests
import json
import sys
import time

base_url = 'https://events.pagerduty.com/v2/enqueue'


def trigger_event(headers, integration_key):
    """Triggers event on Pagerduty."""

    payload = {
        "routing_key": integration_key,
        "event_action": "trigger",
        "dedup_key": "example_key",  # used to refer to event for future use
        "payload": {
            "summary": "Example alert",
            "source": "Nagios monitoring tool",
            "severity": "critical",
            },
        }

    r = requests.post(base_url, headers=headers, data=json.dumps(payload))

    print 'Trigger response code: ' + str(r.status_code)
    return r.json()['dedup_key']


def acknowledge_event(headers, integration_key, dedup_key):
    """Acknowledges event on Pagerduty."""

    payload = {
        "routing_key": integration_key,
        "dedup_key": dedup_key,
        "event_action": "acknowledge"
        }

    r = requests.post(base_url, headers=headers, data=json.dumps(payload))

    print 'Acknowledge response code: ' + str(r.status_code)
    return r.json()['dedup_key']


def resolve_event(headers, integration_key, dedup_key):
    """Resolves event on Pagerduty."""

    payload = {
        "routing_key": integration_key,
        "dedup_key": dedup_key,
        "event_action": "resolve"
        }

    r = requests.post(base_url, headers=headers, data=json.dumps(payload))

    print 'Resolve response code: ' + str(r.status_code)
    return r.json()['dedup_key']


if __name__ == '__main__':

    # HTTP Request Headers
    headers = {
        'Content-type': 'application/json',
        }

    integration_key = sys.argv[1]  # API integration key in service

    t_dedup_key = trigger_event(headers, integration_key)

    time.sleep(2)

    a_dedup_key = acknowledge_event(headers, integration_key, t_dedup_key)

    time.sleep(2)

    r_dedup_key = resolve_event(headers, integration_key, a_dedup_key)
