from django.http import JsonResponse

def api_response(status="success", message="", data=None, http_status=200):
    return JsonResponse({
        "status": status,
        "message": message,
        "data": data,
    }, status=http_status)
