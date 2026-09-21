from pathlib import Path

from dotenv import dotenv_values


def load_config():
    current_dir = Path(__file__).resolve().parent
    env_file = current_dir / ".env"
    if not env_file.exists():
        raise FileNotFoundError(f"Missing .env in {current_dir}. Copy from .env.example.")
    return dict(dotenv_values(env_file))


config = load_config()
