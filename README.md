# Shamir Secret Sharing for your Seed Words
This app encodes and decodes your seed words into a set of Shamir Secret Shares. You will get either QR codes or JSON text strings to save.
You specify how many shares you want to split it into, and how many are needed to recover your words.

You can then print or upload the QR or JSON to save in different places.

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
* If you encode your seed with this method and then 10 or 100 years later cannot get this code to run, you can still recover your seed as follows:
  * Assuming QR code readers still exist, you pull the text out of the QR codes.
    * Each QR code holds a JSON array of one shares for each word.
  * Separate the elements from each share, in order, into separate documents.
  * You'll need to find some code that can decode a Shamir secret, or you'll have to figure out the math. The python code on the Wikipedia page should be easy to run once you have the JSON data from the QR codes.

# Running
There are two versions of this code. One which creates QR codes, and the other which creates JSON text.

You'll run the QR code version on the command line by typing:
* python3 ./secrets.py

You'll run the text version on the command line by typing:
* python3 ./text_secrets.py

Then you follow the prompts.
* You'll have to decide if you're turning your seed words into QR codes (encoding) or turning QR codes into your seed words (decoding)
  * Default is to [e]ncode

# Running - Encoding
* You'll have to decide into how many shares you want your seed split. (5 is the default)
* You'll have to decide how many shares you want to require (threshold) to decode your seed words. (2 is the default)
* You'll have to type in your seed words.
  * You've been told this is a bad idea, and I agree.
  * You should *only* do this on a computer you're sure doesn't have viruses
  * You should *only* do this on a computer that is not connected to the internet.
  * You can paste all your words at once (with a space between the words) or enter them one at a time.
  * If you do not enter any words, a hard-coded set will be used so you can see how this works.
* The program then creates a bunch of shares which you then save in various places.
  * Either as png files (secret-share-#.png)
  * Or as a long string of letters and square braces

# Running - Decoding
* You'll have to enter the the whole JSON string, or the full path to pictures of the QR codes.
  * One at a time.
* Enter a blank line after you've entered all input
* The app prints out your seed words
  * Make sure no one is looking over your shoulder.

# Installation
Hopefully you have python3 installed.

You're probably going to need to install some python modules.

These are the ones you'll need for the JSON text version:
* pip3 install mnemonic

These are the ones you'll need for the QR code version:
* pip3 install mnemonic
* pip3 install qrcode
* (see below) pip3 install opencv-python
* (install zbar, but this is platform specific. See below)
* pip3 install pyzbar

# Installing zbar
On Macintosh, I used:
* brew install zbar

On Raspberry Pi, I used:
* sudo apt-get install zbar-tools
* sudo apt-get install python-zbar
* sudo apt-get install libzbar0

# opencv-python
On an Raspberry Pi 4B, I could not get OpenCV to install through pip.
I performed these steps
* (optional) pip3 install --upgrade pip setuptools wheel
  * This might not be necessary, but I did try it before finally succeeding
* (optional) pip3 install cmake
* (optional) sudo apt install ninja-build
* I followed the directions here: https://pimylifeup.com/raspberry-pi-opencv/
* sudo apt install build-essential pkg-config git
* sudo apt install python3-dev
* git clone https://github.com/opencv/opencv.git
* git clone https://github.com/opencv/opencv_contrib.git
* mkdir ~/opencv/build
* cd ~/opencv/build
* cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D BUILD_TESTS=OFF \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D CMAKE_SHARED_LINKER_FLAGS=-latomic \
    -D BUILD_EXAMPLES=OFF ..
* make
* sudo make install
* sudo ldconfig
* From here, I went back to install zbar & pyzbar
  * The make command took several hours, so be prepared.



