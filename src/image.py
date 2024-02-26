import logging

import torch
from diffusers import AutoPipelineForText2Image
from PIL import Image

from common import IMAGE_DIR, configs, timer


def generate_image(
    model: AutoPipelineForText2Image,
    prompt: str,
    num_inference_steps: int,
    height: int,
    width: int,
) -> Image:
    """_summary_

    Args:
        model (AutoPipelineForText2Image): _description_
        prompt (str): _description_
        num_inference_steps (int): _description_
        height (int): _description_
        width (int): _description_

    Returns:
        np.ndarray: _description_
    """
    img = model(
        prompt=prompt,
        guidance_scale=0.0,
        num_inference_steps=num_inference_steps,
        height=height,
        width=width,
    ).images[0]
    return img


def generate_images(
    model: AutoPipelineForText2Image,
    base_prompt: str,
    prompt_modifiers: list[str],
    n_images: int,
    inference_steps: int,
    height: int,
    width: int,
) -> None:
    """_summary_

    Args:
        model (AutoPipelineForText2Image): _description_
        base_prompt (str): _description_
        prompt_modifiers (list[str]): _description_
        n_images (int): _description_
        inference_steps (int): _description_
        height (int): _description_
        width (int): _description_
    """
    for idx, prompt_modifier in enumerate(prompt_modifiers):
        logger.info(f'Generating images with prompt modifier "{prompt_modifier}"')
        prompt = f"{base_prompt}, {prompt_modifier}."
        prompt_dir = IMAGE_DIR / f"prompt_{idx+1}" / "prompt.txt"
        prompt_dir.parent.mkdir(parents=True, exist_ok=True)
        prompt_dir.write_text(prompt)

        for n_image in range(n_images):
            img = generate_image(
                model,
                prompt,
                inference_steps,
                height,
                width,
            )

            img_path = prompt_dir.parent / f"img_{n_image}.jpg"
            img_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(img_path, quality=100, subsampling=0)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__file__)

logger.info("\n##### Starting step 3 image creation #####\n")

pipeline = AutoPipelineForText2Image.from_pretrained(
    configs["image"]["model_id"],
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
).to(configs["image"]["device"])

# pipeline.enable_attention_slicing() # Not working with MacOS
# pipeline.enable_model_cpu_offload() # Not working with MacOS

with timer("Image creation"):
    generate_images(
        pipeline,
        configs["image"]["prompt"],
        configs["image"]["prompt_modifiers"],
        configs["image"]["n_images"],
        configs["image"]["inference_steps"],
        configs["image"]["height"],
        configs["image"]["width"],
    )
