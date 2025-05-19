import uuid
import requests

from decouple import config


class MercadoPago:

    BASE_URL = config('MP_BASE_API_URL')

    def __init__(self):
        self.__access_token = config('MP_ACCESS_TOKEN')
        self.__headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.__access_token}',
        }

    def __post(self, path: str, payload: dict) -> dict:
        url = f'{self.BASE_URL}{path}'
        headers = {**self.__headers, 'X-Idempotency-Key': str(uuid.uuid4())}
        response = requests.post(
            url=url,
            json=payload,
            headers=headers,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError:
            try:
                error = response.json()
            except ValueError:
                error = response.text
            raise RuntimeError(f'Erro MP {response.status_code}: {error}')
        return response.json()

    def __get_card_token(self, card_data: dict) -> str:
        response = self.__post('/v1/card_tokens', card_data)
        return response.get('id')

    def __create_payment(self, payment_payload: dict) -> dict:
        return self.__post('/v1/payments', payment_payload)

    def pay_with_card(self, amount: float, installments: int, description: str, card_data: dict, payer: dict) -> dict:
        token = self.__get_card_token(card_data)
        payload = {
            'transaction_amount': amount,
            'token': token,
            'description': description,
            'installments': int(installments),
            'payer': payer,
        }
        return self.__create_payment(payload)

    def pay_with_pix(self, amount: float, description: str, payer: dict) -> dict:
        payload = {
            'transaction_amount': amount,
            'description': description,
            'payment_method_id': 'pix',
            'payer': payer,
        }
        return self.__create_payment(payload)

    def pay_with_boleto(self, amount: float, description: str, payer: dict) -> dict:
        payload = {
            'transaction_amount': amount,
            'description': description,
            'payment_method_id': 'bolbradesco',
            'payer': payer,
        }
        return self.__create_payment(payload)
