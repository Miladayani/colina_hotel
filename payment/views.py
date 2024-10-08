import requests
import json

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.conf import settings
from django.http import HttpResponse

from orders.models import Order


def payment_process(request):
    # Get order id from session
    order_id = request.session.get('order_id')
    # Get the order object
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'callback_url': 'http://127.0.0.1:8000',
    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = res.json()

    # بررسی می‌کنیم که آیا پاسخ یک دیکشنری است و کلید 'data' در آن وجود دارد یا خیر
    if isinstance(data, dict) and 'data' in data:
        authority_data = data['data']

        # بررسی می‌کنیم که آیا 'authority' در authority_data وجود دارد
        if 'authority' in authority_data:
            authority = authority_data['authority']
            order.zarinpal_authority = authority
            order.save()
        else:
            # هندل کردن خطای عدم وجود کلید 'authority'
            print("Authority key is missing in the response.")
    else:
        # هندل کردن خطای عدم وجود داده یا اشتباه بودن نوع پاسخ
        print("Response data is not a dictionary or missing 'data' key.")

    # data = res.json()['data']
    # authority = data['authority']
    # order.zarinpal_authority = authority
    # order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect('https://www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')


def payment_callback(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
        }

    request_data = {
        'merchant_id': settings.ZARINPAL_MERCHANT_ID,
        'amount': rial_total_price,
        'authority': payment_authority,
    }

    res = requests.post(
        url='https://api.zarinpal.com/pg/v4/payment/verify.json',
        data=json.dumps(request_data),
        headers=request_header,
    )

    if 'date' in res.json() and ('errors' not in res.json()['data'] or len(res.json()['data']['errors']) == 0):
        data = res.json()['data']
        payment_code = data['code']

        if payment_code == 100:
            order.is_paid = True
            order.ref_id = data['ref_id']
            order.zarinpal_data = data
            order.save()

            return HttpResponse('Success')

        elif payment_code == 101:
            return HttpResponse('success , but before')
        else:
            error_code = res.json()['errors']['code']
            error_message = res.json()['errors']['message']
            return HttpResponse('error')

    else:
        return HttpResponse('error')


def payment_process_sandbox(request):
    # Get order id from session
    order_id = request.session.get('order_id')
    # Get the order object
    order = get_object_or_404(Order, id=order_id)

    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'

    request_header = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    request_data = {
        'MerchantID': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'Amount': rial_total_price,
        'Description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
        'CallbackURL': request.build_absolute_uri(reverse('payment_callback')),
    }

    res = requests.post(zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = res.json()
    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(data['errors']) == 0:
        return redirect('https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error from zarinpal')


def payment_callback_sandbox(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)
    toman_total_price = order.get_total_price()
    rial_total_price = toman_total_price * 10

    if payment_status == 'OK':
        request_header = {
            "accept": "application/json",
            "content-type": "application/json",
        }

        request_data = {
            'MerchantID': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'Amount': rial_total_price,
            'Authority': payment_authority,
        }

        res = requests.post(
            url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json',
            data=json.dumps(request_data),
            headers=request_header,
        )

        if 'errors' not in res.json():
            data = res.json()
            payment_code = data['Status']

            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data['RefID']
                order.zarinpal_data = data
                order.save()

                return HttpResponse('پرداخت شما با موفقیت انجام شد.')

            elif payment_code == 101:
                return HttpResponse('پرداخت شما با موفقیت انجام شد. البته این تراکنش قبلا ثبت شده است!')
            else:
                error_code = res.json()['errors']['code']
                error_message = res.json()['errors']['message']
                return HttpResponse('تراکنش ناموفق بود')

    else:
        return HttpResponse('تراکنش ناموفق بود')