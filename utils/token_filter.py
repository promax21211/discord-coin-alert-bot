def is_strong_token(data):
    try:
        cap = float(data.get("fdv", 0))
        vol = float(data.get("volume", 0))
        return cap > 30000 and vol > 50000
    except:
        return False
