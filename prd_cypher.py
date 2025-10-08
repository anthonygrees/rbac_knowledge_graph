import requests

def executeCypher(query):
    print(query)
    response = requests.post(
        "https://prodaus.api.airia.ai/v1/Graphs/project-graph-7795f113-9dfe-4ecc-be68-b4a17c0684d7/cypher",
        headers={
            "X-API-Key" : "akey-placeholder",
            "Content-Type": "application/json"
            },
            json={
                "query": query
            }
    )
    print("Status Code:", response.status_code)
    print("Response:", response.text)