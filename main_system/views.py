from django.shortcuts import render
from .models import Local, Catering, OtherOffer, Room, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import FilterOffersForm, CommentForm


def offer_list(request):
    if request.method == 'GET':
        form = FilterOffersForm()

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
        paginator = Paginator(offers, 3)
        page = request.GET.get('page')
        try:
            offers = paginator.page(page)
        except PageNotAnInteger:
            offers = paginator.page(1)
        except EmptyPage:
            offers = paginator.page(paginator.num_pages)

        return render(request, 'main_page/offer_list.html', {'page': page, 'offers': offers, 'form': form})

    else:
        form = FilterOffersForm(request.POST)
        if form.is_valid():
            offers = list()
            filtered_location = form.cleaned_data['filtered_location']

            locals = Local.objects.filter(location__district=filtered_location)
            caterings = Catering.objects.filter(location__district=filtered_location)
            other_offers = OtherOffer.objects.filter(location__district=filtered_location)

            for local in locals:
                offers.append(local)
            for catering in caterings:
                offers.append(catering)
            for other_offer in other_offers:
                offers.append(other_offer)

            if len(offers) == 0:
                town_offers = list()
                locals = Local.objects.filter(location__town=filtered_location)
                caterings = Catering.objects.filter(location__town=filtered_location)
                other_offers = OtherOffer.objects.filter(location__town=filtered_location)
                for local in locals:
                    town_offers.append(local)
                for catering in caterings:
                    town_offers.append(catering)
                for other_offer in other_offers:
                    town_offers.append(other_offer)

                if len(town_offers):
                    district = town_offers[0].location.district
                    locals = Local.objects.filter(location__district=district)
                    caterings = Catering.objects.filter(location__district=district)
                    other_offers = OtherOffer.objects.filter(location__district=district)
                    for local in locals:
                        offers.append(local)
                    for catering in caterings:
                        offers.append(catering)
                    for other_offer in other_offers:
                        offers.append(other_offer)

            offers.sort(key=lambda r: r.added, reverse=True)
            paginator = Paginator(offers, 3)
            page = request.GET.get('page')
            try:
                offers = paginator.page(page)
            except PageNotAnInteger:
                offers = paginator.page(1)
            except EmptyPage:
                offers = paginator.page(paginator.num_pages)

            return render(request, 'main_page/offer_list.html', {'page': page, 'offers': offers, 'form': form})


def offer_detail(request, id, name):
    new_comment = None

    catering = Catering.objects.filter(id=id, name=name)
    if len(catering) == 0:
        local = Local.objects.filter(id=id, name=name)
        if len(local) == 0:
            other_offer = OtherOffer.objects.filter(id=id, name=name)
            other_offer = other_offer[0]
            comments = other_offer.comments.filter(active=True)
            if request.method == 'POST':
                comment_form = CommentForm(data=request.POST)
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.other_offer = other_offer
                    new_comment.save()
            else:
                comment_form = CommentForm()
            return render(request, 'main_page/other_offer_detail.html',
                          {'other_offer': other_offer, 'comments': comments, 'comment_form': comment_form,
                           'new_comment': new_comment})
        else:
            local = local[0]
            rooms = Room.objects.filter(local=local.id).order_by('max_people')
            comments = local.comments.filter(active=True)
            if request.method == 'POST':
                comment_form = CommentForm(data=request.POST)
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.local = local
                    new_comment.save()
            else:
                comment_form = CommentForm()
            return render(request, 'main_page/local_detail.html',
                          {'local': local, 'rooms': rooms, 'comments': comments, 'comment_form': comment_form,
                           'new_comment': new_comment})

    catering = catering[0]
    comments = catering.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.catering = catering
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'main_page/catering_detail.html', {'catering': catering, 'comments': comments,
                                                              'comment_form': comment_form, 'new_comment': new_comment})
