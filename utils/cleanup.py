from datetime import datetime, timedelta
import time

def clean_old_tokens(collection):
    now = int(time.time() * 1000)  # in ms
    cutoff = now - 45 * 60 * 1000  # 45 mins ago

    tokens = collection.find()
    for token in tokens:
        if token.get("update_count", 0) == 0:
            created = token.get("created_at", 0)
            if created < cutoff:
                print(f"🗑 Deleting inactive token: {token['address']}")
                collection.delete_one({"_id": token["_id"]})
