from urllib.parse import quote_plus

API_ID = 20551282
API_HASH = "f2aa48726d861f983ddb5f8f8d044a1e"
BOT_TOKEN = "7018018136:AAFJ3xHuNBRmSXGRm4_0_M1HLvvLYFYMTDA"
SESSION = "BQE5lnIAj4Iynun3rVc-mDGYVFgwy_ofWDswx9zRHUG1KRWmHAtQjmrGS8oLIKiLdfYU8TA7iGWUZEpjNK2jEIDHCD_rBYmCb1keX9shflfp8W9UPN3C92LN48iVbh0q-gsBE4pAlagYVzcz9_7n6-LveWCut0GKqinI3mWGluKk2ADmRfIeOCouFNJC-lwIi09jNZnvBed1nTs3XoF1JZbYfCzarzJP4C9d7P2UuwoDKEt2YnhZ13KnM5wCXB-7afY4GTXGT4W1mLJFIlBVWoCko0N1mU3bGffkeKHTfcFIXm4JyykoXDsMUeDPIWUhK3DXfY4YcMx_cCK77DKLuHUiAD_qtQAAAAGJwFOWAA"
LOG_CHANNEL = -1002110630687
ADMIN = 6606050198

# URL-encode the username and password
username = quote_plus("forpaiduser")
password = quote_plus("EXy9d9MqZznOSc0x")

DATABASE_URI = f"mongodb+srv://{username}:{password}@cluster0.hd6xbja.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
