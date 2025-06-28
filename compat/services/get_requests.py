import requests

def get_client_demandes(jwt_token):
    url = 'http://localhost:8001/client-demandes-not-satisfied/'

    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/json',
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching demandes: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
