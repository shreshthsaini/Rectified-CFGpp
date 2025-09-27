import torch
from diffusers import StableDiffusion3Pipeline
import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Rectified-CFG++ Demo Script')
    parser.add_argument('--prompt', type=str, required=True,
                      help='Text prompt for image generation')
    parser.add_argument('--negative_prompt', type=str, default="",
                      help='Negative prompt for generation (optional)')
    parser.add_argument('--guidance_scale', type=float, default=4.5,
                      help='Guidance scale for CFG (default: 4.5)')
    parser.add_argument('--num_steps', type=int, default=28,
                      help='Number of inference steps (default: 28)')
    parser.add_argument('--sigma_noise', type=float, default=0.005,
                      help='Sigma noise parameter (default: 0.005)')
    parser.add_argument('--width', type=int, default=1024,
                      help='Output image width (default: 1024)')
    parser.add_argument('--height', type=int, default=1024,
                      help='Output image height (default: 1024)')
    parser.add_argument('--output_dir', type=str, default="./outputs",
                      help='Directory to save generated images (default: ./outputs)')
    parser.add_argument('--seed', type=int, default=42,
                      help='Random seed for reproducibility (default: 42)')
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_args()
    
    # Set random seed for reproducibility
    torch.manual_seed(args.seed)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Initialize the pipeline with Rectified-CFG++
    print("Loading model...")
    pipe = StableDiffusion3Pipeline.from_pretrained(
        "stabilityai/stable-diffusion-3.5-large",
        torch_dtype=torch.bfloat16,
        custom_pipeline="./rect-cfg-SD3-pipeline/"
    )
    pipe.to("cuda")
    
    print(f"Generating image with prompt: {args.prompt}")
    
    # Generate the image
    image = pipe(
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        num_inference_steps=args.num_steps,
        sigma_noise=args.sigma_noise,
        true_cfg=args.guidance_scale,
        width=args.width,
        height=args.height,
    ).images[0]
    
    # Save the generated image
    output_path = os.path.join(args.output_dir, f"output_cfg{args.guidance_scale}_steps{args.num_steps}.png")
    image.save(output_path)
    print(f"Image saved to: {output_path}")

if __name__ == "__main__":
    main() 
