import os
import shutil
from typing import List

BACKUP_DIR = "backups"


def backup_files(file_paths: List[str]) -> List[str]:
    """Create timestamped backups of given files."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backed_up = []
    for path in file_paths:
        if not os.path.exists(path):
            continue
        filename = os.path.basename(path)
        dest = os.path.join(BACKUP_DIR, filename)
        shutil.copy2(path, dest)
        backed_up.append(dest)
    return backed_up
