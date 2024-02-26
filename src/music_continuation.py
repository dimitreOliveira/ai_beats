import logging

import numpy as np
import torch
from audiocraft.models import MusicGen

from common import (
    MUSIC_FINAL_DIR,
    MUSIC_INITIAL_DIR,
    configs,
    get_audio_duration,
    load_audio,
    save_audio,
    timer,
)


def generate_music_continuation(
    model: MusicGen, waveform: torch.Tensor, sampling_rate: int
) -> torch.Tensor:
    """_summary_

    Args:
        model (MusicGen): _description_
        waveform (torch.Tensor): _description_
        sampling_rate (int): _description_

    Returns:
        torch.Tensor: _description_
    """
    music = (
        model.generate_continuation(
            waveform,
            prompt_sample_rate=sampling_rate,
        )
        .cpu()
        .numpy()
    )
    return music


def extend_music(
    music: np.ndarray,
    model: MusicGen,
    sampling_rate: int,
    music_duration,
    max_continuation_duration,
    prompt_music_duration,
) -> np.ndarray:
    """_summary_

    Args:
        music (np.ndarray): _description_
        model (MusicGen): _description_
        sampling_rate (int): _description_
        music_duration (_type_): _description_
        max_continuation_duration (_type_): _description_
        prompt_music_duration (_type_): _description_

    Returns:
        np.ndarray: _description_
    """
    final_music = np.expand_dims(music, axis=(0, 1))  # must have 3 dimensions (1, 1, x)
    current_music_duration = get_audio_duration(final_music, sampling_rate)

    while current_music_duration < music_duration:
        continuation_duration = min(
            max_continuation_duration,
            (music_duration - current_music_duration + prompt_music_duration),
        )
        logger.info(
            (
                f"\tMusic has {current_music_duration}s, ",
                f"generating an extra {continuation_duration - prompt_music_duration}s",
            )
        )
        model.set_generation_params(duration=continuation_duration)

        prompt_music_init = prompt_music_duration * sampling_rate
        init_music = final_music[:, :, :-prompt_music_init]
        prompt_music = final_music[:, :, -prompt_music_init:]
        prompt_music_waveform = torch.from_numpy(prompt_music)

        music = generate_music_continuation(
            model,
            prompt_music_waveform,
            sampling_rate,
        )

        final_music = np.concatenate((init_music, music), axis=-1)
        current_music_duration = get_audio_duration(final_music, sampling_rate)
    return final_music


def continue_music(
    model: MusicGen,
    music_duration: int,
    max_continuation_duration: int,
    prompt_music_duration: int,
) -> None:
    """_summary_

    Args:
        model (pipeline): _description_
        model (MusicGen): _description_
        prompt (str): _description_
        n_music (int): _description_
        music_duration (int): _description_
        initial_music_tokens (int): _description_
        max_continuation_duration (int): _description_
        prompt_music_duration (int): _description_
    """
    for music_path in sorted(
        [p for p in MUSIC_INITIAL_DIR.glob("*.wav") if p.is_file()]
    ):
        logger.info(f'Extending music "{music_path}" to duration of {music_duration}s')
        final_music_path = MUSIC_FINAL_DIR / music_path.name
        final_music_path.parent.mkdir(parents=True, exist_ok=True)
        print(final_music_path)

        sampling_rate, music = load_audio(str(music_path))
        print(sampling_rate, music.shape)

        music = extend_music(
            music,
            model,
            sampling_rate,
            music_duration,
            max_continuation_duration,
            prompt_music_duration,
        )

        save_audio(music, sampling_rate, str(final_music_path))


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("\n##### Starting step 2 music continuation #####\n")

model = MusicGen.get_pretrained(configs["music"]["model_id"])

with timer("Music continuation"):
    continue_music(
        model,
        configs["music"]["music_duration"],
        configs["music"]["max_continuation_duration"],
        configs["music"]["prompt_music_duration"],
    )
