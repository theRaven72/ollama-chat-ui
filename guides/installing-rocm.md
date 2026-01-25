# Installing ROCm for Ollama on Pop!_OS 24.04 with AMD 7800 XT

## Understanding the Limitation

**Important:** The 7800 XT has 16GB VRAM. For LLM inference:
- ✅ **Models up to 12-14B parameters** will fit entirely on GPU → Fast (30-60+ tokens/s)
- ⚠️ **27B models** will partially fit (some layers spill to CPU) → Slow (~2-5 tokens/s)
- ❌ **Larger models (30B+)** won't fit well

**ROCm won't make 27B models fast on a 7800 XT** - it's a VRAM limitation, not a software issue. Stick with 12B models for best performance.

---

## Clean ROCm Installation

### Step 1: Remove Old ROCm (if present)
```bash
sudo apt purge -y rocm* hip* hsa* amdgpu-install
sudo rm -rf /opt/rocm
sudo rm -rf /etc/apt/sources.list.d/rocm*
sudo rm -rf /var/lib/apt/lists/*rocm*
sudo apt update
```

### Step 2: Add Official ROCm Repository
```bash
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://repo.radeon.com/rocm/rocm.gpg.key \
  | sudo gpg --dearmor -o /etc/apt/keyrings/rocm.gpg

echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.2.4 noble main" \
  | sudo tee /etc/apt/sources.list.d/rocm.list

sudo apt update
```

### Step 3: Install ROCm Runtime
```bash
sudo apt install -y rocm-hip-runtime rocminfo rocm-smi
```

### Step 4: Fix Permissions
```bash
sudo usermod -aG render,video $USER
```

**Then log out and log back in** (or reboot).

### Step 5: Verify Installation
```bash
# Check GPU is detected
rocminfo | grep -E 'Name:|Marketing Name|gfx'

# Should show:
# Name: gfx1101
# Marketing Name: AMD Radeon RX 7800 XT

# Check GPU status
rocm-smi
```

---

## Using Ollama with ROCm

### Ollama Automatically Uses ROCm
Once ROCm is installed, Ollama will automatically detect and use your GPU. **No configuration needed.**

### Verify GPU Usage

**Check VRAM usage:**
```bash
rocm-smi --showmeminfo vram
```

**Monitor GPU during inference:**
```bash
watch -n 1 'rocm-smi --showuse --showmemuse --showpower'
```

**Check Ollama logs:**
```bash
sudo journalctl -u ollama -n 50 | grep -E "offload|device|layers"
```

You should see:
- `found 1 ROCm devices`
- `loaded ROCm backend`
- `offloaded X/X layers to GPU`

---

## Choosing the Right Model

### ✅ Recommended Models for 7800 XT (16GB VRAM)

```bash
# These will fit entirely on GPU
ollama run gemma3:12b
ollama run qwen2.5:14b
ollama run llama3.1:8b
ollama run mistral:7b
```

### ❌ Why 27B Models Are Slow

When you run a 27B model, you'll see in the logs:
```
offloaded 47/63 layers to GPU
model weights device=ROCm0 size="10.8 GiB"
model weights device=CPU size="6.5 GiB"  ← CPU bottleneck!
```

This means 16 layers are stuck on CPU, creating a massive slowdown as each token bounces between GPU and CPU.

---

## Troubleshooting

### Low GPU Usage (1%) But High VRAM (90%+)

This means layers are spilling to CPU. Solutions:

1. **Use a smaller model** (12B instead of 27B)
2. **Try a more compressed quantization:**
   ```bash
   # If using gemma3:27b, try a smaller quant
   ollama pull gemma3:27b-q3_K_M  # More compressed
   ```
3. **Reduce context window:**
   ```bash
   OLLAMA_NUM_CTX=2048 ollama run gemma3:27b
   ```

### Verify CPU vs GPU Work

While running a model:
```bash
# Check if CPU is doing heavy work
top -H -p $(pidof ollama)

# If CPU usage is high, you're in hybrid mode (GPU+CPU)
```

### Check Which Model Is Actually Running

```bash
# List installed models
ollama list

# Check logs for the specific model loaded
sudo journalctl -u ollama -n 30 | grep "architecture\|file_type"
```

---

## Performance Expectations

### With Proper GPU Acceleration (12B models):
- **GPU Usage:** 90-100%
- **Power:** 180-220W
- **Speed:** 30-60+ tokens/second
- **VRAM:** 50-70%

### With 27B Models (Hybrid CPU+GPU):
- **GPU Usage:** 1-10% (misleading metric)
- **Power:** 60-100W
- **Speed:** 2-5 tokens/second
- **VRAM:** 90-95%

---

## Summary

1. **ROCm is working correctly** if you see:
   - High VRAM usage (rocm-smi --showmeminfo vram)
   - ROCm backend loaded in logs
   - GPU detected as gfx1101

2. **For fast inference on 7800 XT:**
   - Stick with 12-14B models
   - They'll fully fit on GPU
   - You'll get 30-60+ tokens/second

3. **27B models will be slow** regardless of ROCm:
   - VRAM limitation forces CPU spillover
   - No software fix for hardware constraint
   - Need 24GB+ VRAM GPU for fast 27B inference

---

## Quick Verification Commands

```bash
# Is ROCm installed?
rocminfo | head -20

# Is my GPU detected?
rocm-smi

# Is Ollama using the GPU?
sudo journalctl -u ollama -f  # Watch while running a model

# How much VRAM is being used?
rocm-smi --showmeminfo vram

# What models do I have?
ollama list
```

---

## Additional Notes

### Common Issues

**Issue: rocm-smi shows "GPU use (%): 1" but VRAM is 96%**
- This is normal when layers spill to CPU
- The old rocm-smi (5.7.0) from Ubuntu repos doesn't report utilization accurately for RDNA 3 GPUs
- Trust the VRAM usage metric instead: `rocm-smi --showmeminfo vram`

**Issue: Model still slow after ROCm install**
- ROCm is working, but model is too large for VRAM
- Switch to a smaller model (12B or 14B)
- Check logs: `sudo journalctl -u ollama -n 50 | grep "offload"`
- Look for "offloaded X/X layers" - if not all layers, that's your bottleneck

**Issue: "No such file or directory: /opt/rocm/bin/rocm-smi"**
- On Pop!_OS, rocm-smi installs to `/usr/bin/rocm-smi`
- Use: `which rocm-smi` to find the correct path
- Or just run: `rocm-smi` (it's in your PATH)

### Best Practices

1. **Always check which model variant you're running:**
   ```bash
   ollama list
   ```

2. **Monitor during first run of each model:**
   ```bash
   watch -n 1 'rocm-smi --showuse --showmemuse --showpower'
   ```

3. **Save your logs when testing:**
   ```bash
   sudo journalctl -u ollama -n 100 > ollama-test.log
   ```

### Hardware Upgrade Path

If you need faster 27B+ model inference:
- **AMD RX 7900 XTX** (24GB VRAM) → Can handle 27B-34B models
- **AMD RX 7900 XT** (20GB VRAM) → Can handle most 27B models
- Your current 7800 XT is excellent for 8-14B models

---

## Resources

- ROCm Documentation: https://rocm.docs.amd.com/
- Ollama Documentation: https://github.com/ollama/ollama
- AMD GPU Support List: https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html

---

**Created for viewers of your stream/channel**  
Last updated: January 2026  
ROCm Version: 6.2.4  
OS: Pop!_OS 24.04 (Ubuntu 24.04 based)  
GPU: AMD Radeon RX 7800 XT
