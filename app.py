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

# URL args.
TXT_ARG = 'txt'
FMT_ARG = 'fmt'
ERR_ARG = 'err'

# Error correction levels.
ERROR_MAP = {
  'L': qrcode.constants.ERROR_CORRECT_L,
  'M': qrcode.constants.ERROR_CORRECT_M,
  'Q': qrcode.constants.ERROR_CORRECT_Q,
  'H': qrcode.constants.ERROR_CORRECT_H
}
DEFAULT_ERROR = 'M' # Matches the qrcode package's default.

@app.route('/')
def index():
  # Get text.
  txt = get_url_arg(request, TXT_ARG)
  if txt is None:
    return jsonify(error=f"Error: Missing argument '{TXT_ARG}'."), 400
  # Verify text.
  if not len(txt):
    return jsonify(error=f'Error: Text cannot be empty.'), 400

  # Get format.
  fmt = get_url_arg(request, FMT_ARG)
  if fmt is None:
    return jsonify(error=f"Error: Missing argument '{FMT_ARG}'."), 400
  # Verify format.
  FMT_OPTS = [FMT_ASCII, FMT_SVG, FMT_PNG]
  if fmt not in FMT_OPTS:
    available_opts = ', '.join(FMT_OPTS)
    return jsonify(error=f'Error: Invalid format. Valid types are: {available_opts}.'), 400

  # Get error.
  err = get_url_arg(request, ERR_ARG)
  if err is None:
    err = DEFAULT_ERROR # Parameter is optional so don't return an error.
  # Verify error.
  if err not in ERROR_MAP.keys():
    available_opts = ', '.join(list(ERROR_MAP.keys()))
    return jsonify(error=f'Error: Invalid error correction type. Valid types are: {available_opts}.'), 400

  return make_qr(txt, fmt, err)

def get_url_arg(request, name):
  return None if name not in request.args else request.args[name]

def make_qr(txt, fmt, err):
  qr = qrcode.QRCode(
    error_correction = ERROR_MAP[err]
  )
  qr.add_data(txt)
  qr.make(fit=True)

  if fmt == FMT_ASCII:
    sio = StringIO()
    qr.print_ascii(out=sio)
    return jsonify(image=sio.getvalue())

  if fmt == FMT_SVG:
    img = qr.make_image(image_factory=qrcode.image.svg.SvgImage)
    buff = BytesIO()
    img.save(buff)
    img_str = bytes("data:image/svg+xml;base64,", encoding='utf-8') + base64.b64encode(buff.getvalue())
    return jsonify(image=img_str.decode('utf-8'))

  if fmt == FMT_PNG:
    img = qr.make_image()
    buff = BytesIO()
    img.save(buff, format='png')
    img_str = bytes("data:image/jpeg;base64,", encoding='utf-8') + base64.b64encode(buff.getvalue())
    return jsonify(image=img_str.decode('utf-8'))

  # This should never happen as the type is checked elsewhere, but just in case it changes.
  return jsonify(error='Error: Unrecognized format.'), 400

#if __name__ == '__main__':
#  app.run()
