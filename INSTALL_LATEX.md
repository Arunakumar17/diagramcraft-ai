# Installing LaTeX on Windows

## ✅ Good News!
Your AI generation is working perfectly! You just need LaTeX to compile the diagrams.

---

## Option 1: MiKTeX (Recommended - Smaller Download)

### Quick Install
1. Download: https://miktex.org/download
2. Run the installer
3. Choose "Install for all users" or "Just for me"
4. **Important**: During installation, set "Install missing packages" to **"Yes"** (auto-install)
5. Complete installation (takes ~5-10 minutes)

### After Installation
Restart your terminal (close and reopen PowerShell), then run:
```bash
pdflatex --version
```

You should see version info. Then restart the backend:
```bash
cd C:\Users\user\Desktop\diagramcraft-ai\backend
python main.py
```

---

## Option 2: TeX Live (Full Featured - Larger Download)

1. Download: https://www.tug.org/texlive/windows.html
2. Run `install-tl-windows.exe`
3. Follow the installer (takes longer, ~4GB)
4. Restart terminal after installation

---

## Option 3: Docker (No Local Install Needed)

If you don't want to install LaTeX locally:

1. Install Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Stop current backend server (Ctrl+C)
3. Run from project root:
```bash
cd C:\Users\user\Desktop\diagramcraft-ai
docker-compose up
```

This will use the pre-configured Docker image with LaTeX already installed.

---

## Quick Test After Installation

Once LaTeX is installed, test it:

```bash
pdflatex --version
```

You should see something like:
```
MiKTeX-pdfTeX 4.x (MiKTeX x.x)
```

Then restart your backend and try generating a diagram again! 🎉

---

## Estimation
- **MiKTeX**: ~300MB download, 10 min install
- **TeX Live**: ~4GB download, 30+ min install  
- **Docker**: ~2GB download, 15 min setup

**Recommendation**: Use **MiKTeX** for quickest setup!
