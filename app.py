from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from services import MercadoPago


app = FastAPI()

templates = Jinja2Templates(
    directory='templates',
)
mp = MercadoPago()


@app.get('/', response_class=HTMLResponse)
async def checkout_page(request: Request):
    return templates.TemplateResponse(
        name='checkout.html',
        context={'request': request},
    )


@app.post('/create_payment')
async def create_payment(request: Request):
    data = await request.json()
    method = data.get('payment_method')
    amount = float(data.get('transaction_amount', 0))
    description = data.get('description')

    try:
        if method == 'card':
            card_data = {
                'card_number': data.get('card_number'),
                'expiration_month': data.get('expiration_month'),
                'expiration_year': data.get('expiration_year'),
                'security_code': data.get('security_code'),
                'cardholder': {
                    'name': data.get('cardholder_name'),
                    'identification': {
                        'type': 'CPF',
                        'number': data.get('identification_number'),
                    },
                },
            }
            installments = data.get('installments')
            payer = {
                'email': data.get('email'),
                'identification': {
                    'type': 'CPF',
                    'number': data.get('identification_number')
                },
            }
            result = mp.pay_with_card(
                amount=amount,
                installments=installments,
                description=description,
                card_data=card_data,
                payer=payer,
            )

        elif method == 'pix':
            payer = {
                'email': data.get('email'),
                'identification': {
                    'type': 'CPF',
                    'number': data.get('identification_number'),
                },
            }
            result = mp.pay_with_pix(
                amount=amount,
                description=description,
                payer=payer,
            )

        elif method == 'boleto':
            payer = {
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email'),
                'identification': {
                    'type': 'CPF',
                    'number': data.get('identification_number')
                },
                'address': {
                    'zip_code': data.get('zip_code'),
                    'street_name': data.get('street_name'),
                    'street_number': data.get('street_number'),
                    'neighborhood': data.get('neighborhood'),
                    'city': data.get('city'),
                    'federal_unit': data.get('federal_unit'),
                },
            }
            result = mp.pay_with_boleto(
                amount=amount,
                description=description,
                payer=payer,
            )

        else:
            raise HTTPException(status_code=400, detail='Método de pagamento inválido')
    
        return JSONResponse(result)

    except RuntimeError as err:
        raise HTTPException(status_code=502, detail=(err))
