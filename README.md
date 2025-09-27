# Rectified-CFG++ for Flow Based Models

[![ArXiv](https://img.shields.io/badge/arXiv-Soon-blue)](https://arxiv.org/abs/xxxxxxx) [![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)

A **training-free**, **geometry-aware** guidance scheme for flow-based text-to-image (T2I) models. Rectified-CFG++ replaces the naïve extrapolation of classifier-free guidance (CFG) with a predictor–corrector integrator that stays on the learned data manifold, eliminating structural artifacts while improving prompt alignment, generation quality and sampling efficiency.

---
## ✨ Features

- **On-Manifold Sampling**  
  Predictor–corrector updates keep trajectories within a bounded tubular neighborhood of the data manifold.
- **Training-Free**  
  Drop-in replacement for standard CFG—no additional training or fine-tuning required.
- **Model-Agnostic**  
  Works with any transformer-based rectified-flow T2I backbone (e.g., Flux, SD3/3.5, Lumina-Next).
- **Stable Across Scales**  
  Maintains visual fidelity and prompt alignment even at high guidance strengths.
- **Efficient**  
  Achieves state-of-the-art FID and CLIP-Score.

---

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/rectified-cfgpp/Rectified-CFGpp.git
cd Rectified-CFGpp
```

2. Create and activate a virtual environment using the provided YAML configuration file:
```bash
conda env create -f environment.yaml
conda activate rectcfgpp
```

## 🚀 Quick Start

The repository includes a simple demo script (`demo.py`) that allows you to quickly test Rectified-CFG++ with various parameters:

### Basic Usage

Generate an image with default parameters:
```bash
python demo.py --prompt "A magical forest at twilight with glowing fireflies"
```

### Advanced Usage

Customize the generation process with additional parameters:
```bash
python demo.py \
    --prompt "A cyberpunk city at night" \
    --guidance_scale 4.5 \
    --num_steps 35 \
    --width 768 \
    --height 768 \
    --output_dir "./my_generations" \
    --seed 99
```

### Available Parameters

- `--prompt`: Text prompt for image generation (required)
- `--negative_prompt`: Negative prompt for generation (default: "")
- `--guidance_scale`: Guidance scale for CFG (default: 4.5)
- `--num_steps`: Number of inference steps (default: 28)
- `--sigma_noise`: Sigma noise parameter (default: 0.005)
- `--width`: Output image width (default: 1024)
- `--height`: Output image height (default: 1024)
- `--output_dir`: Directory to save generated images (default: "./outputs")
- `--seed`: Random seed for reproducibility (default: 42)

Generated images will be saved in the specified output directory with filenames indicating the guidance scale and number of steps used.

## 📚 Citation
--SOON--

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

