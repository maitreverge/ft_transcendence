# from django.shortcuts import render
from django.http import HttpResponse


def api_gateway(request):
    return HttpResponse(
        """
        <div class="overlay">
            <div class="overlay-content">
                <h2>api_gateway Oulala</h2>
            </div>
        </div>
    """
    )
