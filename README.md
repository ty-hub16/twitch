# Twitch Streamer Scripts

**Skills Used:**
OAuth 2.0 auth (Twitch API), TCP socket connection to Twitch IRC, JSON config file

A collection of helpful scripts and tools for Twitch streamers. Currently includes:

## 📻 Twitch Chat Alert

Real-time audio alerts when chat messages arrive. Perfect for streamers who want to stay engaged with chat without constantly checking if they have new chat messages.

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
venv\Scripts\activate  # or source venv/bin/activate on macOS/Linux
pip install -r requirements.txt
copy .env.example .env
# Edit .env with your Twitch channel and OAuth token
python main.py
```

See [twitch_chat_alert/README.md](twitch_chat_alert/README.md) for detailed documentation.

---

## 🗑️ Record De-Dup (`record_de_dup.py`)

When OBS finishes a recording and you use the **Remux** feature to convert it to MP4, it leaves behind the original `.mkv` file alongside the new `.mp4`. This means every recording session produces a duplicate file you don't need, wasting disk space.

`record_de_dup.py` fixes this by scanning your recordings folder and deleting all `.mkv` files, keeping only the remuxed `.mp4`.

**Usage:**
```bash
# Defaults to ~/Videos (OBS default output folder)
python record_de_dup.py

# Or specify a custom recordings directory
python record_de_dup.py "C:\Path\To\Recordings"
```

---
