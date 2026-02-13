import requests
from typing import Literal

BASE_URL = "https://extraetf.com/api-v3/funds/search/full"

def search(sort_by, ordering, limit: int=25, filters=None ):
    raise NotImplementedError("Searching for funds is not implemented, yet")

