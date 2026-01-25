# BEFORE YOU START - READ THIS (Yes, Really)

## The Hard Truth About Following Tutorials

**These instructions work on MY system:**
- **OS:** Pop!_OS 24.04 (Wayland)
- **GPU:** AMD Radeon RX 7800 XT (16GB VRAM)
- **CPU:** AMD Ryzen 9 5950X
- **RAM:** 64GB
- **Date Tested:** January 2026

**Will it work on YOUR system?** Maybe. Probably. But no guarantees.

Linux is not Windows. Every distribution, every version, every desktop environment can have subtle (or not-so-subtle) differences that break things. **That's not a bug, that's Linux.**

---

## "But It Doesn't Work On My Machine!"

Before you leave a comment saying the guide is broken, check if you're actually running the same setup:

### ❌ Things That Will Definitely Break These Instructions

1. **Different Ubuntu/Pop!_OS Version**
   - **Pop!_OS 22.04 or earlier:** Different package versions, different kernel, different ROCm compatibility
   - **Pop!_OS 24.10+:** Might work, might have newer packages that conflict
   - **Ubuntu 24.10+:** Different repositories, different package names possibly

2. **Non-Ubuntu-Based Distributions**
   - **Fedora/Red Hat/CentOS:** Uses `dnf`/`yum`, not `apt`. Completely different package names.
   - **Arch/Manjaro:** Uses `pacman`. ROCm is in AUR. Different installation process entirely.
   - **OpenSUSE:** Uses `zypper`. Different repos.
   - **Gentoo:** If you're using Gentoo, you don't need my help (and you probably compile ROCm from source anyway).

3. **Different AMD GPU**
   - **RDNA 2 (RX 6000 series):** Should work similarly, might have different gfx target (gfx1030, etc.)
   - **RDNA 1 (RX 5000 series):** Limited ROCm support, may not work at all
   - **Older GCN cards:** Some work, some don't. Check ROCm compatibility list.
   - **Integrated graphics (APUs):** Very limited support, probably won't work for LLM inference

4. **NVIDIA GPU**
   - These instructions are for AMD + ROCm
   - NVIDIA uses CUDA, not ROCm
   - Completely different installation process
   - Ollama auto-detects NVIDIA GPUs with CUDA

5. **Different Display Server**
   - **X11 vs Wayland:** Shouldn't matter for ROCm, but could affect other things
   - **No display server (headless):** Should actually be simpler

---

## Distribution-Specific Differences

### If You're On Pop!_OS/Ubuntu 22.04 (Not 24.04):

**You'll need to change:**
```bash
# Instead of "noble" use "jammy"
echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/rocm.gpg] https://repo.radeon.com/rocm/apt/6.2.4 jammy main" \
  | sudo tee /etc/apt/sources.list.d/rocm.list
```

**Check your codename:**
```bash
lsb_release -c
# Output shows your Ubuntu codename
# 22.04 = jammy
# 24.04 = noble
```

### If You're On Linux Mint:

Linux Mint is based on Ubuntu but with its own versioning:
- **Linux Mint 22:** Based on Ubuntu 24.04 (noble) ✅ Should work
- **Linux Mint 21:** Based on Ubuntu 22.04 (jammy) - use jammy instead of noble
- **Linux Mint 20:** Based on Ubuntu 20.04 (focal) - ROCm 6.2 might not support this

### If You're On Fedora/RHEL:

Sorry, these instructions won't work. You need:
```bash
# Example for Fedora (DO NOT just copy-paste, check official docs)
sudo dnf install rocm-hip-runtime rocminfo rocm-smi
```

**Official guide:** https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/rpm.html

### If You're On Arch/Manjaro:

```bash
# ROCm is in the AUR
yay -S rocm-hip-sdk rocminfo rocm-smi-lib
```

**Official guide:** https://rocm.docs.amd.com/projects/install-on-linux/en/latest/how-to/native-install/arch-install.html

---

