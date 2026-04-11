# Twitch Chat Alert

A lightweight background service that monitors Twitch chat and triggers audio alerts when viewers send messages. Uses direct IRC connection to Twitch for real-time chat monitoring.

Perfect for streamers who want to know when chat messages arrive without actively watching.

## Features

✨ **Real-time Notifications**
- Instant audio alert when chat messages arrive
- 15-minute default cooldown (configurable)
- Works with direct Twitch IRC connection
- Windows, macOS, Linux support

🎵 **Audio Alerts**
- Built-in alert sound
- Custom audio file support (`.mp3`, `.wav`, etc.)

⚙️ **Minimal Configuration**
- Just 3 environment variables needed
- OAuth token stored locally in `.env`
- Logs to `logs/twitch_alert.log`

🔐 **Security**
- Direct OAuth token authentication with Twitch
- No data collection or external calls
- Requires only `chat:read` scope

## Installation

### Prerequisites
- Python 3.8+
- **Windows**: No additional dependencies! 🎉
- **macOS/Linux**: No additional dependencies! 🎉

### Quick Start (5 minutes)

1. **Navigate to project:**
   ```bash
   cd twitch_chat_alert
   ```

2. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependency:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration:**
   ```bash
   copy .env.example .env    # Windows
   cp .env.example .env       # macOS/Linux
   ```

5. **Get your OAuth token:**
   - Visit: https://dev.twitch.tv/console/apps
   - Create or select your application
   - Generate OAuth token with `chat:read` scope
   - **OR** Use quick generator: https://twitchtokengenerator.com/ (select `chat:read`)

6. **Edit `.env`:**
   ```
   TWITCH_CHANNEL=your_channel_name
   TWITCH_ACCESS_TOKEN=your_oauth_token_here
   LOG_LEVEL=INFO
   ```

7. **Run it!**
   ```bash
   python main.py
   ```

   You should see:
   ```
   ✓ Socket connected
   ✓ Sent OAuth token (authenticated mode)
   ✓ Joined channel: #your_channel_name
   ✅ Connected to Twitch IRC
   🎧 Monitoring channel. Send a message to test!
   ```

   Send a test message in your Twitch chat - you should hear the alert sound! 🔔

## Usage

### Run the service

```bash
python main.py
```

The service will:
1. Connect to Twitch IRC using your OAuth token
2. Monitor your channel for chat messages
3. Play `sounds/default_alert.mp3` when a message arrives
4. Enforce 15-minute cooldown before next alert
5. Log all activity to `logs/twitch_alert.log`

### Customization

**Adjust alert settings:** Edit `config.json`:
```json
{
  "alert": {
    "cooldown_seconds": 900,              // Seconds between alerts (900 = 15 min)
    "sound_file": "sounds/default_alert.mp3",  // Path to alert sound file
    "ignore_own_messages": true           // Don't alert on your own messages
  }
}
```

**Change any setting and restart the service - no code editing needed!**

### Run as Background Service

See [RUNNING_AS_SERVICE.md](RUNNING_AS_SERVICE.md) for detailed instructions on:
- **Windows (Task Scheduler)** - Auto-start at login or on schedule
- **macOS (LaunchAgent)** - Background launch agent
- **Linux (systemd)** - System service unit

## Troubleshooting

### No sound playing?
- **Windows**: Should work out of the box (uses built-in winsound)
- **macOS/Linux**: Verify `main.py` can play sound (sound file must exist)
- Verify sound file exists: `ls sounds/default_alert.mp3`
- Check `logs/twitch_alert.log` for errors

### Not connecting to Twitch?
- Verify OAuth token is valid: Check your `.env` file
- Verify token has `chat:read` scope (check at https://dev.twitch.tv)
- Check channel name is lowercase in `.env`
- Check internet connection
- Look for errors in `logs/twitch_alert.log`

### Alerts not triggering?
- Make sure the service is running and shows `✅ Connected to Twitch IRC`
- Verify cooldown time hasn't elapsed (default: 15 minutes)
- Check `logs/twitch_alert.log` for message activity
- Send a test message to your Twitch chat

### Debug mode

Change `LOG_LEVEL` in `.env`:
```
LOG_LEVEL=DEBUG
```

Then check `logs/twitch_alert.log` for detailed output.

## Architecture

Simple and focused:
```
main.py                           # Main entry point / service orchestration
src/
└── twitch_irc_monitor.py        # IRC connection logic
```

**That's it!** No complex dependencies, no config files, just IRC + alerts.

## Security

- ⚠️ **Never commit `.env` file** - contains your OAuth token
- ⚠️ **Never share your OAuth token** - treat it like a password
- Only uses `chat:read` scope (minimal permissions)
- No data collection or external calls

## License

MIT License - See [LICENSE](LICENSE) for details

## Support

Questions or bugs? Create an issue!

---

**Made for streamers** 🎮 Stream with confidence knowing you won't miss chat messages.
