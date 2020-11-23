from django.shortcuts import render, get_object_or_404, redirect
from .models import Local, Catering, OtherOffer, Room
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import FilterOffersForm, CommentForm
from account.models import Profile
from django.contrib import messages


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
            filtered_event = form.cleaned_data['filtered_event']
            tag = get_object_or_404(Tag, name=filtered_event)

            locals = Local.objects.filter(location__district=filtered_location, tags__name__in=[tag])
            caterings = Catering.objects.filter(location__district=filtered_location, tags__name__in=[tag])
            other_offers = OtherOffer.objects.filter(location__district=filtered_location, tags__name__in=[tag])

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
                other_offers = OtherOffer.objects.filter(location__town=filtered_location, tags__name__in=[tag])
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
                    other_offers = OtherOffer.objects.filter(location__district=district, tags__name__in=[tag])
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


def take_room_offer(request, id, name, room_id):
    local = Local.objects.filter(id=id, name=name)
    local = local[0]
    room = Room.objects.filter(id=room_id, local=local)
    room = room[0]
    profile = Profile.objects.get(user=request.user)
    profile.rooms.add(room)

    return render(request, 'user_panel/offer_added.html', {'offer': room})


def remove_room_offer(request, room_id):
    profile = Profile.objects.get(user=request.user)
    room = profile.rooms.get(id=room_id)
    profile.rooms.remove(room)

    rooms = profile.rooms.all()
    caterings = profile.caterings.all()
    other_offers = profile.other_offers.all()

    offers = list()
    room_offers = list()
    for catering in caterings:
        offers.append(catering)
    for other_offer in other_offers:
        offers.append(other_offer)
    for room in rooms:
        room_offers.append(room)

    return render(request, 'user_panel/user_panel.html', {'offers': offers, 'room_offers': room_offers})


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


def remove_offer(request, id, name):
    catering = Catering.objects.filter(id=id, name=name)
    if len(catering) == 0:
        other_offer = OtherOffer.objects.filter(id=id, name=name)
        other_offer = other_offer[0]
        profile = Profile.objects.get(user=request.user)
        profile.other_offers.remove(other_offer)

        rooms = profile.rooms.all()
        caterings = profile.caterings.all()
        other_offers = profile.other_offers.all()

        offers = list()
        room_offers = list()
        for catering in caterings:
            offers.append(catering)
        for other_offer in other_offers:
            offers.append(other_offer)
        for room in rooms:
            room_offers.append(room)

        return render(request, 'user_panel/user_panel.html', {'offers': offers, 'room_offers': room_offers})

    catering = catering[0]
    profile = Profile.objects.get(user=request.user)
    profile.caterings.remove(catering)

    rooms = profile.rooms.all()
    caterings = profile.caterings.all()
    other_offers = profile.other_offers.all()

    offers = list()
    room_offers = list()
    for catering in caterings:
        offers.append(catering)
    for other_offer in other_offers:
        offers.append(other_offer)
    for room in rooms:
        room_offers.append(room)

    return render(request, 'user_panel/user_panel.html', {'offers': offers, 'room_offers': room_offers})


def user_panel(request):
    profile = Profile.objects.get(user=request.user)
    rooms = profile.rooms.all()
    caterings = profile.caterings.all()
    other_offers = profile.other_offers.all()

    offers = list()
    room_offers = list()
    for catering in caterings:
        offers.append(catering)
    for other_offer in other_offers:
        offers.append(other_offer)
    for room in rooms:
        room_offers.append(room)

    return render(request, 'user_panel/user_panel.html', {'offers': offers, 'room_offers': room_offers})
