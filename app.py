import base64
from io import StringIO, BytesIO
from flask import Flask, jsonify, request
import qrcode
import qrcode.image.svg

app = Flask(__name__)

# Formats.
FMT_ASCII = 'ascii'
FMT_SVG = 'svg'
FMT_PNG = 'png'

@app.route('/')
def index():
    TXT_ARG = 'txt'
    FMT_ARG = 'fmt'

    # Get text.
    if TXT_ARG not in request.args:
        return json_msg(f"Error: Missing argument '{TXT_ARG}'."), 400
    txt = request.args[TXT_ARG]
    # Verify text.
    if not len(txt):
        return json_msg(f'Error: Text cannot be empty.'), 400

    # Get format.
    if FMT_ARG not in request.args:
        return json_msg(f"Error: Missing argument '{FMT_ARG}'."), 400
    fmt = request.args[FMT_ARG]
    # Verify format.
    FMT_OPTS = [FMT_ASCII, FMT_SVG, FMT_PNG]
    if fmt not in FMT_OPTS:
        return json_msg(f'Error: Invalid format. Valid types are: {FMT_OPTS}.'), 400

    qr = make_qr(txt, fmt)
    return qr

def json_msg(msg):
    return jsonify(message=msg)

def make_qr(txt, fmt):
    qr = qrcode.QRCode()
    qr.add_data(txt)
    qr.make(fit=True)

    if fmt == FMT_ASCII:
        # Make a custom output stream cast into a string as the func requires it!
        sio = StringIO()
        qr.print_ascii(out=sio)
        return jsonify(image=sio.getvalue())

    if fmt == FMT_SVG:
        img = qr.make_image(image_factory=qrcode.image.svg.SvgImage)
        buff = BytesIO()
        img.save(buff)
        as_bytes = base64.b64encode(buff.getvalue())
        img_str = bytes("data:image/svg+xml;base64,", encoding='utf-8') + as_bytes
        return jsonify(image=img_str.decode('utf-8'))

    if fmt == FMT_PNG:
        img = qr.make_image()
        buff = BytesIO()
        img.save(buff, format='png')
        as_bytes = base64.b64encode(buff.getvalue())
        img_str = bytes("data:image/jpeg;base64,", encoding='utf-8') + as_bytes
        return jsonify(image=img_str.decode('utf-8'))

    return jsonify(msg='Done!') 

if __name__ == '__main__':
    app.run()
