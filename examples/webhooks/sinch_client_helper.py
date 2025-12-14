from pathlib import Path
from sinch import SinchClient
from dotenv import dotenv_values


def load_config() -> dict[str, str]:
    """
    Load configuration from the .env file in the webhooks directory.

    Returns:
        dict[str, str]: Dictionary containing configuration values
    """
    # Get the directory where this file is located
    current_dir = Path(__file__).resolve().parent
    env_file = current_dir / '.env'

    if not env_file.exists():
        raise FileNotFoundError(f"Could not find .env file in webhooks directory: {env_file}")

    config_dict = dotenv_values(env_file)

    return config_dict


def get_sinch_client(config: dict) -> SinchClient:
    """
    Create and return a configured SinchClient instance.

    Args:
        config (dict): Dictionary containing configuration values
    Returns:
        SinchClient: Configured Sinch client instance
    """
    project_id = config.get('SINCH_PROJECT_ID')
    key_id = config.get('SINCH_KEY_ID')
    key_secret = config.get('SINCH_KEY_SECRET')

    return SinchClient(
        project_id=project_id,
        key_id=key_id,
        key_secret=key_secret,
    )
