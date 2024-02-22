import logging
import pprint
import time
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import scipy
import yaml


def parse_configs(configs_path: str) -> dict:
    """Parse configs from the YAML file.

    Args:
        configs_path (str): Path to the YAML file

    Returns:
        dict: Parsed configs
    """
    configs = yaml.safe_load(open(configs_path, "r"))
    logger.info(f"Configs: {pprint.pformat(configs)}")
    return configs


def save_audio(audio: np.ndarray, sampling_rate: int, path: str) -> None:
    """Save and audio file.

    Args:
        audio (np.ndarray): Audio to be saved
        sampling_rate (int): Sampling rate of the audio
        path (str): Path to save the audio
    """
    scipy.io.wavfile.write(
        path,
        data=audio,
        rate=sampling_rate,
    )


def load_audio(path: str) -> tuple[int, np.ndarray]:
    """Save and audio file.

    Args:
        path (str): Path to read the audio
    """
    sampling_rate, audio = scipy.io.wavfile.read(path)
    return sampling_rate, audio


def get_audio_duration(audio: np.ndarray, sampling_rate: int) -> int:
    return audio.shape[-1] // sampling_rate


@contextmanager
def timer(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
    elapsed = time.strftime("%H:%M:%S", time.gmtime(end - start))
    logger.info(f"{label} took {elapsed}")


CONFIGS_PATH = "configs.yaml"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

configs = parse_configs(CONFIGS_PATH)

PROJECT_DIR = Path(f"{configs['project_dir']}/{configs['project_name']}")
IMAGE_DIR = PROJECT_DIR / "images"
VIDEO_DIR = PROJECT_DIR / "videos"
AUDIO_CLIP_DIR = PROJECT_DIR / "audio_clips"
MUSIC_INITIAL_DIR = PROJECT_DIR / "musics" / "initial"
MUSIC_FINAL_DIR = PROJECT_DIR / "musics" / "final"
