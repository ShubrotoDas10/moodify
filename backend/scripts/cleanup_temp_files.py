"""
Script to manually cleanup temporary files
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.file_handlers import cleanup_old_files
from app.core.logging_config import log


if __name__ == "__main__":
    log.info("Running manual cleanup...")
    cleanup_old_files()
    log.info("Cleanup completed")
