import random
# from math import ceil
from decimal import Decimal
# for the Bitcoin-specific stuff
from mnemonic import Mnemonic
import json
import qrcode
from cv2 import imread
from pyzbar import pyzbar

# the SSS implementation came from
# https://www.geeksforgeeks.org/implementing-shamirs-secret-sharing-scheme-in-python/

# Encode
# Convert your words onto BIP39 numbers (24 of them)
# Convert all 24 numbers into SSS shares
# Collate the shares into a big long string.
# Generate QR code from each of the big long strings
# Save the QR code

# Decode
# Turn QR code into string
# Split string into shares.
# Combine with other QR codes & split
# assemble the shares together & decode into numbers
# Numbers back into BIP 39 words



FIELD_SIZE = 10 ** 5

def reconstruct_secret(shares):
    """
    Combines individual shares (points on graph)
    using Lagranges interpolation.

    `shares` is a list of points (x, y) belonging to a
    polynomial with a constant of our key.
    """
    sums = 0
    # prod_arr = []

    for j, share_j in enumerate(shares):
        xj, yj = share_j
        prod = Decimal(1)

        for i, share_i in enumerate(shares):
            xi, _ = share_i
            if i != j:
                prod *= Decimal(Decimal(xi) / (xi - xj))

        prod *= yj
        sums += Decimal(prod)

    return int(round(Decimal(sums), 0))


def polynom(x, coefficients):
    """
    This generates a single point on the graph of given polynomial
    in `x`. The polynomial is given by the list of `coefficients`.
    """
    point = 0
    # Loop through reversed list, so that indices from enumerate match the
    # actual coefficient indices
    for coefficient_index, coefficient_value in enumerate(coefficients[::-1]):
        point += x ** coefficient_index * coefficient_value
    return point


def coeff(t, secret):
    """
    Randomly generate a list of coefficients for a polynomial with
    degree of `t` - 1, whose constant is `secret`.

    For example with a 3rd degree coefficient like this:
        3x^3 + 4x^2 + 18x + 554

        554 is the secret, and the polynomial degree + 1 is
        how many points are needed to recover this secret.
        (in this case it's 4 points).
    """
    local_coeff = [random.randrange(0, FIELD_SIZE) for _ in range(t - 1)]
    local_coeff.append(secret)
    return local_coeff


def generate_shares(n, m, secret):
    """
    Split given `secret` into `n` shares with minimum threshold
    of `m` shares to recover this `secret`, using SSS algorithm.
    """
    coefficients = coeff(m, secret)
    shares = []

    for i in range(1, n + 1):
        x = random.randrange(1, FIELD_SIZE)
        shares.append((x, polynom(x, coefficients)))

    return shares


def assemble_secrets(split_secrets):
    startup = True
    words = []
    word_secrets = []
    for one in split_secrets:
        # This is an array of shares
        if startup:
            count = len(one)
            startup = False
            for x in range(count):
                word_secrets.append([])
        word_index = 0
        for word_secret in one:
            word_secrets[word_index].append(word_secret)
            word_index += 1

    for one_word in word_secrets:
        word_index = reconstruct_secret(one_word)
        words.append(word_list.wordlist[(word_index - 1)])
    return words


class Buckets:
    def __init__(self, count):
        self.bucketsOfShares = []
        for x in range(count):
            self.bucketsOfShares.append([])

    def add_shares(self, shares):
        # print(f'{one} Shares: {", ".join(str(share) for share in shares)}')
        # print("-" * 10)
        bucketindex = 0
        for single in shares:
            self.bucketsOfShares[bucketindex].append(single)
            bucketindex += 1

    def generate_images(self):
        share_index = 0
        for item in self.bucketsOfShares:
            json_string = json.dumps(item)
            qr = qrcode.QRCode(
                version=20,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=8,
                border=5,
            )
            qr.make(fit=True)
            qr.add_data(json_string)
            img = qr.make_image(back_color=(255, 255, 255), fill_color=(0, 0, 0))
            share_index += 1
            img.save("secret-share-{count}.png".format(count=share_index))


