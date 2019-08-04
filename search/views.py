import requests
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import reverse, redirect

from .models import Vocabulary


def search(request):
    return render(request, "search/search_word.html")


def search_word(request):
    if request.is_ajax():
        q = request.GET.get("word", "").lower()
        all_words = Vocabulary.objects.filter(word__icontains=q)
        match_word = all_words.filter(word=q)
        if match_word:
            match_word_id = match_word[0].id
            all_words = all_words.filter(~Q(id__in=[match_word_id]))
        starting_matches = all_words.filter(word__startswith=q).extra(select={'length': 'Length(word)'}).order_by(
            '-frequency', 'length')[:25]
        other_matches = all_words.filter(~Q(id__in=all_words.values_list('id', flat=True))).extra(
            select={'length': 'Length(word)'}).order_by('-frequency', 'length')[:25]
        match_words = [i.word for i in match_word]
        starting_match_words = [obj.word for obj in starting_matches]
        other_match_words = [obj.word for obj in other_matches]

        data = match_words + starting_match_words + other_match_words
        return JsonResponse({"search_result": data}, safe=False)
    else:
        return JsonResponse({"message": "kindly send ajax request"}, status=400)
