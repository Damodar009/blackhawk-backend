import os
import sys
from alembic import command
from alembic.config import Config

def run_migrations():
    """
    Run Alembic migrations programmatically.
    Equivalent to running `alembic upgrade head` in the terminal.
    """
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Add project root to sys.path so we can import app modules if needed
    sys.path.insert(0, project_root)
    
    # Path to alembic.ini
    alembic_ini_path = os.path.join(project_root, "alembic.ini")
    
    # Create Alembic configuration object
    alembic_cfg = Config(alembic_ini_path)
    
    # Set the script location explicitly (optional, but good for safety)
    alembic_cfg.set_main_option("script_location", os.path.join(project_root, "migrations"))
    
    print(f"Running migrations using config: {alembic_ini_path}")
    
    try:
        command.upgrade(alembic_cfg, "head")
        print("Migrations completed successfully.")
    except Exception as e:
        print(f"Error running migrations: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations()
