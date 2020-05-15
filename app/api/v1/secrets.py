import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter
from pymongo.encryption import (Algorithm)

from app.encryption import client_encryption, data_key_id
from app.db import db


router = APIRouter()


@router.get("/generate")
def generate(secret: str, phrase: str, ttl: int = None):
    '''Insert encrypted secret into DB and return secret_key to user

    :Parameters:
      - 'secret': The user's secret to store.
      - 'phrase': Code phrase to receive secret in time.
      - 'ttl': Time-to-live in seconds.

    :Returns:
      Secret_key of document in DB.
    '''

    id = str(uuid.uuid4())
    
    encrypted_phrase = client_encryption.encrypt(
        phrase,
        Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic,
        key_id=data_key_id
    )
    encrypted_secret = client_encryption.encrypt(
        secret,
        Algorithm.AEAD_AES_256_CBC_HMAC_SHA_512_Deterministic,
        key_id=data_key_id
    )
    
    document = {
        "_id": id,
        "expire_at": datetime.utcnow() + timedelta(seconds=ttl) if ttl is not None else None,
        "phrase": encrypted_phrase,
        "secret": encrypted_secret
    }
    db.coll.insert_one(document)
    return {"secret_key": id}


@router.get("/secrets/{secret_key}")
def get_secret(secret_key: str, phrase: str):
    '''Get encrypted secret from DB by phrase, decrypt it and return to user

    :Parameters:
      - 'secret_key': The secret key of document in DB.
      - 'phrase': Code phrase to receive secret.

    :Returns:
      Secret stored in DB.
    '''

    document = db.coll.find_one({"_id": secret_key})
    if not document or client_encryption.decrypt(document["phrase"]) != phrase:
        return {"secret": None}

    secret = client_encryption.decrypt(document["secret"])
    db.coll.delete_many({"_id": secret_key})
    return {"secret": secret}
    