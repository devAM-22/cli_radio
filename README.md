# CLI_Radio

A command-line internet radio player built in Python using the MPV media player and the RadioBrowser API.

The application allows users to browse, search, and play radio stations by country, manage favorites, and control playback directly from the terminal.

---

## ✨ Features

- 🎧 Stream internet radio stations using MPV
- 🌍 Browse stations by country
- 🔎 Search stations by name
- 🎲 Random station generator
- ⭐ Save and manage favorite stations (JSON storage)
- 🔊 Volume control (0–100)
- ⚙️ Startup configuration via `config.json`
- 🖥️ Simple CLI-based interface

---

## 🧰 Tech Stack

- Python 3.14+ (tested on 3.14.5)
- MPV Media Player (libmpv)
- pyradios (RadioBrowser API)
- JSON (local storage)

---

## 🔨 Build tools

- Nuitka (used to compile the application into an executable)

---

## 📦 Installation

### Install MPV Media Player (Windows)

Download and install MPV:
```bash
winget install mpv
```
Make sure `libmpv` is available in your MPV installation directory (e.g. `C:\Program Files\MPV Player`).

### Environment setup (Windows)

Virtual environment for developing can easily be setup by running `setup.bat` in the root folder.

### Install MPV Media Player (Linux)

MPV is usually pre-installed in most common Linux distributions. However if this is not the case you can install it by using your package manager:


#### Debian/Ubuntu

```bash
sudo apt install mpv
```

#### Fedora

```bash
sudo dnf install mpv
```

#### Arch/Manjaro

```bash
sudo pacman -S mpv
```

It's essential that `libmpv` is installed.

### Environment setup (Linux)

Similarly to Windows, virtual environment for developing can easily be setup by running `setup.sh` in the root folder.

---

### ▶️ How to run?

Standalone executables for Linux and Windows are available in releases page. Note that executable needs to be in the same file path as `config.json` and `icon.txt`.

---
## License

This project is licensed under the MIT License.

Third-party dependencies are licensed separately and remain subject to their respective licenses:

- python-mpv
- libmpv
- pyradios