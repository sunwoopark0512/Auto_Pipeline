#!/bin/bash
# Basic Snort IDS installation script
# Run this script with root or sudo privileges.

set -e

LOG_DIR="/var/log/snort"  # dedicated directory for IDS logs

# Install Snort
apt-get update
apt-get install -y snort  # or replace with suricata

# Ensure log directory exists
mkdir -p "$LOG_DIR"
chown snort:snort "$LOG_DIR"
# Inform about configuration and logging
echo "Edit /etc/snort/snort.conf to specify HOME_NET and other options." >&2

echo "Logs will be written to $LOG_DIR" >&2

systemctl enable snort
systemctl restart snort


