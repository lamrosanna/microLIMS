from django.shortcuts import render
import requests
bars=[]
# Create your views here.
def home(request): 
    response = requests.get('https://freegeoip.app/json/').json()
    lat = response['latitude']
    lon = response['longitude']
    response2 = requests.get('https://api.openbrewerydb.org/breweries?by_dist='+str(lat)+','+str(lon)+"'").json()
    data={}
    k=0
    for item in response2:
        data[k] = item
        k+=1
        print(item['name']+ ', '+item['brewery_type'] )
    return render(request, 'apitest1/index.html',{
        'barlist': data,
    })


    def home2(request):
        # someone makes an api request to YOUR api
        # When that request comes in, you take THEIR IP Address
        # Plug that IP Address into the Gecode API
        # Serialize the result, and take the city portion and store it into a variable
        # Plug the city portion into the brewery API
        breweryResponse = requests.get('https://api.openbrewerydb.org/breweries?by_city=anaheim').json()