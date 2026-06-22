# WebFax 📠

> A modern reimagining of the classic fax machine, built for the internet age.  
> Send text over the web and have it printed instantly on the other end — just like a fax, but over IP.
>
> No drivers. No setup. Just open a browser, type, and print.

---

## What is WebFax?

FoIP turns any thermal printer into a web-connected fax machine.  
Anyone with a browser can send a message to your printer — instantly, over IP.

Think of it as **Fax over IP (FoIP)** — retro concept, modern tech.

---

## Features

- 🖨️ Print instantly from any browser
- 🌐 Works over local network or the internet
- 🀄 Full Chinese character support (GBK)
- 👁️ Live 58mm receipt preview before printing
- 🔌 Direct USB parallel port support (PL2305)
- 🐧 Linux native, no proprietary drivers needed
- ⚡ Lightweight — just Python + Flask

---

## Requirements

- Linux (Debian/Ubuntu recommended)
- Python 3.8+
- Flask
- Thermal printer with parallel port (DB25)
- Prolific PL2305 USB-to-parallel adapter

---

## Installation

```bash
# Clone the repository
git clone https://github.com/kingdomes/WebFax.git
cd webfax

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install flask

# Edit Info
View the comments in index.py and modify them to your own information.
```

---

## Usage

```bash
# Start the server
python3 index.py
```

Then open your browser and go to:

```
http://your-server-ip:8080
```

Type your message, preview it, and hit **Print**.  
The thermal printer on the other end will print it out instantly.

---

## Hardware Setup

```
Browser → Network → WebFax Server → USB (PL2305) → Parallel Port → Thermal Printer
```

1. Connect the PL2305 USB-to-parallel adapter to your server
2. Connect the DB25 cable to your thermal printer
3. Power on the printer
4. Run WebFax

---

## Configuration

Edit `index.py` to change settings:

| Setting | Default | Description |
|---------|---------|-------------|
| `host` | `0.0.0.0` | Listen address |
| `port` | `8080` | Listen port |
| Encoding | `GBK` | Character encoding |

---

## Run as a Service

```bash
# Copy service file
sudo cp webfax.service /etc/systemd/system/

# Enable and start
sudo systemctl enable webfax
sudo systemctl start webfax
```

---

## License

MIT License — free to use, modify, and distribute.

---

## Inspiration

> The fax machine was the internet before the internet.  
> WebFax brings it back — one thermal print at a time.

---
