# Twitch Chat Alert

Play a sound when new chat messages arrive in your Twitch channel.

This app connects directly to Twitch IRC and uses a Twitch user access token from the official Twitch OAuth flow.

## Requirements

- Python 3.10+
- Windows for audio playback (`winsound` is used for alerts)
- A Twitch user access token with the `chat:read` scope

## Setup

### 1. Create and activate a virtual environment

#### Windows Command Prompt
```bat
python -m venv venv
venv\Scripts\activate
```

#### Windows PowerShell
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy `.env.example` to `.env` and set:

- `TWITCH_CHANNEL`: your Twitch channel name in lowercase
- `TWITCH_ACCESS_TOKEN`: a Twitch user access token from the official Twitch OAuth flow
- `LOG_LEVEL`: optional, defaults to `INFO`

Important:

- Do not include `oauth:` in `TWITCH_ACCESS_TOKEN`
- The app adds the `oauth:` prefix when connecting to IRC
- The token must include the `chat:read` scope

## Getting a Twitch Access Token

Use Twitch's official developer auth flow:

1. Create or use a Twitch application in the Twitch Developer Console.
2. Request a user access token with the `chat:read` scope.
3. Copy the returned access token into `.env` as `TWITCH_ACCESS_TOKEN`.

Reference:

- https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/

## Run the App

```bash
python main.py
```

When connected successfully, the app joins `#TWITCH_CHANNEL`, logs incoming messages, and plays the configured sound when the cooldown allows it.

## Configuration

Settings in `config.json`:

- `alert.cooldown_seconds`: minimum time between sound alerts
- `alert.sound_file`: relative path to the alert sound file
- `alert.ignore_own_messages`: ignore messages sent by the configured channel account

Default sound file:

- `sounds/default_alert.mp3`

## Run at Startup

See [RUNNING_AS_SERVICE.md](RUNNING_AS_SERVICE.md) for Task Scheduler setup on Windows.

## Troubleshooting

### Authentication fails

- Confirm the token came from Twitch's official OAuth flow
- Confirm the token has the `chat:read` scope
- Confirm `TWITCH_ACCESS_TOKEN` does not include `oauth:`
- Confirm `TWITCH_CHANNEL` matches the channel name in lowercase

### No audio plays

- Confirm the sound file exists
- Confirm Windows audio is working
- Check the configured `alert.sound_file` path in `config.json`

### App exits immediately

- Confirm `.env` exists next to `main.py`
- Confirm `config.json` is valid JSON
- Review console output for missing configuration values