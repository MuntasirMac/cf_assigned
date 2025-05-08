from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .models import Country
from .utils import api_response
from django.http import HttpResponseNotAllowed, JsonResponse
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import json, re, templates

# Create your views here.
@login_required
def country_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET is allowed'}, status=405)
    
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 25)
    countries = Country.objects.all().order_by('name')
    paginator = Paginator(countries, page_size)
    query = request.GET.get('q', '')
    if query:
        countries = countries.filter(name__icontains=query)

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
    # return JsonResponse(response, status=200)
    context = {
        "countries": countries_page,
        'query': query,
    }
    return render(request, "countries/list.html", context)

@login_required
def country_detail_view(request, id):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    try:
        # id = int(id)
        country = Country.objects.filter(id=id).first()
        same_region = Country.objects.filter(region=country.region).exclude(id=country.id)
        same_language = Country.objects.filter(
        languages__icontains=country.languages[0] if country.languages else ''
    ).exclude(id=country.id)
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

    # return JsonResponse({
    #     "status": "success",
    #     "message": f"Details of country '{country.name}'",
    #     "data": data
    # }, status=200)
    return render(request, 'countries/detail.html', {
        'country': country,
        'same_region': same_region,
        'same_language': same_language,
    })

@login_required
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

@login_required
@csrf_exempt
def country_update_view(request, id):
    if request.method not in ['PUT', 'POST']:
        return api_response("error", "Only PUT or POST allowed", None, http_status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return api_response("error", "Invalid JSON", None, http_status=400)

    country = get_object_or_404(Country, id=id)

    # Update fields only if present in request
    fields = [
        "name", "official_name", "cca2", "languages", "capital", "population", "area",
        "region", "subregion", "timezones", "currencies", "flags", "coat_of_arms", "flag"
    ]
    for field in fields:
        if field in body:
            setattr(country, field, body[field])

    try:
        country.save()
    except Exception as e:
        return api_response("error", f"Failed to update country: {str(e)}", None, http_status=500)

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

    return api_response("success", "Country updated successfully", data, http_status=200)

@login_required
@csrf_exempt
def country_delete_view(request, id):
    if request.method != 'DELETE':
        return api_response("error", "Only DELETE allowed", None, http_status=405)

    # Get country by id
    country = get_object_or_404(Country, id=id)

    try:
        country.delete()
    except Exception as e:
        return api_response("error", f"Failed to delete country: {str(e)}", None, http_status=500)

    return api_response("success", f"Country with ID {id} deleted successfully", None, http_status=204)

@login_required
def same_region_countries_view(request, id):
    if request.method != 'GET':
        return api_response("error", "Only GET allowed", None, http_status=405)

    # Get the target country
    target_country = get_object_or_404(Country, id=id)

    # Fetch countries in the same region, excluding the target country
    same_region_countries = Country.objects.filter(region=target_country.region).exclude(id=id)

    # Serialize the data
    countries_data = [
        {
            "id": country.id,
            "name": country.name,
            "official_name": country.official_name,
            "cca2": country.cca2,
            "languages": country.languages,
            "capital": country.capital,
            "population": country.population,
            "region": country.region,
            "subregion": country.subregion,
            "timezones": country.timezones,
            "currencies": country.currencies,
            "flags": country.flags,
            "coat_of_arms": country.coat_of_arms,
            "flag": country.flag,
        }
        for country in same_region_countries
    ]

    return api_response("success", f"Countries in the same region as {target_country.name}", countries_data)

@login_required
def countries_by_language_view(request):
    if request.method != 'GET':
        return api_response("error", "Only GET allowed", None, http_status=405)

    # Get language from query parameter
    language = request.GET.get('language', None)

    if not language:
        return api_response("error", "Language query parameter is required", None, http_status=400)

    # Case-insensitive regex search for countries that speak the given language
    regex_pattern = f"(?i){re.escape(language)}"  # (?i) for case-insensitive matching
    matching_countries = Country.objects.filter(
        Q(languages__contains=[language]) | Q(languages__regex=regex_pattern)
    )
    # print(len(matching_countries))
    countries_data = [
        {
            "id": country.id,
            "name": country.name,
            "official_name": country.official_name,
            "cca2": country.cca2,
            "languages": country.languages,
            "capital": country.capital,
            "population": country.population,
            "region": country.region,
            "subregion": country.subregion,
            "timezones": country.timezones,
            "currencies": country.currencies,
            "flags": country.flags,
            "coat_of_arms": country.coat_of_arms,
            "flag": country.flag,
        }
        for country in matching_countries
    ]

    return api_response("success", f"Countries that speak {language}", countries_data)

@login_required
def search_country_by_name(request):
    if request.method != 'GET':
        return api_response("error", "Only GET method allowed", None, http_status=405)

    name_query = request.GET.get('name', '').strip()

    if not name_query:
        return api_response("error", "Query parameter 'name' is required", None, http_status=400)

    countries = Country.objects.filter(name__icontains=name_query)

    country_data = [
        {
            "id": country.id,
            "name": country.name,
            "official_name": country.official_name,
            "cca2": country.cca2,
            "languages": country.languages,
            "capital": country.capital,
            "population": country.population,
            "region": country.region,
            "subregion": country.subregion,
            "timezones": country.timezones,
            "currencies": country.currencies,
            "flags": country.flags,
            "coat_of_arms": country.coat_of_arms,
            "flag": country.flag,
        }
        for country in countries
    ]

    return api_response("success", f"Found {len(country_data)} matching countries", country_data)