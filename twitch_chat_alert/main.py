"""
Twitch Chat Alert Service
Main entry point using IRC connection
"""

import os
import sys
import logging
import json
from pathlib import Path
from dotenv import load_dotenv
from playsound import playsound
import time

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from twitch_irc_monitor import TwitchIRCMonitor

# Load environment
load_dotenv()

TWITCH_CHANNEL = os.getenv("TWITCH_CHANNEL", "").lower()
TWITCH_ACCESS_TOKEN = os.getenv("TWITCH_ACCESS_TOKEN")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("twitch_alert")


class TwitchAlertService:
    """Main service combining IRC monitoring with audio alerts"""
    
    CONFIG_FILE = Path(__file__).parent / "config.json"
    
    def __init__(self):
        self.channel = TWITCH_CHANNEL
        self.token = TWITCH_ACCESS_TOKEN
        self.last_alert_time = 0
        self.monitor = None
        
        # Load configuration
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """Load configuration from config.json"""
        try:
            with open(self.CONFIG_FILE) as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"❌ config.json not found at {self.CONFIG_FILE}")
            return {}
        except json.JSONDecodeError:
            logger.error("❌ config.json is invalid JSON")
            return {}
            
    def _get_config(self, key: str, default=None):
        """Get config value with dot notation (e.g., 'alert.cooldown_seconds')"""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default
        
    def start(self):
        """Start the alert service"""
        logger.info("=" * 70)
        logger.info("Twitch Chat Alert Service")
        logger.info("=" * 70)
        
        # Validate config file
        if not self.CONFIG_FILE.exists():
            logger.error(f"❌ config.json not found")
            logger.info(f"Create {self.CONFIG_FILE} with your settings")
            return
            
        if not self.config:
            logger.error("❌ config.json is empty or invalid JSON")
            return
        
        # Validate env
            logger.error("❌ TWITCH_CHANNEL not set in .env")
            logger.info("Update .env and try again")
            return
            
        logger.info(f"Channel: {self.channel}")
        if self.token:
            logger.info("✓ Using OAuth authentication")
        else:
            logger.error("❌ TWITCH_ACCESS_TOKEN not set in .env")
            logger.info("Cannot receive messages without OAuth token")
            return
            
        # Check for sound file
        sound_file = self._get_config("alert.sound_file", "sounds/default_alert.mp3")
        sound_path = Path(__file__).parent / sound_file
        if not sound_path.exists():
            logger.warning(f"⚠ Sound file not found: {sound_path}")
            logger.info("  Audio alerts will be disabled")
            
        logger.info("")
        
        # Create monitor - use channel name as username when authenticated
        self.monitor = TwitchIRCMonitor(
            channel=self.channel,
            oauth_token=self.token,
            username=self.channel  # Use channel name as username for auth
        )
        
        # Connect with retry
        while True:
            if self.monitor.connect():
                break
            logger.info("Retrying connection in 5 seconds...")
            time.sleep(5)
            
        # Start monitoring
        try:
            self.monitor.monitor(message_callback=self.on_message)
        except KeyboardInterrupt:
            logger.info("\n✓ Service stopped")
        except Exception as e:
            logger.error(f"Error: {e}")
            
    def on_message(self, author: str, message: str):
        """
        Callback when chat message received
        
        Args:
            author: Username of message author
            message: Content of message
        """
        # Check if we should ignore own messages
        ignore_own = self._get_config("alert.ignore_own_messages", True)
        if ignore_own and author.lower() == self.channel:
            logger.debug(f"Ignoring own message: {author}")
            return
        
        # Check if we should ignore bots
        ignore_bots = self._get_config("alert.ignore_bots", True)
        if ignore_bots and ("bot" in author.lower() or "stream" in author.lower()):
            logger.debug(f"Ignoring bot message: {author}")
            return
        
        # Get cooldown from config
        cooldown = self._get_config("alert.cooldown_seconds", 900)
        
        # Simple rate limiting
        current_time = time.time()
        if current_time - self.last_alert_time < cooldown:
            return
            
        # Log message
        logger.info(f"🔔 Alert: {author}")
        
        # Play sound
        self._play_alert()
        
        self.last_alert_time = current_time
        
    def _play_alert(self):
        """Play audio alert using playsound"""
        sound_file = self._get_config("alert.sound_file", "sounds/default_alert.mp3")
        sound_path = (Path(__file__).parent / sound_file).resolve()
        
        logger.info(f"🔊 Attempting to play sound from: {sound_path}")
        logger.info(f"   File exists: {sound_path.exists()}")
        logger.info(f"   File size: {sound_path.stat().st_size if sound_path.exists() else 'N/A'} bytes")
        
        if not sound_path.exists():
            logger.warning(f"⚠ Sound file not found: {sound_path}")
            return
            
        try:
            # Use playsound for audio playback (handles MP3 natively)
            playsound(str(sound_path))
            logger.info(f"✓ Sound played successfully")
        except Exception as e:
            logger.warning(f"❌ Could not play sound: {e}")


def main():
    """Main entry point"""
    service = TwitchAlertService()
    service.start()


if __name__ == "__main__":
    main()
