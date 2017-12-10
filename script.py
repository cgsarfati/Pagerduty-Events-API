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
    return r.json()['dedeup_key']


if __name__ == '__main__':

    # HTTP Request Headers
    headers = {
        'Content-type': 'application/json',
        }

    trigger_event(headers, sys.argv[1])
