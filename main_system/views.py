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

    offers.sort(key=lambda r: r.added, reverse=True)

    return render(request, 'main_page/offer_list.html', {'offers': offers})


def offer_detail(request, id, name):
    catering = Catering.objects.filter(id=id, name=name)
    if len(catering) == 0:
        local = Local.objects.filter(id=id, name=name)
        if len(local) != 0:
            return render(request, 'main_page/local_detail.html', {'local': local})
        else:
            other_offer = OtherOffer.objects.filter(id=id, name=name)
            return render(request, 'main_page/other_offer_detail.html', {'other_offer': other_offer})

    return render(request, 'main_page/catering_detail.html', {'catering': catering})
