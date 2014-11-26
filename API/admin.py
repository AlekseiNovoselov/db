from django.http import HttpResponse
import json
from API.Handlers.dbConnection import eDataBase
from tools import requirePost

@requirePost
def clear(request):
    eDataBase.clear(request)
    response_data = {"code": 0, "response": "All Ok"}
    return HttpResponse(json.dumps(response_data), content_type='application/json')



