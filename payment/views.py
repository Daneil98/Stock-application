
import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import DepositForm
from .models import Payment
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


def payment_process(request):
    Payment_id = request.session.get('Payment_id')
    Payment_instance = Payment()
    total_cost = Payment_instance.amount
    if request.method == 'POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount': f'{total_cost:.2f}',
            'payment_method_nonce': 'fake-valid-nonce',
            "options" : {
                "submit_for_settlement": True, # Required
            },  
        })
        
        # create and submit transaction
        if result.is_success:
            Payment_instance = Payment()
            # mark the order as paid
            Payment_instance.paid = True
            # store the unique transaction id
            Payment_instance.braintree_id = result.transaction.id
            #CHeck for duplicate transactions
            Payment.transaction_id = result.transaction.id
            # save the payment
            Payment_instance.save()
            return redirect('payment:done')
        else:
            print(result.message)
            return redirect('payment:canceled')
    else:
    # generate token
        client_token = 'sandbox_rz4k7rvw_qnk7x4t299nm2wdy'
        return render(request, 'process.html', {'Payment': Payment, 'client_token': client_token})

def payment_done(request):
    return render(request, 'payment/done.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')
