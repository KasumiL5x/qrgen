import qrcode

txt = 'https://dgreen.me/'
err = qrcode.constants.ERROR_CORRECT_M

qr = qrcode.QRCode(
    version=1,
    error_correction=err
)
qr.add_data(txt)
qr.make(fit=True)

qr.print_ascii()

#qrcode.make(url).print_ascii()
#qrcode.make(url).save('./qr.png')
