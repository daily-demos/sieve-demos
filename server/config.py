"""Module providing primary input and output configuration paths."""

import os
import uuid

UPLOAD_DIR_ENV = 'UPLOAD_DIR'
OUTPUT_DIR_ENV = 'OUTPUT_DIR'


def ensure_dirs():
    """Creates required file directories if they do not already exist."""
    ensure_dir(UPLOAD_DIR_ENV)
    ensure_dir(OUTPUT_DIR_ENV)


def ensure_dir(env_name: str):
    """Creates directory based on env variable,
    if said directory does not already exist."""
    directory = os.getenv(env_name)
    if not directory:
        directory = env_name
        os.environ[env_name] = directory

    if not os.path.exists(directory):
        os.makedirs(directory)


def get_recordings_dir_path() -> str:
    """Returns MP4 upload directory."""
    return os.path.abspath(os.getenv(UPLOAD_DIR_ENV))


def get_output_dir_path() -> str:
    """Returns final output parent directory."""
    return os.path.abspath(os.getenv(OUTPUT_DIR_ENV))