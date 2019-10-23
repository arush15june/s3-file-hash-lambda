import logging
from Crypto.Hash import SHA256, SHA3_256
import base64

logger = logging.getLogger('crypter')

""" 
    SHA256, SHA3-256 Hashing utility.
"""

def read_file_data(path: bytes):
    """ Read file data.

    :param path str: path to read from. 
    
    :return bytes: bytestring of file data.
    """
    logger.debug(f'Reading File: {path}')
    with open(path, 'rb') as f:
        return f.read()

def _hash_data(hasher: object, byte_data: bytes):
    """ 
        Hash data using supplied hasher object.
    
        :param hasher object; Hasher from Crypto.Hash supplied to function. [ex. SHA256, SHA3_256, etc].
        :param byte_data bytes: bytes to be hashed.

        :return bytes: generated hash value.
    """
    return hasher.new(data=byte_data).digest()

def hash_sha_256(byte_data: bytes):
    """ 
        Generate SHA256 hash of the passed bytes.

        :param byte_data bytes: bytes to be hashed.

        :return bytes: generated hash value.
    """
    digest = _hash_data(SHA256, byte_data)
    encoded_digest = base64.b64encode(digest)

    return encoded_digest

def hash_sha3_256(byte_data: bytes):
    """ 
        Generate SHA3-256 hash of the passed bytes.

        :param byte_data bytes: bytes to be hashed.

        :return bytes: generated hash value.
    """
    digest = _hash_data(SHA3_256, byte_data)
    encoded_digest = base64.b64encode(digest)
    
    return encoded_digest