import logging

import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import export_to_video, load_image

from common import IMAGE_DIR, VIDEO_DIR, configs, timer


def generate_video(
    model,
    n_continuations,
    decode_chunk_size,
    motion_bucket_id,
    noise_aug_strength,
    video_fps,
    loop_video,
):
    for prompt_dir in sorted([p for p in IMAGE_DIR.glob("*/") if p.is_dir()]):
        for cover in sorted([p for p in prompt_dir.glob("*.jpg") if p.is_file()]):
            logger.info(f'Generating video for cover "{prompt_dir.stem}/{cover.stem}"')
            all_frames = []
            frames = [load_image(str(cover))]

            for n_continuation in range(n_continuations):
                logger.info(f"Generating set of frames: {n_continuation+1}")
                frames = model(
                    frames[-1],
                    decode_chunk_size=decode_chunk_size,
                    motion_bucket_id=motion_bucket_id,
                    noise_aug_strength=noise_aug_strength,
                    generator=generator,
                ).frames[0]

                all_frames.extend(frames)

            video_path = VIDEO_DIR / prompt_dir.stem / f"{cover.stem}.mp4"
            video_path.parent.mkdir(parents=True, exist_ok=True)
            if loop_video:
                frames_continuous = all_frames + all_frames[-2::-1]
                export_to_video(frames_continuous, str(video_path), fps=video_fps)
            else:
                export_to_video(all_frames, str(video_path), fps=video_fps)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("\n##### Starting step 4 video creation #####\n")

pipeline = StableVideoDiffusionPipeline.from_pretrained(
    configs["video"]["model_id"],
    # torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
).to(configs["video"]["device"])

# pipeline.unet = torch.compile(pipeline.unet, mode="reduce-overhead", fullgraph=True)
# pipeline.enable_model_cpu_offload()

generator = torch.manual_seed(configs["seed"])

with timer("Video creation"):
    generate_video(
        pipeline,
        configs["video"]["n_continuations"],
        configs["video"]["decode_chunk_size"],
        configs["video"]["motion_bucket_id"],
        configs["video"]["noise_aug_strength"],
        configs["video"]["video_fps"],
        configs["video"]["loop_video"],
    )
