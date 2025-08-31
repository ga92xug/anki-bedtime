# anki-bedtime
Create a simple bedtime story for unlearned anki cards


# Setup

1. Install ntfy on phone and put in ntfy topic
2. chmod +x ./run.py
3. Automate the creation on start of laptop
    - This guide only works for linux for windows only god can help you
    - ```[Unit]
Description=Generate and send Anki story prompt
After=graphical-session.target
PartOf=graphical-session.target

[Service]
WorkingDirectory=your_dir_here

# Add your environment variable here
Environment="NTFY_TOPIC=your_actual_topic"

# This line imports the necessary GUI variables
ExecStartPre=-/usr/bin/dbus-update-activation-environment --systemd DISPLAY WAYLAND_DISPLAY XDG_CURRENT_DESKTOP

# Your execution command
ExecStart=/usr/bin/python3 your_dir_here/run.py

Restart=on-failure
RestartSec=15

[Install]
WantedBy=default.target```
    - `nano ~/.config/systemd/user/ankiprompt.service`
    - `systemctl --user enable ankiprompt.service`
    - test with `systemd --user start ankiprompt.service`