import requests

DEFAULT_HEADERS = {'Accept': 'application/json','Connection': 'Keep-Alive'}

def get_issuer(org_id, CONFIG):
    return requests.get(url=CONFIG["BASE_URL"] + "organizations/" + str(org_id), headers=DEFAULT_HEADERS).json()["label"]