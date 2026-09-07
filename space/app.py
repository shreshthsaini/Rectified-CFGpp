"""Rectified-CFG++ demo: flow-model text-to-image with on-manifold guidance.

Generates one image with Rectified-CFG++ (NeurIPS 2025) and, optionally, the
same seed with standard classifier-free guidance so the two can be compared.
Backbone: Stable Diffusion 3.5 (gated; set HF_TOKEN in the Space secrets).
"""

import os
import traceback

import gradio as gr
import torch

try:
    import spaces  # ZeroGPU
except ImportError:  # local run or plain GPU hardware
    class spaces:  # noqa: N801
        @staticmethod
        def GPU(*args, **kwargs):
            if args and callable(args[0]):
                return args[0]
            return lambda f: f

MODEL_ID = os.environ.get("MODEL_ID", "stabilityai/stable-diffusion-3.5-medium")
LOAD_MODEL = os.environ.get("LOAD_MODEL", "1") == "1"
HAS_GPU = torch.cuda.is_available()
DEVICE = "cuda" if HAS_GPU else "cpu"

pipe = None
vanilla = None
load_error = None

if LOAD_MODEL and HAS_GPU:
    try:
        from diffusers import StableDiffusion3Pipeline

        pipe = StableDiffusion3Pipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.bfloat16,
            custom_pipeline=os.path.join(os.path.dirname(os.path.abspath(__file__)), "rect_cfgpp"),
        )
        pipe.to(DEVICE)
        # Standard CFG pipeline sharing every weight with the Rectified-CFG++ one.
        vanilla = StableDiffusion3Pipeline(**pipe.components)
        vanilla.to(DEVICE)
    except Exception:  # surfaced in the UI instead of crashing the Space
        load_error = traceback.format_exc()


def _round16(x):
    return int(x) // 16 * 16


@spaces.GPU(duration=150)
def generate(prompt, negative_prompt, guidance_scale, num_steps, sigma_noise, width, height, seed, compare):
    if pipe is None:
        raise gr.Error(
            "Model is not loaded. This Space needs a GPU (ZeroGPU or larger) and an HF_TOKEN "
            "secret with access to the gated Stable Diffusion 3.5 weights."
        )
    if not prompt or not prompt.strip():
        raise gr.Error("Enter a prompt.")
    width, height = _round16(width), _round16(height)
    seed = int(seed)
    # The corrector's noise injection draws from the global RNG, so seed it too.
    torch.manual_seed(seed)
    g = torch.Generator(device=DEVICE).manual_seed(seed)
    ours = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt or "",
        true_cfg=float(guidance_scale),
        sigma_noise=float(sigma_noise),
        num_inference_steps=int(num_steps),
        width=width,
        height=height,
        generator=g,
    ).images[0]
    base = None
    if compare:
        g2 = torch.Generator(device=DEVICE).manual_seed(seed)
        base = vanilla(
            prompt=prompt,
            negative_prompt=negative_prompt or "",
            guidance_scale=float(guidance_scale),
            num_inference_steps=int(num_steps),
            width=width,
            height=height,
            generator=g2,
        ).images[0]
    return ours, base


EXAMPLES = [
    ["A red fox standing on a mossy log in a misty pine forest, morning light, photograph", "", 4.5, 28, 42],
    ["An astronaut reading a newspaper on a park bench on the Moon, Earth in the sky, film still", "", 7.0, 28, 7],
    ["A ceramic teapot shaped like a snail, studio product photo, soft shadows", "", 9.0, 28, 3],
    ["Watercolor painting of a lighthouse on a cliff during a storm", "blurry, text", 5.5, 28, 11],
]

DESCRIPTION = """
# Rectified-CFG++ for Flow Based Models

Training-free, geometry-aware guidance for rectified-flow text-to-image models. Standard classifier-free guidance
extrapolates off the learned data manifold, which shows up as over-saturation and broken structure at high scales.
Rectified-CFG++ replaces that extrapolation with a predictor-corrector update that stays on the manifold, so you can
push the guidance scale higher and keep prompt alignment without the artifacts.

Left: Rectified-CFG++. Right (optional): the same seed with standard CFG at the same scale. Try scales of 7 to 10 to see the gap.

[Paper (arXiv 2510.07631)](https://arxiv.org/abs/2510.07631) · [Code](https://github.com/shreshthsaini/Rectified-CFGpp) · [Project page](https://shreshthsaini.github.io/Rectified-CFGpp/) · NeurIPS 2025
"""

with gr.Blocks(title="Rectified-CFG++") as demo:
    gr.Markdown(DESCRIPTION)
    if pipe is None:
        why = "no GPU is attached" if not HAS_GPU else "the model failed to load"
        gr.Markdown(
            f"**The model is not loaded because {why}.** The UI is here so you can see the controls; "
            "generation needs ZeroGPU (or a larger GPU) and an `HF_TOKEN` secret that has accepted the "
            f"[{MODEL_ID}](https://huggingface.co/{MODEL_ID}) license."
            + (f"\n\n```\n{load_error[-1500:]}\n```" if load_error else "")
        )
    with gr.Row():
        with gr.Column(scale=1):
            prompt = gr.Textbox(label="Prompt", lines=3, placeholder="Describe the image")
            negative = gr.Textbox(label="Negative prompt", lines=1, value="")
            scale = gr.Slider(1.0, 12.0, value=4.5, step=0.5, label="Guidance scale (applies to both)")
            steps = gr.Slider(8, 50, value=28, step=1, label="Steps")
            with gr.Accordion("More", open=False):
                sigma = gr.Slider(0.0, 0.02, value=0.005, step=0.001, label="Corrector noise sigma")
                width = gr.Slider(512, 1280, value=1024, step=16, label="Width")
                height = gr.Slider(512, 1280, value=1024, step=16, label="Height")
                seed = gr.Number(value=42, precision=0, label="Seed")
            compare = gr.Checkbox(value=True, label="Also render standard CFG with the same seed")
            run = gr.Button("Generate", variant="primary")
        with gr.Column(scale=2):
            with gr.Row():
                out_ours = gr.Image(label="Rectified-CFG++", type="pil")
                out_base = gr.Image(label="Standard CFG (same seed)", type="pil")
    run.click(generate, [prompt, negative, scale, steps, sigma, width, height, seed, compare], [out_ours, out_base])
    gr.Examples(EXAMPLES, inputs=[prompt, negative, scale, steps, seed])
    gr.Markdown(
        "```bibtex\n@inproceedings{saini2025rectifiedcfgpp,\n  title     = {Rectified-CFG++ for Flow Based Models},\n"
        "  author    = {Shreshth Saini and Shashank Gupta and Alan C. Bovik},\n"
        "  booktitle = {Advances in Neural Information Processing Systems},\n  year      = {2025}\n}\n```"
    )

if __name__ == "__main__":
    demo.launch()
