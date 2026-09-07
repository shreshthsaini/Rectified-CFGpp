---
title: Rectified-CFG++
emoji: 🧭
colorFrom: gray
colorTo: blue
sdk: gradio
sdk_version: 6.26.0
app_file: app.py
pinned: false
license: mit
short_description: On-manifold guidance for flow text-to-image models (NeurIPS 2025)
models:
- stabilityai/stable-diffusion-3.5-medium
---

# Rectified-CFG++ for Flow Based Models

Demo for [Rectified-CFG++](https://arxiv.org/abs/2510.07631) (Saini, Gupta, Bovik; NeurIPS 2025): a training-free predictor-corrector guidance rule for rectified-flow text-to-image models. Generates with Rectified-CFG++ and, side by side, standard classifier-free guidance at the same seed and scale.

Code: https://github.com/shreshthsaini/Rectified-CFGpp · Project page: https://shreshthsaini.github.io/Rectified-CFGpp/

## Running it

The Space needs a GPU and an `HF_TOKEN` secret from an account that has accepted the Stable Diffusion 3.5 license. Set `MODEL_ID` to `stabilityai/stable-diffusion-3.5-large` for the paper's larger backbone.
