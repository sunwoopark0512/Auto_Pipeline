"""Badge generation script."""

import json
from datetime import datetime, timezone
from pathlib import Path


def generate_badges():
    """Generate status badges."""
    # Get current UTC time
    current_time = datetime.now(timezone.utc)
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    
    # Create badges directory if it doesn't exist
    badges_dir = Path("badges")
    badges_dir.mkdir(exist_ok=True)
    
    # Generate time badge
    time_badge = {
        "schemaVersion": 1,
        "label": "UTC Time",
        "message": formatted_time,
        "color": "blue"
    }
    
    with open(badges_dir / "time.json", "w") as f:
        json.dump(time_badge, f)


if __name__ == "__main__":
    generate_badges()
