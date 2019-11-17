from django.shortcuts import render


def postPoint(request):
        if request.method == 'POST':
            if request.POST.get('Lat') and request.POST.get('Long'):
                datapoint=Datapoint()
                datapoint.locLat= request.POST.get("Lat")
                datapoint.locLong = request.POST.get("Long")
                datapoint.save()
                return HttpResponseRedirect('/')

        else:
                return HttpResponse(status=201)
