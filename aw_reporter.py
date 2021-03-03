#!/usr/bin/env python3

import requests
import json
import click
import sys
from datetime import datetime, timedelta

WALLETS = [
    {"xxxxx.wam": "name"},
]
for wallet in WALLETS:
    addr = list(wallet)[0]
    name = wallet.get(addr)
    URL = f"https://wax.eosphere.io/v2/history/get_actions?account={addr}&limit=1000"
    HOURS = 3

    resp = requests.get(URL)

    if resp.status_code != 200:
        click.secho(f"Problem pulling wallet data: {resp.reason}", bold=True, fg="red")
        sys.exit(1)

    actions = resp.json().get("actions")

    now = datetime.utcnow()
    last_day = []
    for action in actions:
        timestamp = datetime.fromisoformat(action.get("timestamp"))
        delta = timestamp - now
        if (
            abs(delta.total_seconds()) < HOURS * 60 * 60
            and action.get("act").get("data").get("from") == "m.federation"
            and action.get("act").get("name") == "transfer"
        ):
            last_day.append(action)

    total = float(0)
    for action in last_day:
        total += action.get("act").get("data").get("amount")
        avg = total / len(last_day)
    print(name)
    print("----------")
    print(f"Attempts: {len(last_day)}")
    print(f"Total: {total}")
    print(f"Avg: {avg}")
    print()
