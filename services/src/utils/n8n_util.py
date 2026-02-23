import requests

n8n_url = "http://localhost:5678/webhook-test/8c62f956-591f-4698-ab3d-b04f5b71b11d" 
n8n_gen_sum_and_questions_url = "http://localhost:5678/webhook-test/c6cb8338-42ed-4c0d-a5b7-4bf9ed52ee0e"
n8n_gen_following_question_url= "http://localhost:5678/webhook-test/cedff963-3e77-4f9d-b674-d0363039568b"

def post_data(data):
    return requests.post(
        n8n_url,
        json=data,
        timeout=1000
    )

def get_summarize_and_questions(data):
    response = requests.post(
        n8n_gen_sum_and_questions_url,
        json=data,
        timeout=1000
    )

    return response.json()

def get_following_questions(data):
    res = requests.post(
        n8n_gen_following_question_url,
        json=data,
        timeout=1000   
    )

    return res.json()