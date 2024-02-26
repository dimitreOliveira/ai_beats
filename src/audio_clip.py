import logging
import random
from itertools import cycle

from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips

from common import AUDIO_CLIP_DIR, MUSIC_FINAL_DIR, VIDEO_DIR, configs, timer


def generate_audio_clip(track_paths, video_prompt_paths, n_loops):
    track_video_prompt_paths = zip(track_paths, cycle(video_prompt_paths))

    for track_path, video_prompt_path in track_video_prompt_paths:
        logger.info(f"Creating audio clip for track '{track_path}'")
        audio_clip_path = AUDIO_CLIP_DIR / f"audio_clip_{track_path.stem}.mp4"
        audio_clip_path.parent.mkdir(parents=True, exist_ok=True)

        audio = AudioFileClip(str(track_path)).audio_loop(n_loops)
        audio_clip_duration = 0
        videos = []

        video_paths = [p for p in video_prompt_path.glob("*.mp4") if p.is_file()]
        random.shuffle(video_paths)
        for video_path in cycle(video_paths):
            video = VideoFileClip(str(video_path))

            if (audio_clip_duration + video.duration) > audio.duration:
                logger.info(
                    f"\tTrimming video to {(audio.duration - audio_clip_duration)}s"
                )
                video = video.subclip(0, (audio.duration - audio_clip_duration))

            logger.info(
                (
                    f"\tClip currently has {audio_clip_duration}s, ",
                    f"adding an extra {video.duration}s from video {video_path.stem}",
                )
            )
            audio_clip_duration += video.duration
            videos.append(video)

            if audio_clip_duration >= audio.duration:
                break

        audio_clip = concatenate_videoclips(videos)
        audio_clip.set_audio(audio).write_videofile(
            str(audio_clip_path),
            verbose=False,
            logger=None,
        )


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("\n##### Starting step 5 audio clip creation #####\n")

track_paths = sorted([p for p in MUSIC_FINAL_DIR.glob("*.wav") if p.is_file()])
video_prompt_paths = sorted([p for p in VIDEO_DIR.glob("prompt_*") if p.is_dir()])

with timer("Audio clip creation"):
    generate_audio_clip(
        track_paths, video_prompt_paths, configs["audio_clip"]["n_music_loops"]
    )
