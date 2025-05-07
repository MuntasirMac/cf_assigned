from django.shortcuts import render
from .models import Country
from .utils import api_response
from django.http import HttpResponseNotAllowed, JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def country_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET is allowed'}, status=405)
    
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 25)
    countries = Country.objects.all().order_by('name')
    paginator = Paginator(countries, page_size)

    try:
        countries_page = paginator.page(page)
    except EmptyPage:
        return JsonResponse({'error': 'Page out of range'}, status=404)
    if not countries.exists():
        return JsonResponse({'error': 'No countries found'}, status=404)
    
    country_data = []
    for country in countries_page:
        country_data.append({
            'name': country.name,
            'official_name': country.official_name,
            'cca2': country.cca2,
            'languages': country.languages,
            'capital': country.capital,
            'population': country.population,
            'area': country.area,
            'region': country.region,
            'subregion': country.subregion,
            'timezones': country.timezones,
            'currencies': country.currencies,
            'flags': country.flags,
            'coat_of_arms': country.coat_of_arms,
            'flag': country.flag,
        })

    response = {
        "count": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": countries_page.number,
        "has_next": countries_page.has_next(),
        "has_previous": countries_page.has_previous(),
        "data": country_data,
    }
    return JsonResponse(response, status=200)

def country_detail_view(request, id):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        # id = int(id)
        country = Country.objects.filter(id=id).first()
    except Country.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Country not found",
            "data": None
        }, status=404)

    data = {
        "name": country.name,
        "cca2": country.cca2,
        "capital": country.capital,
        "region": country.region,
        "subregion": country.subregion,
        "flag": country.flag,
        "languages": country.languages,
        "population": country.population,
        "area": country.area,
        "timezones": country.timezones,
        "currencies": country.currencies,
        "flags": country.flags,
        "coat_of_arms": country.coat_of_arms,
        "official_name": country.official_name,
    }

    return JsonResponse({
        "status": "success",
        "message": f"Details of country '{country.name}'",
        "data": data
    }, status=200)


@csrf_exempt
def country_create_view(request):
    if request.method != 'POST':
        return api_response("error", "Only POST allowed", None, http_status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return api_response("error", "Invalid JSON", None, http_status=400)

    required_fields = ["name", "official_name", "cca2", "languages", "capital", "population", "region", "flag"]
    missing = [field for field in required_fields if field not in body]
    if missing:
        return api_response("error", f"Missing fields: {', '.join(missing)}", None, http_status=400)

    try:
        country = Country.objects.create(
            name=body["name"],
            official_name=body.get("official_name", ""),
            cca2=body["cca2"],
            languages=body.get("languages", []),
            capital=body["capital"],
            population=body["population"],
            area=body.get("area"),
            region=body["region"],
            subregion=body.get("subregion", ""),
            timezones=body.get("timezones", []),
            currencies=body.get("currencies", []),
            flags=body.get("flags", {}),
            coat_of_arms=body.get("coat_of_arms", {}),
            flag=body["flag"]
        )
    except Exception as e:
        return api_response("error", f"Failed to create country: {str(e)}", None, http_status=500)

    data = {
        "id": country.id,
        "name": country.name,
        "official_name": country.official_name,
        "cca2": country.cca2,
        "languages": country.languages,
        "capital": country.capital,
        "population": country.population,
        "area": country.area,
        "region": country.region,
        "subregion": country.subregion,
        "timezones": country.timezones,
        "currencies": country.currencies,
        "flags": country.flags,
        "coat_of_arms": country.coat_of_arms,
        "flag": country.flag,
    }

    return api_response("success", "Country created successfully", data, http_status=201)