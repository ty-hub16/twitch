# Twitch Streamer Scripts

A collection of helpful scripts and tools for Twitch streamers. Currently includes:

## 📻 Twitch Chat Alert

Real-time audio alerts when chat messages arrive. Perfect for streamers who want to stay engaged with chat without constantly watching.

**Features:**
- Instant audio alerts on chat messages
- Direct Twitch IRC connection
- Configurable cooldown (15 minutes default)
- Simple setup (3 environment variables)
- Minimal dependencies
- Cross-platform (Windows, macOS, Linux)

**Quick Start:**
```bash
cd twitch_chat_alert
python -m venv venv
venv/Scripts/activate  # or source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your Twitch channel and OAuth token
python main.py
```

See [twitch_chat_alert/README.md](twitch_chat_alert/README.md) for detailed documentation.

---

**More tools coming soon!** Have a script idea? Open an issue!