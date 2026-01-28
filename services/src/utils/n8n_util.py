import requests

n8n_url = "http://localhost:5678/webhook-test/8c62f956-591f-4698-ab3d-b04f5b71b11d" 

def post_data(data):
    requests.post(
        n8n_url,
        json=data,
        timeout=10
    )