#
#   This example shows how to send a trigger event without a dedup_key.
#   In this case, PagerDuty will automatically assign a random and unique key
#   and return it in the response object.
#   You should store this key in case you want to send an acknowledge or resolve
#   event to this incident in the future.
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
        "dedup_key": "example_key",
        "payload": {
            "summary": "Example alert",
            "source": "Nagios monitoring tool",
            "severity": "critical",
            },
        }

    r = requests.post(base_url, headers=headers, data=json.dumps(payload))

    print 'Triggered event response code: ' + str(r.status_code)
    return r.json()['dedup_key']


def acknowledge_event(headers, integration_key, dedup_key):
    """Acknowledges event on Pagerduty."""

    payload = {
        "routing_key": integration_key,
        "dedup_key": dedup_key,
        "event_action": "acknowledge"
        }

    r = requests.post(base_url, headers=headers, data=json.dumps(payload))

    print 'Acknowledged response code: ' + str(r.status_code)
    return r.json()['dedup_key']


if __name__ == '__main__':

    # HTTP Request Headers
    headers = {
        'Content-type': 'application/json',
        }

    integration_key = sys.argv[1]

    t_dedup_key = trigger_event(headers, integration_key)

    time.sleep(2)

    a_dedup_key = acknowledge_event(headers, integration_key, t_dedup_key)

    time.sleep(2)

    print acknowledge
