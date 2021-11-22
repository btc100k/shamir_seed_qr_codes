# shamir_seed_qr_codes

This app encodes and decodes your BIP39 seed words into a set of QR codes.
You specify how many pieces you want to split it into, and how many are the minimum needed to recover your words.

You can then print or upload the QR codes to save in different places.

You're probably going to need to install some python modules. These are the ones I think you'll need.
* pip install mnemonic
* pip install qrcode
* pip install cv2
* pip install pyzbar

I also needed to install zbar on the command line.
On Macintosh, I used:
brew install zbar
