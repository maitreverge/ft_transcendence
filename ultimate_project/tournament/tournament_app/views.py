from django.shortcuts import render
from django.http import HttpResponse
import requests
# Create your views here.
from django.http import JsonResponse

def test(request):
    return render(request, "test.html", {"touille": "champion du bidule"})


def start_tournament(request):
	print("START TOURNAMENT", flush=True)
	data = requests.get("http://ctn-match:8002/match/new-match/").json() #! opti url and gateway!
	print(data, flush=True)
	# return JsonResponse(data, status= 201)
	return render(request, "test.html", {"matchData": data})
	return HttpResponse(
        """
        <div class="overlay">
            <div class="overlay-content">
                <h2>Tournament Oulali</h2>
                <!-- Tournament content -->
                <button hx-get="/" hx-target="body">Close</button>
            </div>
        </div>
    """
    )


