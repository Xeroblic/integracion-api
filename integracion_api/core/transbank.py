import json
import requests


def iniciar_transaccion(monto, metodo_pago):
    url = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/"
    headers = {
        'Tbk-Api-Key-Id': '597055555532',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Content-Type': 'application/json'
    }
    data = {
        "buy_order": "asdasdadasd",
        "session_id": "sdfsdfsdfsdfsdf",
        "amount": monto,
        "return_url": "https://www.tu-sitio.com/retorno"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def obtener_resultado(token):
    url = f"https://webpay3g.transbank.cl/rswebpaytransaction/api/webpay/v1.0/transactions/{token}"
    headers = {
        'Tbk-Api-Key-Id': '597055555532',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers)
    return response.json()

def obtener_estado(token):
    url = f"https://webpay3g.transbank.cl/rswebpaytransaction/api/webpay/v1.0/transactions/{token}"
    headers = {
        'Tbk-Api-Key-Id': '597055555532',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def realizar_reembolso(token, monto):
    url = f"https://webpay3g.transbank.cl/rswebpaytransaction/api/webpay/v1.0/transactions/{token}/refunds"
    headers = {
        'Tbk-Api-Key-Id': '597055555532',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Content-Type': 'application/json'
    }
    data = {
        "amount": monto
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()
