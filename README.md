# Auto Pipeline

This repository contains scripts for generating and uploading content to Notion using various automation steps.

## Security

An optional intrusion detection system (IDS) can be configured to monitor this environment. See `security/ids_setup.sh` for a simple Snort installation script. Logs are stored in `/var/log/snort` by default.

### Enabling and Monitoring IDS Logs

Run the setup script with root privileges:

```bash
sudo bash security/ids_setup.sh
```

After installation, review `/var/log/snort/` (or your configured directory) to monitor alerts and other IDS output. Rotate or archive these logs regularly to maintain disk space.

