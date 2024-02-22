import logging

import numpy as np
from transformers import pipeline

from common import MUSIC_INITIAL_DIR, configs, get_audio_duration, save_audio, timer


def generate_music(
    model: pipeline, prompt: str, initial_music_tokens: int
) -> np.ndarray:
    """_summary_

    Args:
        model (pipeline): _description_
        prompt (str): _description_
        initial_music_tokens (int): _description_

    Returns:
        np.ndarray: _description_
    """
    music = model(
        prompt,
        forward_params={
            "do_sample": True,
            "max_new_tokens": initial_music_tokens,
        },
    )
    return music


def create_music(
    model: pipeline,
    prompt: str,
    n_music: int,
    initial_music_tokens: int,
) -> None:
    """_summary_

    Args:
        model (pipeline): _description_
        continuation_model (MusicGen): _description_
        prompt (str): _description_
        n_music (int): _description_
        music_duration (int): _description_
        initial_music_tokens (int): _description_
        max_continuation_duration (int): _description_
        prompt_music_duration (int): _description_
    """
    for n in range(n_music):
        logger.info(f"Generating music {n+1} with {initial_music_tokens} tokens")
        music_path = MUSIC_INITIAL_DIR / f"music_{n+1}.wav"
        music_path.parent.mkdir(parents=True, exist_ok=True)

        initial_music = generate_music(
            model,
            prompt,
            initial_music_tokens,
        )
        music = initial_music["audio"]
        sampling_rate = initial_music["sampling_rate"]
        save_audio(music, sampling_rate, str(music_path))

        logger.info(
            f"Music {n+1} generated with {get_audio_duration(music, sampling_rate)}s"
        )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("\n##### Starting step 1 music creation #####\n")

pipe = pipeline(
    task="text-to-audio",
    model=configs["music"]["model_id"],
    device=configs["music"]["device"],
    # torch_dtype=torch.float16,  # Not working with MacOS
)

with timer("Music creation"):
    create_music(
        pipe,
        configs["music"]["prompt"],
        configs["music"]["n_music"],
        configs["music"]["initial_music_tokens"],
    )
