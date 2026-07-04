#!/bin/bash
# Setup cron jobs for pod-ft scheduler on VPS
# Run: bash infra/scripts/setup-cron.sh
# Or manually: crontab -e and paste the line below

CRON_LINE="*/5 * * * * curl -s -o /dev/null -X POST https://vectornode.ru/api/v1/schedules/tick"

# Check if already in crontab
if crontab -l 2>/dev/null | grep -q "schedules/tick"; then
    echo "Cron job already exists. Skipping."
else
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
    echo "Added cron job: $CRON_LINE"
fi

# Verify
echo "Current crontab:"
crontab -l
