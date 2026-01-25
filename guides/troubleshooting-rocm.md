# ROCm & GPU Troubleshooting

Issues related to ROCm installation and GPU acceleration for Ollama.

## Post-Installation Issues

### Issue: "rocm-smi: command not found"

**Cause:** ROCm didn't install, or it's in a different path.

**Fix:**
```bash
# Find where it installed
which rocm-smi

# If nothing, check if package is installed
dpkg -l | grep rocm-smi

# If not installed, install it
sudo apt install rocm-smi
```

On Pop!_OS 24.04, rocm-smi typically installs to `/usr/bin/rocm-smi`, not `/opt/rocm/bin/rocm-smi`.

### Issue: "GPU not detected" or "No ROCm devices found"

**Cause:** Either your GPU isn't supported, or you need a reboot, or permissions aren't set.

**Fix:**
```bash
# Check if your GPU is even visible
lspci | grep -i vga

# Check if you're in the right groups
groups
# Should show: render video

# If not, add yourself
sudo usermod -aG render,video $USER
# Then LOG OUT and log back in (or reboot)

# Check /dev/kfd permissions
ls -l /dev/kfd
# Should show: crw-rw---- 1 root render

# Finally, verify ROCm sees it
rocminfo | grep -i "marketing name"
```

### Issue: "Permission denied" on /dev/kfd

**Cause:** You're not in the `render` group, or you didn't log out after adding yourself.

**Fix:**
```bash
# Add yourself to render group
sudo usermod -aG render,video $USER

# LOG OUT and log back in (not just close terminal, actually log out)
# Or reboot

# Verify
groups | grep render
ls -l /dev/kfd
```

### Issue: "Repository not found" or "Unable to locate package"

**Cause:** You're not on Ubuntu 24.04, or you didn't add the repository correctly.

**Fix:**
```bash
# Check your Ubuntu version
lsb_release -a

# Make sure you used the right codename (noble for 24.04)
cat /etc/apt/sources.list.d/rocm.list

# Re-run apt update
sudo apt update
```

For Ubuntu 22.04, you need to use "jammy" instead of "noble" in the repository URL.

## GPU Performance Issues

### Issue: "Ollama still using CPU, not GPU"

**Cause:** Model is too big for your VRAM.

**Fix:**
```bash
# Check how much VRAM you have
rocm-smi --showmeminfo vram

# Check Ollama logs
sudo journalctl -u ollama -n 50 | grep -E "offload|device"

# If you see "offloaded 47/63 layers" (not all layers), your model is too big
# Solution: Use a smaller model
ollama run gemma3:12b  # Instead of 27b
```

**Understanding layer offloading:**
- `offloaded 49/49 layers to GPU` → ✅ All on GPU (fast)
- `offloaded 47/63 layers to GPU` → ⚠️ 16 layers on CPU (slow)
- `model weights device=CPU` → ❌ Running on CPU (very slow)

### Issue: "rocm-smi shows 1% GPU usage but 96% VRAM"

**This is NOT an error.** This means:
- Your model is loaded into VRAM ✅
- But some layers are spilling to CPU ❌
- **Solution:** Use a smaller model

**Additional info:**
The rocm-smi from Ubuntu repos (version 5.7.0) doesn't report RDNA 3 GPU usage percentages accurately. The metric is misleading. Instead, trust:
- **VRAM usage** - `rocm-smi --showmeminfo vram`
- **Power consumption** - High power (180-220W) = GPU working
- **Ollama logs** - Shows actual layer offloading

### Issue: Model still slow after ROCm installation

**Verify it's actually a ROCm problem:**
```bash
# While running a model, check actual GPU activity
watch -n 1 'rocm-smi --showuse --showmemuse --showpower'
```

**What you should see (12B model, fully on GPU):**
- GPU use: 90-100%
- Power: 180-220W
- VRAM: 50-70%

**What indicates CPU bottleneck (27B model on 16GB VRAM):**
- GPU use: 1-10%
- Power: 60-100W
- VRAM: 90-95%

**Fix:** This isn't a ROCm problem - your model is too large. Use gemma3:12b or qwen2.5:14b instead.

### Issue: "ggml_cuda_init: found 0 ROCm devices"

**Ollama isn't detecting ROCm.** 

**Fix:**
```bash
# Verify ROCm is actually installed
rocminfo | grep -i "marketing name"

# Check Ollama can access /dev/kfd
ls -l /dev/kfd

# Restart Ollama service
sudo systemctl restart ollama

# Check logs
sudo journalctl -u ollama -f
```

Then run a model and watch for "found 1 ROCm devices" in the logs.

## Verification Commands

### Check if ROCm sees your GPU:
```bash
rocminfo | grep -E "Name:|Marketing Name|gfx"
```

Expected output:
```
Name:                    gfx1101
Marketing Name:          AMD Radeon RX 7800 XT
```

### Check VRAM usage:
```bash
rocm-smi --showmeminfo vram
```

When a model is loaded, you should see high usage:
```
VRAM Total Used Memory (B): 15000000000  # ~15GB used
```

### Check Ollama is using ROCm:
```bash
sudo journalctl -u ollama -n 50 | grep -i rocm
```

Expected output:
```
ggml_cuda_init: found 1 ROCm devices
load_backend: loaded ROCm backend from /usr/local/lib/ollama/rocm/libggml-hip.so
```

### Monitor GPU during inference:
```bash
watch -n 1 'rocm-smi --showuse --showmemuse --showpower'
```

Run a model in another terminal and watch the stats change.

## Model Size vs VRAM Guide

### For 16GB VRAM (RX 7800 XT):

**✅ Will fit entirely on GPU (fast):**
- 7B-9B models → 30-60+ tokens/s
- 12B-14B models → 25-50+ tokens/s

**⚠️ Will partially fit (slow):**
- 27B models → 2-5 tokens/s (CPU bottleneck)

**❌ Won't fit well:**
- 30B+ models → Very slow or OOM errors

**Solution:** Stick with 12-14B models maximum for best performance.

## Advanced Diagnostics

### Full system check:
```bash
# GPU detected by system?
lspci | grep -i vga

# ROCm sees GPU?
rocminfo | grep "Marketing Name"

# Correct permissions?
groups | grep render
ls -l /dev/kfd

# Ollama running?
systemctl status ollama

# Which backend is Ollama using?
sudo journalctl -u ollama -n 100 | grep -E "backend|ROCm|CUDA|CPU"
```

### rocm-smi --interval flag doesn't work

The Ubuntu/Pop!_OS version of rocm-smi (5.7.0) doesn't support the `--interval` flag.

**Workaround:**
```bash
watch -n 1 rocm-smi
```

## Getting Help

When reporting ROCm issues, provide:

```bash
# Your system info
lsb_release -a
uname -r
lspci | grep -i vga

# ROCm status
rocminfo | head -50
rocm-smi --showmeminfo vram

# Ollama logs
sudo journalctl -u ollama -n 100 --no-pager

# Permission check
groups
ls -l /dev/kfd
```

## Official Resources

- **ROCm Official Docs:** https://rocm.docs.amd.com/
- **ROCm GPU Support List:** https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html
- **Ollama GPU Documentation:** https://github.com/ollama/ollama/blob/main/docs/gpu.md
- **AMD Community Forums:** https://community.amd.com/t5/rocm/ct-p/amd-rocm

---

**Still stuck? Make sure you've read [COMPATIBILITY.md](COMPATIBILITY.md) first.**
