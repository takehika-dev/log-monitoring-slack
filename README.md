# Memory Monitor with Slack
Monitor system memory usage and send alerts to Slack when usage exceeds a defined threshold.

## Features
- Periodic polling of system RAM usage
- Alerts when memory usage crosses above threshold
- Notification when usage returns to normal
- Posts messages to Slack channels via API

## Prerequisites
- Python >= 3.6

Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Slack App Setup
1. Go to https://api.slack.com/apps and **Create New App** from scratch.
2. Under **OAuth & Permissions**, add the `chat:write` scope.
3. Install the app into your workspace and authorize.
4. Copy the **Bot User OAuth Token** (starts with `xoxb-…`).
5. Invite the bot user to your target channel:
```
/invite @YourBotName
```


## Configuration
Set the following environment variables:
   ```bash
   export SLACK_BOT_TOKEN="xoxb-..."             # Bot User OAuth Token
   export SLACK_CHANNEL="#your-channel-name"     # Channel name or ID (default: #general)
   ```

## Usage
   ```bash
   python monitor_memory.py --threshold 80 --interval 60
   ```

### Options
- `--threshold`: Memory usage percent to trigger alert (default: 80.0)
- `--interval`: Polling interval in seconds (default: 60)
- `--slack-token`: Slack Bot token (overrides SLACK_BOT_TOKEN)
- `--slack-channel`: Slack channel (overrides SLACK_CHANNEL)


## License
You are free to use this code for personal and educational purposes. Commercial use and redistribution are not allowed.
