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
        other_providers= OtherProvider.objects.all()
        providers = list()

        for local in locals:
            providers.append(local)
        for catering in caterings:
            providers.append(catering)
        for other_provider in other_providers:
            providers.append(other_provider)

        providers.sort(key=lambda r: r.added, reverse=True)
        paginator = Paginator(providers, 3)
        page = request.GET.get('page')
        try:
            providers = paginator.page(page)
        except PageNotAnInteger:
            providers = paginator.page(1)
        except EmptyPage:
            providers = paginator.page(paginator.num_pages)

        return render(request, 'main_page/offer_list.html', {'page': page, 'providers': providers, 'form': form})

    else:
        form = FilterOffersForm(request.POST)
        if form.is_valid():
            providers = list()
            filtered_location = form.cleaned_data['filtered_location']
            filtered_event = form.cleaned_data['filtered_event']
            tag = get_object_or_404(Tag, name=filtered_event)

            locals = Local.objects.filter(location__district=filtered_location, tags__name__in=[tag])
            caterings = Catering.objects.filter(location__district=filtered_location, tags__name__in=[tag])
            other_providers = OtherProvider.objects.filter(location__district=filtered_location, tags__name__in=[tag])

            for local in locals:
                providers.append(local)
            for catering in caterings:
                providers.append(catering)
            for other_offer in other_providers:
                providers.append(other_offer)

            if len(providers) == 0:
                town_providers = list()
                locals = Local.objects.filter(location__town=filtered_location, tags__name__in=[tag])
                caterings = Catering.objects.filter(location__town=filtered_location, tags__name__in=[tag])
                other_providers = OtherProvider.objects.filter(location__town=filtered_location, tags__name__in=[tag])
                for local in locals:
                    town_providers.append(local)
                for catering in caterings:
                    town_providers.append(catering)
                for other_provider in other_providers:
                    town_providers.append(other_provider)

                if len(town_providers):
                    district = town_providers[0].location.district
                    locals = Local.objects.filter(location__district=district, tags__name__in=[tag])
                    caterings = Catering.objects.filter(location__district=district, tags__name__in=[tag])
                    other_offers = OtherProvider.objects.filter(location__district=district, tags__name__in=[tag])
                    for local in locals:
                        providers.append(local)
                    for catering in caterings:
                        providers.append(catering)
                    for other_offer in other_offers:
                        providers.append(other_offer)

            providers.sort(key=lambda r: r.added, reverse=True)
            paginator = Paginator(providers, 3)
            page = request.GET.get('page')
            try:
                providers = paginator.page(page)
            except PageNotAnInteger:
                providers = paginator.page(1)
            except EmptyPage:
                providers = paginator.page(paginator.num_pages)

            return render(request, 'main_page/offer_list.html', {'page': page, 'providers': providers,
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
            return render(request, 'main_page/other_provider_detail.html',
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
            messages.success(request, 'Twój komentarz został dodany')
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
                                                                      'offers': offers,
                                                                      'final_cost': final_cost})
    else:
        form = EstimationForm()
        return render(request, 'user_panel/costs_counting.html', {'offers': offers,
                                                                  'form': form,
                                                                  'final_cost': final_cost})