## Common "It Doesn't Work" Issues (And Fixes)

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
```

### Issue: "rocm-smi shows 1% GPU usage but 96% VRAM"

**This is NOT an error.** This means:
- Your model is loaded into VRAM ✅
- But some layers are spilling to CPU ❌
- Solution: Use a smaller model

The rocm-smi from Ubuntu repos (5.7.0) also doesn't report RDNA 3 GPU usage accurately. Trust VRAM usage instead.

---

## How To Actually Get Help

If something doesn't work, **don't just comment "it doesn't work."** That's useless.

**Instead, provide:**

1. **Your exact system:**
   ```bash
   # Run these and paste output
   lsb_release -a
   uname -r
   lspci | grep -i vga
   ```

2. **What command failed:**
   ```bash
   # Copy the EXACT command you ran
   # Copy the EXACT error message
   ```

3. **Relevant logs:**
   ```bash
   # For Ollama issues
   sudo journalctl -u ollama -n 100 --no-pager
   
   # For ROCm issues
   rocminfo | head -50
   ```

4. **What you've already tried:**
   - Did you reboot?
   - Did you check you're in the render/video groups?
   - Did you verify the repository was added correctly?

---

## Expected Behavior (So You Know If It's Working)

### ✅ ROCm Is Working If:

```bash
# This shows your GPU
rocminfo | grep -i "marketing name"
# Output: Marketing Name: AMD Radeon RX 7800 XT

# This shows VRAM usage
rocm-smi --showmeminfo vram
# Output shows: VRAM Total Used Memory (B): 15000000000 (or similar high number when model loaded)

# This shows ROCm loaded
sudo journalctl -u ollama -n 50 | grep -i rocm
# Output: found 1 ROCm devices
#         loaded ROCm backend
```

### ✅ GPU Acceleration Is Working If:

**When running a 12B model:**
- GPU power: 180-220W
- VRAM usage: 50-70%
- Speed: 30-60+ tokens/second
- Ollama logs show: "offloaded X/X layers to GPU" (all layers)

**When running a 27B model (on 16GB VRAM):**
- GPU power: 60-100W
- VRAM usage: 90-95%
- Speed: 2-5 tokens/second
- Ollama logs show: "offloaded 47/63 layers" (partial - CPU bottleneck)

### ❌ It's NOT Working If:

- `rocminfo` doesn't show your GPU at all
- VRAM stays at 0% even with model loaded
- Ollama logs show: "loaded CPU backend" but NOT "loaded ROCm backend"
- Speed is super slow (< 2 tokens/sec on any model)

---

## The Bottom Line

**If you're on Pop!_OS 24.04 with an AMD RDNA 2/3 GPU:**
These instructions should work with minimal issues.

**If you're on Ubuntu 24.04 (or derivatives like Mint 22):**
Should work with maybe minor tweaks.

**If you're on anything else:**
You're on your own. Check the official ROCm docs and adapt accordingly.

**If you're using NVIDIA:**
Wrong guide. You need CUDA, not ROCm.

**If you're on Windows:**
This is for Linux. WSL2 might work but is not covered here.

---

## Official Resources (When You Need More Than This Guide)

- **ROCm Official Docs:** https://rocm.docs.amd.com/
- **ROCm Installation Guide:** https://rocm.docs.amd.com/projects/install-on-linux/en/latest/
- **ROCm GPU Support List:** https://rocm.docs.amd.com/projects/install-on-linux/en/latest/reference/system-requirements.html
- **Ollama Documentation:** https://github.com/ollama/ollama/blob/main/docs/gpu.md
- **AMD Community Forums:** https://community.amd.com/t5/rocm/ct-p/amd-rocm

---

## Final Warning

**You are responsible for your own system.**

I'm showing you what worked for me. If it breaks your system, that's on you. Always:
- Make backups
- Read commands before running them
- Understand what `sudo` does (hint: it gives root access)
- Know how to recover if something goes wrong

**If you don't understand what a command does, DON'T RUN IT.**

Google it. Read the man page (`man <command>`). Ask in forums. But don't blindly copy-paste and then complain when something breaks.

---

**Now go read the actual installation guide.**

And yes, I know this document is long. That's because I'm tired of answering the same questions. Read it. Thank me later.
