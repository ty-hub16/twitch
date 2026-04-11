# Twitch Chat Alert

Play a sound when new chat messages arrive in your Twitch channel.

This app connects directly to Twitch IRC and uses a Twitch user access token from the official Twitch OAuth flow.

## Requirements

- Python 3.10+
- Windows for audio playback (`winsound` is used for alerts)
- A Twitch user access token (Client Secret from dev.twitch.tv)

## Setup

### 1. Create and activate a virtual environment

cd twitch_chat_alert


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

### Step 1: Create an Application

1. Go to https://dev.twitch.tv/
2. Click **Create Application** > **Register Your Application**
3. Enter your application name
4. Set the OAuth redirect URI to `http://localhost:3000`
5. Select **Application Integration** as the category
6. Once created, go to **Applications** on the left sidebar and click **Manage**
7. Copy your **Client ID** (you'll need this in the next step)

### Step 2: Get Your User Access Token

1. Take this template URL and replace `YOUR_CLIENT_ID` with your actual Client ID:
   ```
   https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:3000&scope=chat%3Aread+chat%3Aedit
   ```
   
   **Example:** If your Client ID is `exampleclientid123456789abcdef`, your URL would be:
   ```
   https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=exampleclientid123456789abcdef&redirect_uri=http://localhost:3000&scope=chat%3Aread+chat%3Aedit
   ```

2. Paste the full URL (with YOUR_CLIENT_ID replaced) into your web browser
3. Click **Authorize** when prompted
4. You may see an error page, but don't worry—**the access token is in the URL**
5. Look at the address bar. The URL will look like:
   ```
   http://localhost:3000/#access_token=exampletoken123456789abcdef&scope=chat%3Aread+chat%3Aedit&token_type=bearer
   ```
6. Copy the token value (the long string after `access_token=` and before `&scope`)
   - In the example above, the token is: `exampletoken123456789abcdef`
7. Paste it into `.env` as `TWITCH_ACCESS_TOKEN`

## Run the App

```bash
python main.py
```

When connected successfully, the app joins `#TWITCH_CHANNEL`, logs incoming messages, and plays the configured sound when the cooldown allows it.

## Configuration

Settings in `config.json`:

- `alert.cooldown_seconds`: minimum time between sound alerts (in seconds; set to 0 for testing)
- `alert.sound_file`: relative path to the alert sound file
- `alert.ignore_own_messages`: ignore messages sent by the configured channel account
- `alert.ignore_bots`: ignore messages from bot accounts (filters usernames containing "bot" or "stream")

**Testing vs Production:**
- **For testing**: Set `cooldown_seconds: 0` and `ignore_own_messages: false`
- **For production**: Set `ignore_own_messages: true` and `ignore_bots: true`

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