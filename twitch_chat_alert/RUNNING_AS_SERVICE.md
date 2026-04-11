# Running Twitch Chat Alert as a Background Service

## Windows - Task Scheduler (Recommended)

1. **Open Task Scheduler:** Press `Win + R`, type `taskschd.msc` and press Enter

2. **Create a Basic Task:**
   - Right-click on "Task Scheduler Library" → "Create Basic Task..."
   - Name: `Twitch Chat Alert`
   - Description: `Monitors Twitch chat for messages and plays audio alerts`
   - Click "Next"

3. **Set Trigger:**
   - Select: "At startup"
   - Click "Next"

4. **Set Action:**
   - Action: "Start a program"
   - Program: Find your Python executable
     - Easiest: Run `where python` in PowerShell to find path
     - Example: `C:\Python311\python.exe`
   - Add arguments: `-u c:\Users\Rell\scripts\twitch_chat_alert\main.py`
   - Start in: `c:\Users\Rell\scripts\twitch_chat_alert`
   - Click "Next"

5. **Finish:**
   - Check: "Open the Properties dialog for this task when I click Finish"
   - Click "Finish"

6. **In Properties (Conditions tab):**
   - Uncheck: "Start the task only if the computer is on AC power"
   - Check: "Wake the computer to run this task"

7. **In Properties (Settings tab):**
   - Check: "Run task as soon as possible after a scheduled start is missed"
   - Check: "If the task fails, restart every: 5 minutes" (optional)

## Command Line (Manual Start)

### Simple Start
```powershell
cd c:\Users\Rell\scripts\twitch_chat_alert
python main.py
```

Press `Ctrl+C` to stop.

### Run in Background (PowerShell)
```powershell
Start-Process python -ArgumentList "c:\Users\Rell\scripts\twitch_chat_alert\main.py" -WindowStyle Hidden
```

## Monitoring Logs

Check what the service is doing:
```powershell
Get-Content logs/twitch_alert.log -Tail 20 -Wait
```

## Troubleshooting

**Service won't start:**
- Check that Python path is correct: `python --version`
- Verify `.env` file has `TWITCH_CHANNEL` and `TWITCH_ACCESS_TOKEN` set
- Check logs: `type logs\twitch_alert.log`

**No sound playing:**
- Verify `sounds/default_alert.mp3` exists
- Test sound manually: `python -c "import winsound; winsound.PlaySound('sounds/default_alert.mp3', winsound.SND_FILENAME)"`

**Not receiving messages:**
- Verify OAuth token has `chat:read` scope (check at https://dev.twitch.tv)
- Ensure channel name in `.env` is correct and lowercase
- Check logs for connection errors: `type logs\twitch_alert.log`
