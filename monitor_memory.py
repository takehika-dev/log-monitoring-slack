#!/usr/bin/env python3

import os
import sys
import time
import argparse

try:
    import psutil
except ImportError:
    print("Missing dependency: psutil. Install with: pip install psutil", file=sys.stderr)
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Missing dependency: requests. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


def send_slack_message(token, channel, text):
    """Send a message to Slack using chat.postMessage."""

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {"channel": channel, "text": text}

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            print(f"Slack API error: {data.get('error')}", file=sys.stderr)

    except requests.RequestException as e:
        print(f"Failed to send Slack message: {e}", file=sys.stderr)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Monitor memory usage and send Slack alerts when usage is high."
    )

    parser.add_argument(
        "--threshold",
        type=float,
        default=80.0,
        help="Memory usage percent threshold to trigger an alert (default: 80.0)",
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Time interval in seconds between checks (default: 60)",
    )

    parser.add_argument(
        "--slack-token",
        help="Slack Bot OAuth token (env var SLACK_BOT_TOKEN if not provided)"
    )

    parser.add_argument(
        "--slack-channel",
        help="Slack channel (name or ID) to post alerts (env var SLACK_CHANNEL or default '#general')"
    )

    return parser.parse_args()


def main():
    args = parse_args()
    token = args.slack_token or os.environ.get("SLACK_BOT_TOKEN")
    if not token:
        print(
            "Error: Slack Bot token must be set via --slack-token or SLACK_BOT_TOKEN env var",
            file=sys.stderr,
        )
        sys.exit(1)
    channel = args.slack_channel or os.environ.get("SLACK_CHANNEL", "#general")

    threshold = args.threshold
    interval = args.interval
    notified = False

    print(f"Starting memory monitor: threshold={threshold}%, interval={interval}s, channel={channel}")
    while True:
        mem = psutil.virtual_memory()
        usage = mem.percent
        message = None

        if usage >= threshold and not notified:
            message = f":warning: Memory usage high: {usage:.2f}% (threshold: {threshold}%)"
            notified = True
        elif usage < threshold and notified:
            message = f":white_check_mark: Memory usage back to normal: {usage:.2f}% (threshold: {threshold}%)"
            notified = False

        if message:
            send_slack_message(token, channel, message)
            print(message)

        time.sleep(interval)


if __name__ == "__main__":
    main()
    