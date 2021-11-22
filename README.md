# shamir_seed_qr_codes

This app encodes and decodes your BIP39 seed words into a set of QR codes.
You specify how many pieces you want to split it into, and how many are the minimum needed to recover your words.

You can then print or upload the QR codes to save in different places.

# Don't Trust. Verify.
* Before you melt your titanium plates to slag, get familiar with what this code is doing.
  * Shamir Secrets encode a number, but you want to store BIP39 seed words, so how is that working?
  * https://en.wikipedia.org/wiki/Shamir%27s_Secret_Sharing
  * The Shamir Secret parts of this code came from https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/
* The words are converted to their BIP39 number (1-2048)
* Each seed word number is converted into multiple parts (shares) which can be used to reconstruct the original number.
* The first share from each word is joined into a JSON array and encoded into a QR code.
  * The second/third/etc share of each word is joined with the respective shares from other words, turned into JSON, and then into a QR code.
* So the QR codes represent a JSON array of shares of your words.
* When you decode, the python code converts the QR codes to JSON, then joins the shares into their BIP39 word numbers.
* The array of word numbers is then converted back into words for you to enter into your hardware wallet.

# Running

This is a python script, so you'll run on the command line by typing:
* python3 ./secrets.py

Then you follow the prompts.
* You'll have to decide if you're turning your seed words into QR codes (encoding) or turning QR codes into your seed words (decoding)
  * Default is to [e]ncode

# Running - Encoding
* You'll have to decide into how many pieces you want your seed split. (5 is the default)
* You'll have to decide how many pieces you want to require to decode your seed words. (2 is the default)
* You'll have to type in your seed words.
  * You've been told this is a bad idea, and I agree.
  * You should *only* do this on a computer you're sure doesn't have viruses
  * You should *only* do this on a computer that is not connected to the internet.
  * You can paste all your words at once (with a space between the words) or enter them one at a time.
  * If you do not enter any words, a hard-coded set will be used so you can see how this works.
* The program then creates a bunch of png files (secret-share-#.png) which you then save in various places.

# Running - Decoding
* You'll have to enter the full path to pictures of the QR codes.
  * One at a time.
* Enter a blank line after you've entered all QR codes
* The app prints out your seed words
  * Make sure no one is looking over your shoulder.

# Installation

Hopefully you have python3 installed.

You're probably going to need to install some python modules. These are the ones you'll need.
* pip3 install mnemonic
* pip3 install qrcode
* pip3 install opencv-python
* (install zbar, but this is platform specific. See below)
* pip3 install pyzbar

If you have trouble installing opencv-python, like I did on my Raspberry Pi
* pip3 install --upgrade pip setuptools wheel
* (Then you go back to pip3 install opencv-python)

# Installing zbar
On Macintosh, I used:
* brew install zbar

On Raspberry Pi, I used:
* sudo apt-get install zbar-tools
* sudo apt-get install python-zbar
* sudo apt-get install libzbar0
