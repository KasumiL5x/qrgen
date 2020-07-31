import qrcode
from io import StringIO

txt = 'https://dgreen.me/'
err = qrcode.constants.ERROR_CORRECT_M

qr = qrcode.QRCode(
    version=1,
    error_correction=err
)
qr.add_data(txt)
qr.make(fit=True)

sio = StringIO()
qr.print_ascii(out=sio)
print(sio.getvalue())

#qr.print_ascii()


#qrcode.make(url).print_ascii()
#qrcode.make(url).save('./qr.png')
