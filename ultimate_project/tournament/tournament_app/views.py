from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def test(request):
    return render(request, "test.html", {"touille": "champion du bidule"})


def start_tournament(request):
    print("Tournament was called", flush=True)
    return HttpResponse(
        """
        <div class="overlay">
            <div class="overlay-content">
                <h2>Tournament Oulala</h2>
                <!-- Tournament content -->
                <button hx-get="/" hx-target="body">Close</button>
            </div>
        </div>
    """
    )
