from typing import Any

import yaml


def load_config(path: str = "config.yaml") -> dict[str, Any]:
    """Load the YAML config file and return as a dictionary."""
    with open(path, "r", encoding="utf-8") as file:
        config: dict[str, Any] = yaml.safe_load(file)
    return config


def get_config_value(key: str, default: Any = None, path: str = "config.yaml") -> Any:
    """Get a value from the YAML config file by key, with optional default."""
    config: dict[str, Any] = load_config(path)
    return config.get(key, default)
