import requests, base64, json
from requests.auth import HTTPBasicAuth
from datetime import datetime
 

consumer_secret = "lC2bNrK0sna60sGn5eKNHEJQhyuLGbDtqZ4NdAv2GgvnDdZIXxTGvAA7mqGaPLAE"
consumer_key = "tnWQLSS6IbyOlP7P91eEaQBe7WVD0Dn96DApWvjc8o3gUcJ0"
short_code = "174379"
pass_key = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
token_api = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
push_api = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
stk_push_query_api = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"
callback_url = "https://1e870b926f35.ngrok-free.app/api/callback"
headers = {}

def get_mpesa_access_token():
    try:
        res = requests.get(token_api,
            auth=HTTPBasicAuth(consumer_key, consumer_secret),
        )
        token = res.json()['access_token']
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        print(headers)
    except Exception as e:
        print(str(e), "error getting access token")
        raise e
    return headers

def generate_password():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password_str = short_code + pass_key + timestamp
    password_bytes = password_str.encode()
    return base64.b64encode(password_bytes).decode("utf-8")

def make_stk_push(amount, phone, sale_id):
    headers = get_mpesa_access_token()
    push_data = {
        "BusinessShortCode": short_code, "Password": generate_password(),
        "Timestamp": datetime.now().strftime("%Y%m%d%H%M%S"), "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount), "PartyA": phone, "PartyB": short_code, "PhoneNumber": phone,
        "CallBackURL": callback_url, "AccountReference": sale_id, "TransactionDesc": "Flask API STKPush",
    }
    response = requests.post(push_api, data=json.dumps(push_data), headers=headers)
    response_data = response.json()
    return response_data




