from django.shortcuts import render


def match(request):
    return render(request, "match.html", {"truc": "trouffion du bidule"})
