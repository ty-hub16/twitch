"""
Twitch Chat Monitor using Direct IRC Connection
Simple, reliable, and works without OAuth
"""

import socket
import logging
import time
import os
from pathlib import Path

logger = logging.getLogger(__name__)


class TwitchIRCMonitor:
    """Monitor Twitch chat via direct IRC socket"""
    
    IRC_HOST = "irc.chat.twitch.tv"
    IRC_PORT = 6667
    
    def __init__(self, channel: str, oauth_token: str = None, username: str = "justinfan12345"):
        """
        Initialize IRC monitor
        
        Args:
            channel: Twitch channel name (without #)
            oauth_token: Optional OAuth token for authenticated connection
            username: IRC username (anonymous by default)
        """
        self.channel = channel.lower()
        self.oauth_token = oauth_token
        self.username = username
        self.sock = None
        self.connected = False
        self.message_count = 0
        
    def connect(self) -> bool:
        """Connect to Twitch IRC and join channel"""
        try:
            logger.info(f"Connecting to {self.IRC_HOST}:{self.IRC_PORT}...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.IRC_HOST, self.IRC_PORT))
            logger.info("✓ Socket connected")
            
            # IMPORTANT: Send PASS BEFORE NICK for OAuth authentication
            if self.oauth_token:
                pass_cmd = f"PASS oauth:{self.oauth_token}\r\n"
                self.sock.sendall(pass_cmd.encode())
                logger.info("✓ Sent OAuth token (authenticated mode)")
            else:
                logger.info("⚠ Using anonymous connection (limited functionality)")
                
            # Send NICK after PASS
            nick_cmd = f"NICK {self.username}\r\n"
            self.sock.sendall(nick_cmd.encode())
            logger.debug(f"✓ Set nickname: {self.username}")
            
            # Enable message tags and commands
            self.sock.sendall("CAP REQ :twitch.tv/tags\r\n".encode())
            self.sock.sendall("CAP REQ :twitch.tv/commands\r\n".encode())
            logger.debug("✓ Enabled Twitch capabilities")
            
            # Wait for connection response (with timeout)
            self.sock.settimeout(5)
            try:
                response = self.sock.recv(4096).decode("utf-8")
                if "004" in response or "001" in response:
                    logger.debug("✓ Received server welcome")
                else:
                    logger.debug("✓ Received response")
                    
                # Check for authentication errors
                if "NOTICE" in response and ("error" in response.lower() or "fail" in response.lower()):
                    logger.error("⚠ Authentication error detected!")
                    
            except socket.timeout:
                logger.warning("⚠ No welcome message (continuing anyway)")
            finally:
                self.sock.settimeout(None)  # Non-blocking for main loop
            
            # Join channel
            self.sock.sendall(f"JOIN #{self.channel}\r\n".encode())
            logger.info(f"✓ Joined channel: #{self.channel}")
            
            self.connected = True
            logger.info("✅ Connected to Twitch IRC\n")
            return True
            
        except Exception as e:
            logger.error(f"❌ Connection failed: {e}")
            self.connected = False
            return False
            
    def monitor(self, message_callback=None):
        """
        Monitor chat messages
        
        Args:
            message_callback: Function to call when message received: callback(author, message)
        """
        if not self.connected:
            logger.error("Not connected. Call connect() first")
            return
            
        logger.info("🎧 Monitoring channel. Send a message to test!\n")
        
        try:
            buffer = ""
            
            while True:
                try:
                    # Receive data
                    data = self.sock.recv(4096).decode("utf-8", errors="ignore")
                    if not data:
                        logger.error("Connection closed by server")
                        break
                    
                    # Add to buffer and process lines
                    buffer += data
                    lines = buffer.split("\r\n")
                    buffer = lines[-1]  # Keep incomplete line
                    
                    for line in lines[:-1]:
                        if line:
                            self._handle_line(line, message_callback)
                            
                except socket.timeout:
                    continue
                except Exception as e:
                    logger.error(f"Error receiving data: {e}")
                    print(f">>> ERROR: {e}")
                    break
                    
        except KeyboardInterrupt:
            logger.info("\n✓ Monitoring stopped")
        finally:
            self.disconnect()
            
    def _handle_line(self, line: str, callback=None):
        """Handle a single IRC line"""
        # Respond to PING
        if line.startswith("PING"):
            self.sock.send(f"PONG {line.split()[1]}\r\n".encode())
            return
            
        # Parse PRIVMSG (chat message)
        if "PRIVMSG" in line:
            msg_data = self._parse_privmsg(line)
            if msg_data:
                self.message_count += 1
                author = msg_data["author"]
                message = msg_data["message"]
                
                logger.info(f"💬 {author}: {message}")
                
                if callback:
                    callback(author, message)
            else:
                logger.debug("✗ Failed to parse PRIVMSG")
                    
    def _parse_privmsg(self, line: str) -> dict:
        """Parse a PRIVMSG line with Twitch tags"""
        try:
            # Format: @tags :user!user@host PRIVMSG #channel :message text
            
            # Find PRIVMSG marker
            if "PRIVMSG" not in line:
                return None
                
            # Split at PRIVMSG
            privmsg_index = line.find("PRIVMSG")
            if privmsg_index < 0:
                return None
                
            # Get author from before PRIVMSG
            before_privmsg = line[:privmsg_index]
            # Extract username (after : and before !)
            colon_index = before_privmsg.rfind(":")
            if colon_index < 0:
                return None
            
            user_section = before_privmsg[colon_index + 1:]
            if "!" not in user_section:
                return None
                
            author = user_section.split("!")[0].strip()
            
            # Get message (after last :)
            last_colon = line.rfind(":")
            if last_colon < 0:
                return None
                
            message = line[last_colon + 1:].strip()
            
            if not author or not message:
                return None
                
            return {
                "author": author,
                "message": message
            }
        except Exception as e:
            print(f">>> Parse error: {e}")
            return None
            
    def disconnect(self):
        """Disconnect from IRC"""
        if self.sock:
            try:
                self.sock.close()
            except:
                pass
        self.connected = False
        logger.info("✓ Disconnected")
