from django.shortcuts import render

# Create your views here.
def add(request):
    #Do your regular get method processes here
    if request.POST:
        datapoint=Datapoint()
        datapoint.locLat= request.POST.get("Lat","")
        datapoint.locLong = request.POST.get("Long","")

        #Do something with post data here

    return render_to_response(status=status.HTTP_201_CREATED)
