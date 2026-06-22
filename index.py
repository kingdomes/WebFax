from flask import Flask, request, render_template_string
import os
import time

app = Flask(__name__)

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>列印服務</title>
    <style>
        .receipt {
            background: #fffdf5;
            width: 220px;
            padding: 16px 12px;
            font-family: 'Courier New', monospace;
            font-size: 12px;
            color: #1a0a00;
            white-space: pre-wrap;
            word-break: break-all;
            line-height: 1.6;
            border: 1px dashed #ccc;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h2>票據列印</h2>
    <form method="POST" action="/print">
        <textarea name="text" id="text-input" rows="10" cols="40" placeholder="輸入要列印的內容..."></textarea>
        <br><br>
        <button type="button" onclick="showPreview()">預覽</button>
        <button type="submit">列印</button>
    </form>
    <div id="preview-box" style="display:none;">
        <p>58mm 票據預覽：</p>
        <div class="receipt" id="preview-content"></div>
    </div>
    {% if message %}
    <p>{{ message }}</p>
    {% endif %}
    <script>
        function showPreview() {
            const text = document.getElementById('text-input').value;
            document.getElementById('preview-content').textContent = text;
            document.getElementById('preview-box').style.display = 'block';
        }
    </script>
</body>
</html>
def get_printer():
"""
    Auto-detect the printer device node.
    Scans /dev/usb/ for devices starting with 'lp'.
    Returns the first device found (e.g. /dev/usb/lp0),
    or None if no device is available.
    """
    try:
        devices = [f"/dev/usb/{d}" for d in os.listdir("/dev/usb/") if d.startswith("lp")]
        return devices[0] if devices else None
    except:
        # /dev/usb/ does not exist, device is disconnected
        return None

def rebind():
    """
    Re-bind the USB parallel port device to the usblp driver.
    The PL2305 adapter sometimes drops off and needs a soft
    unplug/replug to recover.
    Note: 1-1.4.1:1.0 is the USB bus path of the device.
    This may change if the adapter is plugged into a different port.
    """
    # Unbind the device from the driver (soft unplug)
    os.system("echo '1-1.4.1:1.0' > /sys/bus/usb/drivers/usblp/unbind 2>/dev/null")
    time.sleep(1)
    # Re-bind the device to restore /dev/usb/lp0
    os.system("echo '1-1.4.1:1.0' > /sys/bus/usb/drivers/usblp/bind 2>/dev/null")
    time.sleep(1)

def send_to_printer(text):
    """
    Send text to the thermal printer.
    If the device is not found, attempt a rebind before printing.
    """
    dev = get_printer()
    if not dev:
        # Device not found, try to rebind
        rebind()
        dev = get_printer()
    if not dev:
        return False, "Printer not found"
    try:
        data = b'\x1b\x40'    # ESC @ — initialize printer, clear buffer
        data += b'\x1c\x26'   # FS & — enable Chinese character mode (GBK)
        data += text.encode('gbk', errors='replace')  # encode text as GBK
        data += b'\n\n\n'     # feed paper to expose printed content
        with open(dev, 'wb') as f:
            f.write(data)
        return True, "Print successful"
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/print', methods=['POST'])
def print_text():
    text = request.form.get('text', '')
    success, message = send_to_printer(text)
    return render_template_string(HTML, message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
