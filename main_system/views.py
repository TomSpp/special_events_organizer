from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Local, Catering, Offer, OtherProvider
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import FilterOffersForm, CommentForm, EstimationForm
from account.models import Profile
from django.contrib import messages


def main_page(request):
    return render(request, 'main_page/main_page.html')


def offer_list(request):
    if request.method == 'GET':
        form = FilterOffersForm()

        locals = Local.objects.all()
        caterings = Catering.objects.all()
        other_offers = OtherProvider.objects.all()
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
            filtered_event = form.cleaned_data['filtered_event']
            tag = get_object_or_404(Tag, name=filtered_event)

            locals = Local.objects.filter(location__district=filtered_location, tags__name__in=[tag])
            caterings = Catering.objects.filter(location__district=filtered_location, tags__name__in=[tag])
            other_offers = OtherProvider.objects.filter(location__district=filtered_location, tags__name__in=[tag])

            for local in locals:
                offers.append(local)
            for catering in caterings:
                offers.append(catering)
            for other_offer in other_offers:
                offers.append(other_offer)

            if len(offers) == 0:
                town_offers = list()
                locals = Local.objects.filter(location__town=filtered_location, tags__name__in=[tag])
                caterings = Catering.objects.filter(location__town=filtered_location, tags__name__in=[tag])
                other_offers = OtherProvider.objects.filter(location__town=filtered_location, tags__name__in=[tag])
                for local in locals:
                    town_offers.append(local)
                for catering in caterings:
                    town_offers.append(catering)
                for other_offer in other_offers:
                    town_offers.append(other_offer)

                if len(town_offers):
                    district = town_offers[0].location.district
                    locals = Local.objects.filter(location__district=district, tags__name__in=[tag])
                    caterings = Catering.objects.filter(location__district=district, tags__name__in=[tag])
                    other_offers = OtherProvider.objects.filter(location__district=district, tags__name__in=[tag])
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

            return render(request, 'main_page/offer_list.html', {'page': page, 'offers': offers,
                                                                 'form': form})


@login_required
def offer_detail(request, year, month, day, provider):
    new_comment = None

    catering = Catering.objects.filter(slug=provider, added__year=year, added__month=month, added__day=day)
    if len(catering) == 0:
        local = Local.objects.filter(slug=provider, added__year=year, added__month=month, added__day=day)
        if len(local) == 0:
            other_provider = OtherProvider.objects.filter(slug=provider, added__year=year,
                                                          added__month=month, added__day=day)
            other_provider = other_provider[0]
            offers = Offer.objects.filter(other_provider=other_provider.id)
            comments = other_provider.comments.filter(active=True)
            if request.method == 'POST':
                comment_form = CommentForm(data=request.POST)
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.name = request.user.username
                    new_comment.other_provider = other_provider
                    new_comment.save()
            else:
                comment_form = CommentForm()
            return render(request, 'main_page/other_offer_detail.html',
                          {'other_provider': other_provider, 'comments': comments,
                           'comment_form': comment_form, 'new_comment': new_comment,
                           'offers': offers})
        else:
            local = local[0]
            offers = Offer.objects.filter(local=local.id)
            comments = local.comments.filter(active=True)
            if request.method == 'POST':
                comment_form = CommentForm(data=request.POST)
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.name = request.user.username
                    new_comment.local = local
                    new_comment.save()
            else:
                comment_form = CommentForm()
            return render(request, 'main_page/local_detail.html',
                          {'local': local, 'offers': offers, 'comments': comments,
                           'comment_form': comment_form, 'new_comment': new_comment})

    catering = catering[0]
    offers = Offer.objects.filter(catering=catering.id)
    comments = catering.comments.filter(active=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.name = request.user.username
            new_comment.catering = catering
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'main_page/catering_detail.html', {'catering': catering, 'comments': comments,
                                                              'offers': offers, 'comment_form': comment_form,
                                                              'new_comment': new_comment})


@login_required
def take_offer(request, offer_id):
    offer = Offer.objects.filter(id=offer_id)
    offer = offer[0]
    profile = Profile.objects.get(user=request.user)
    profile.offers.add(offer)

    return render(request, 'user_panel/offer_added.html', {'offer': offer})

'''
@login_required
def remove_room_offer(request, room_id):
    profile = Profile.objects.get(user=request.user)
    room = profile.rooms.get(id=room_id)
    if request.method == 'POST':
        profile.rooms.remove(room)

        messages.success(request, 'Wybrana oferta została usunięta.')
        return redirect('main_system:user_panel')

    return render(request, 'user_panel/confirm_removing_room_offer.html', {'room': room})


@login_required
def take_offer(request, id, name):
    catering = Catering.objects.filter(id=id, name=name)
    if len(catering) == 0:
        other_offer = OtherOffer.objects.filter(id=id, name=name)
        other_offer = other_offer[0]
        profile = Profile.objects.get(user=request.user)
        profile.other_offers.add(other_offer)
        return render(request, 'user_panel/offer_added.html',
                      {'offer': other_offer})

    catering = catering[0]
    profile = Profile.objects.get(user=request.user)
    profile.caterings.add(catering)

    return render(request, 'user_panel/offer_added.html', {'offer': catering})
'''

@login_required
def remove_offer(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)

    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        profile.offers.remove(offer)
        messages.success(request, 'Wybrana oferta została usunięta.')
        return redirect('main_system:user_panel')

    return render(request, 'user_panel/confirm_removing_offer.html', {'offer': offer})


@login_required
def user_panel(request):
    profile = Profile.objects.get(user=request.user)
    offers = profile.offers.all()

    return render(request, 'user_panel/user_panel.html', {'offers': offers})


@login_required
def estimate_costs(request):
    profile = Profile.objects.get(user=request.user)
    offers = profile.offers.all()
    final_cost = 0

    if request.method == 'POST':
        form = EstimationForm(data=request.POST)
        if form.is_valid():
            people_amount = form.cleaned_data['people_amount']

            for offer in offers:
                if offer.catering is not None:
                    final_cost += offer.cost * people_amount
                else:
                    final_cost += offer.cost

            return render(request, 'user_panel/costs_counting.html', {'form': form,
                                                                      'final_cost': final_cost})
    else:
        form = EstimationForm()
        return render(request, 'user_panel/costs_counting.html', {'offers': offers,
                                                                  'form': form,
                                                                  'final_cost': final_cost})
