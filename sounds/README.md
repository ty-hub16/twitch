# Alert Sounds

Place your alert sound files in this directory.

## Supported Formats
- MP3
- WAV
- OGG
- FLAC

## Built-in Default
The service comes with a default alert sound: `default_alert.mp3`

## Adding Custom Sounds
1. Place your sound file in this directory
2. Update `config.json`:
   ```json
   "alert": {
     "sound_file": "sounds/my_custom_sound.mp3"
   }
   ```

## Recommended Sound Sources
- Freesound.org (Creative Commons)
- Pixabay.com (royalty-free)
- Epidemic Sound (if licensed)
- Create your own!

**Tip:** Keep sound files under 2MB for quick loading.
