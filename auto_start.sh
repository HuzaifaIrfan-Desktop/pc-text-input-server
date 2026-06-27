#!/usr/bin/env bash
set -e

SERVICE_NAME="$(basename "$PWD")"

cat > "${SERVICE_NAME}.service" <<EOF
[Unit]
Description=${SERVICE_NAME}
After=network.target

[Service]
Type=simple
WorkingDirectory=$PWD
ExecStart=$(command -v uv) run run.py
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
EOF



mkdir -p ~/.config/systemd/user
mv "${SERVICE_NAME}.service" ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable --now "${SERVICE_NAME}.service"

echo
echo "Installed and started:"
echo "  ${SERVICE_NAME}.service"
echo
echo "Useful commands:"
echo "  systemctl --user status ${SERVICE_NAME}"
echo "  journalctl --user -u ${SERVICE_NAME} -f"

systemctl --user status ${SERVICE_NAME}