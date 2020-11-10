from django.shortcuts import render
from .models import Local, Catering, OtherOffer


def offer_list(request):
    locals = Local.objects.all()
    caterings = Catering.objects.all()
    other_offers = OtherOffer.objects.all()

    offers = list()
    for local in locals:
        offers.append(local)
    for catering in caterings:
        offers.append(catering)
    for other_offer in other_offers:
        offers.append(other_offer)

    return render(request, 'main_page/offer_list.html', {'offers': offers})
