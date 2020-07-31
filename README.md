# qrgen
> Generate QR codes via GET requests!

This was a silly idea I hacked together quickly.  It's surprisingly functional.  The idea is to generate QR codes on demand using a HTTP GET query with URL variables.

## Why?
Good question.

## Deployment
This project is built with `Flask`.  Host the `app.py` just as you would any normal Flask app.  If you're new to Flask deployment, [look here](https://flask.palletsprojects.com/en/1.1.x/deploying/#deployment).

Alternatively to run this on localhost, uncomment the code block in `app.py` surrounding `app.run()` and then run `python app.py` in your terminal.

## Usage
Three variables are currently supported by adding them to the URL:

* `txt` — The text that the QR code will represent.
* `fmt` — The format that the QR code will generate.
* `err` — (Optional) The error correction level of the QR code.

The variables can be set in the URL just like you would expect: `http://localhost:5000/?txt=Hello&fmt=svg&err=M`

The format (`fmt`) can be either:

* `ascii`, which generates an escaped ascii representation of the QR code,
* `svg`, which generates a base-64 encoded `svg+xml` representation of the QR code, or
* `png`, which generates a base-64 encoded `png` representation of the QR code.

The error correction level (`err`) can be either `L`, `M`, `Q`, or `H`.  Please see the [qrcode package](https://github.com/lincolnloop/python-qrcode) for information about this.

## Packages
This project uses `Flask` for deployment,  `qrcode` for generating QR codes (which also depends on `pillow`).

Enjoy!
