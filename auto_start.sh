#!/usr/bin/env bash
set -e

SERVICE_NAME="$(basename "$PWD")"

cat > "${SERVICE_NAME}.service" <<EOF
[Unit]
Description=${SERVICE_NAME}
After=graphical-session.target
Wants=graphical-session.target

[Service]
Type=simple
WorkingDirectory=$PWD
ExecStart=$(command -v uv) run run.py

Environment=DISPLAY=${DISPLAY}
Environment=XAUTHORITY=${XAUTHORITY}
Environment=WAYLAND_DISPLAY=${WAYLAND_DISPLAY}
Environment=XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR}
Environment=DBUS_SESSION_BUS_ADDRESS=${DBUS_SESSION_BUS_ADDRESS}

Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF

mkdir -p ~/.config/systemd/user
mv -f "${SERVICE_NAME}.service" ~/.config/systemd/user/

# Import the current graphical environment into the user manager
systemctl --user import-environment \
    DISPLAY \
    XAUTHORITY \
    WAYLAND_DISPLAY \
    XDG_RUNTIME_DIR \
    DBUS_SESSION_BUS_ADDRESS

systemctl --user daemon-reload
systemctl --user enable "${SERVICE_NAME}.service"
systemctl --user restart "${SERVICE_NAME}.service"

echo
echo "Installed and started:"
echo "  ${SERVICE_NAME}.service"
echo
echo "Useful commands:"
echo "  systemctl --user status ${SERVICE_NAME}"
echo "  journalctl --user -u ${SERVICE_NAME} -f"
echo

systemctl --user --no-pager status "${SERVICE_NAME}"