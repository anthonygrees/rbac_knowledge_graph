import requests

def get_graphs():
    out = requests.get("https://prodaus.api.airia.ai/v1/Graphs",
        headers={
        "X-API-Key" : "akey-placeholder"
        }
    )
    print("Status Code:", out.status_code)
    print("Response:", out.text)

get_graphs()