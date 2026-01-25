# BEFORE YOU START – READ THIS (Yes, Really)

## Compatibility & Expectations (Vulkan / Ollama)

This project is designed around **how Ollama actually works today** on modern Linux systems.
Please read this before following any guides or opening issues.

---

## Tested Reference System

These instructions are confirmed to work on the following setup:

- **OS:** Pop!_OS 24.04 (Wayland)
- **GPU:** AMD Radeon RX 7800 XT (16GB VRAM)
- **CPU:** AMD Ryzen 9 5950X
- **RAM:** 64GB
- **Kernel / Mesa:** Stock Pop!_OS 24.04
- **Date Tested:** January 2026

If your system differs, things will *probably* still work — but expectations matter.

---

## The Reality of Linux Tutorials

Linux is not a single platform. Differences in:
- distribution
- kernel version
- Mesa version
- GPU driver stack

can and do affect behavior.

This guide documents **what works**, not universal guarantees.

---

## GPU Acceleration: How It Actually Works

### Vulkan Is Automatic

On supported AMD GPUs, **Ollama automatically uses Vulkan** for GPU acceleration.

You **do not** need to:
- install ROCm
- add repositories
- set environment variables
- edit systemd services
- toggle backends manually

If Vulkan works on your system, Ollama will use it.

---

### What “Supported GPU” Means (Vulkan)

Generally supported:
- **AMD RDNA 2 / RDNA 3 GPUs** (RX 6000 / RX 7000 series)
- Most modern AMD drivers via Mesa

May work with limitations:
- Older AMD GPUs (performance varies)
- Integrated GPUs (limited VRAM = limited model size)

Not covered:
- Very old GPUs without Vulkan compute support

---

## Distribution Notes

### Ubuntu / Pop!_OS / Linux Mint (Recommended)

These distributions provide:
- modern Mesa
- stable Vulkan support
- smooth Ollama experience

Pop!_OS 24.04 and Mint 22 are known-good baselines.

---

### Fedora / Arch / Other Distros

These usually work fine, but:
- package names differ
- Mesa updates may be newer or older
- troubleshooting may require distro-specific knowledge

This guide does not provide distro-specific commands outside Ubuntu-based systems.

---

## How to Verify GPU Acceleration (The Right Way)

### Step 1: Verify Vulkan Exists

```bash
vulkaninfo | head
```

If this prints output (not an error), Vulkan is available.

---

### Step 2: Run a Model

```bash
ollama run gemma3:12b
```

Use any reasonably sized model.

---

### Step 3: Watch Real GPU Activity

In another terminal:

```bash
radeontop
```

If you see GPU usage increase while the model is generating text, **GPU acceleration is working**.

This is the most reliable verification method.

---

## Common Misconceptions (Read This Carefully)

### “I need ROCm for AMD GPUs”
❌ False for Ollama inference.

ROCm is used primarily for **training and research workloads**.
Ollama inference uses Vulkan automatically on supported systems.

---

### “I need to force Vulkan with environment variables”
❌ No.

Modern Ollama builds auto-detect and select the correct backend.

---

### “Wayland vs X11 affects GPU inference”
❌ No.

LLM inference is compute-only and independent of the display server.

---

## Performance Expectations (Reality Check)

### 12B Models
- Fully GPU-resident
- Fast token generation
- Ideal for daily use

### 27B Models (16GB VRAM)
- Partial GPU offload
- Slower generation
- CPU becomes the bottleneck
- Still usable for testing and analysis

This is a **VRAM limitation**, not a driver or Vulkan issue.

---

## If Something Doesn’t Work

Before opening an issue, gather:

```bash
lsb_release -a
uname -r
vulkaninfo | head
ollama list
```

And confirm:
- Vulkan runs
- Ollama runs
- GPU activity appears in `radeontop`

Issues without this information may be closed.

---

## Final Notes

- This project prioritizes **simplicity and correctness**
- No experimental GPU stacks required
- No system-level changes needed beyond standard drivers

If you’re looking to train models or fine-tune LoRAs, this project is **not** aimed at that workflow.

---

**Read this first. Save yourself hours.**
