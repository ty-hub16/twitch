# Twitch Chat Alert

Play a sound when new chat messages arrive in your Twitch channel.

This app connects directly to Twitch IRC and uses a Twitch user access token from the official Twitch OAuth flow.

## Requirements

- Python 3.10+
- Windows for audio playback (`winsound` is used for alerts)
- A Twitch user access token (Client Secret from dev.twitch.tv)

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
- `TWITCH_ACCESS_TOKEN`: your Client Secret from dev.twitch.tv
- `LOG_LEVEL`: optional, defaults to `INFO`

## Getting a Twitch Access Token

1. Go to https://dev.twitch.tv/
2. Click **Create Application** > **Register Your Application**
3. Enter your application name
4. Set the OAuth redirect URI to `http://localhost:3000`
5. Select **Application Integration** as the category
6. Once created, go to **Applications** on the left sidebar
7. Click **Manage** on your application
8. Under the **Client ID** section, click **Generate a New Client Secret**
9. Copy the **Client Secret** and paste it into `.env` as `TWITCH_ACCESS_TOKEN`

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

- Confirm the Client Secret came from dev.twitch.tv
- Confirm `TWITCH_CHANNEL` matches the channel name in lowercase

### No audio plays

- Confirm the sound file exists
- Confirm Windows audio is working
- Check the configured `alert.sound_file` path in `config.json`

### App exits immediately

- Confirm `.env` exists next to `main.py`
- Confirm `config.json` is valid JSON
- Review console output for missing configuration values