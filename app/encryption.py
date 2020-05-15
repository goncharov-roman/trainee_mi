import os

from pymongo import MongoClient
from pymongo.encryption import (Algorithm, ClientEncryption)

from .db import client, db


local_master_key = os.urandom(96)
kms_providers = {"local": {"key": local_master_key}}

key_vault_namespace = "mydb.__keyVault"
key_vault_db, key_vault_coll = key_vault_namespace.split('.', 1)

key_vault = client[key_vault_db][key_vault_coll]
key_vault.drop()
key_vault.create_index(
    "keyAltNames",
    unique=True,
    partialFilterExpression={"keyAltNames": {"$exists": True}}
)

client_encryption = ClientEncryption(
    kms_providers,
    key_vault_namespace,
    client,
    db.coll.codec_options
)

data_key_id = client_encryption.create_data_key(
    'local', key_alt_names=["trainee_mi"]
)
