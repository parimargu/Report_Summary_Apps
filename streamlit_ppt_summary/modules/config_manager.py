import yaml
import os

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_env_var(key):
    return os.getenv(key)