class UserInput:
    def __init__(self):
        self.minimum_required = 2
        self.split_count = 5
        self.seedwords = ['cream', 'install', 'pottery', 'banana', 'soon', 'promote', 'industry', 'add', 'sunny',
                          'shuffle', 'save', 'extra', 'permit', 'monkey', 'stock', 'slender', 'luggage', 'stumble',
                          'hotel', 'cube', 'mixture', 'pulse', 'velvet', 'hat']
        self.numberlist = []

    def generate_buckets(self):
        buckets = Buckets(self.split_count)
        for one in self.numberlist:
            shares = generate_shares(self.split_count, self.minimum_required, one)
            # print(f'{one} Shares: {", ".join(str(share) for share in shares)}')
            # print("-" * 10)
            buckets.add_shares(shares)
        return buckets


class WordList:
    def __init__(self):
        mnemo = Mnemonic("english")
        self.wordlist = mnemo.wordlist

    def is_valid(self, word):
        try:
            self.wordlist.index(word)
            return True
        except ValueError:
            return False

    def words_to_numbers(self, words):
        numberlist = []
        for one in words:
            numberlist.append((self.wordlist.index(one) + 1))
        return numberlist


def read_words():
    seedwords = []
    for x in range(500):
        if len(seedwords) == 0:
            word = input('Enter first seed word: ')
        else:
            word = input('Enter next seed word: (#{count}) '.format(count=(len(seedwords) + 1)))
        if len(word) == 0:
            break
        else:
            aslist = word.split(" ")
            if len(aslist) == 12 or len(aslist) == 18 or len(aslist) == 24:
                seedwords = aslist
                break
            else:
                if word_list.is_valid(word):
                    seedwords.append(word)
                else:
                    print("**** Unrecognized Word:", word)
    return seedwords


def do_encode():
    user_input = UserInput()

    print("We are going to take your seed words, and create Shamir’s Secret Sharing QR codes for you to store.")
    print("-" * 20)
    count = input('How many total splits do you want? (Default: {count}) '.format(count=user_input.split_count))
    if len(count) > 0:
        user_input.split_count = int(count)
    print("-" * 20)
    count = input('What minimum number of splits do you want to require? (Default: {count}) '.format(
        count=user_input.minimum_required))
    if len(count) > 0:
        user_input.minimum_required = int(count)
    print("-" * 20)
    print("This is the hard part. You're going to have to type in your seed words.")
    print("You can either enter them one at a time, using a blank line to indicate you are done")
    print("or you can paste in the full list, with each word separated by space")
    # cream install pottery banana soon promote industry add sunny shuffle save extra
    # permit monkey stock slender luggage stumble hotel cube mixture pulse velvet hat
    word = read_words()
    if len(word) == 0:
        print("You didn't enter any seed words, which I understand if you just want to see how this works.")
        print("Let's use some hard coded words to show you how this works.")
        word = user_input.seedwords

    print("-" * 20)
    print("We have {count} words.".format(count=len(word)))
    user_input.seedwords = word
    user_input.numberlist = word_list.words_to_numbers(word)

    buckets = user_input.generate_buckets()
    buckets.generate_images()
    print("Done.")
    print("We created {count} images.".format(count=user_input.split_count))
    print("Print out these QR codes and keep them in separate locations.")
    print("You'll need {count} images to recover your seed words.".format(count=user_input.minimum_required))


def do_decode():
    print("We are going to restore your seed words from a series of images.")
    print("Enter the path to your files one by one.")
    print("Use a blank line to indicate you're done adding images.")
    print("-" * 20)

    segments = []
    for x in range(500):
        # filename = 'secret-share-1.png'
        filename = input('Enter the path of a QR image file? ')
        if len(filename) > 0:
            # read the QRCODE image
            try:
                data = pyzbar.decode(imread(filename))
                # print(data[0].data.decode("utf-8"))
                payload = data[0].data.decode("utf-8")
                from_json = json.loads(payload)
                # print("from json", restoredFromJson)
                segments.append(from_json)
            except Exception:
                print("Failed to load file: {name}".format(name=filename))
        else:
            break

    print("We have {count} segments of the secret.".format(count=len(segments)))
    words = assemble_secrets(segments)
    print("Here are your words:")
    print(" ".join(words))


word_list = WordList()
is_encoding = True
action = input('Are we encoding or decoding? e|d (Default: {action}) '.format(action="e"))
if len(action) > 0:
    if action.lower() == 'd':
        is_encoding = False

if is_encoding:
    do_encode()
else:
    do_decode()
