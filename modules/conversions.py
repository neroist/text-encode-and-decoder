import base64
import hashlib
from urllib.parse import quote, unquote
import unicodedata


msg_encoding = "ascii"

def b85encode(message): return base64.b85encode(message.encode(msg_encoding, errors='replace')).decode(msg_encoding, errors='replace')
def b85decode(message): return base64.b85decode(message.encode(msg_encoding)).decode(msg_encoding, errors='replace')

def b64encode(message): return base64.b64encode(message.encode(msg_encoding, errors='replace')).decode(msg_encoding, errors='replace')
def b64decode(message): return base64.b64decode(message.encode(msg_encoding, errors='replace')).decode(msg_encoding, errors='replace')

def b32encode(message): return base64.b32encode(message.encode(msg_encoding, errors='replace')).decode(msg_encoding, errors='replace')
def b32decode(message): return base64.b32decode(message.encode(msg_encoding, errors='replace')).decode(msg_encoding, errors='replace')

def b16encode(message): return base64.b16encode(message.encode(msg_encoding, errors='replace')).decode(msg_encoding, errors='replace')
def b16decode(message): return base64.b16decode(message.encode(msg_encoding, errors='replace')).decode(msg_encoding, errors='replace')

def a85encode(message): return base64.a85encode(message.encode(msg_encoding, errors='replace')).decode(msg_encoding, errors='replace')
def a85decode(message): return base64.a85decode(message.encode(msg_encoding, errors='replace')).decode(msg_encoding, errors='replace')


# other stuff
def urlencode(message): return quote(message)
def urldecode(message): return unquote(message)

def md5encode(message): return str(hashlib.md5(message.encode()).hexdigest())

def sha1encode(message): return str(hashlib.sha1(message.encode()).hexdigest())
def sha224encode(message): return str(hashlib.sha224(message.encode()).hexdigest())
def sha384encode(message): return str(hashlib.sha384(message.encode()).hexdigest())
def sha256encode(message): return str(hashlib.sha256(message.encode()).hexdigest())
def sha512encode(message): return str(hashlib.sha512(message.encode()).hexdigest())


encodings = {
    "base85": b85encode,
    "base64": b64encode,
    "base32": b32encode,
    "base16": b16encode,
    "ascii85": a85encode,
    "url": urlencode,
    "md5": md5encode,
    "sha256": sha256encode,
    "sha1": sha1encode,
    "sha512": sha512encode,
    "sha224": sha224encode,
    "sha384": sha384encode
} # added 2 new encrytion methods

supported_encodings = tuple(encodings.keys())

decodings = {
    "base85": b85decode,
    "base64": b64decode,
    "base32": b32decode,
    "base16": b16decode,
    "ascii85": a85decode,
    "url": urldecode
}

supported_decodings = tuple(decodings.keys())
