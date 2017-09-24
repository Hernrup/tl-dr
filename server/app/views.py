from app import api
import json
from app.response import JsonResponse
import logging

logger = logging.getLogger(__name__)


@api.route('/api/posts', methods=['GET'])
def get_posts():

    response = JsonResponse(
        json.dumps([]),
        status=200
    )
    response.cache_control.no_store = True
    return response


@api.route('/post/<id>', methods=['GET'])
def get_post(id):

    response = JsonResponse(
        json.dumps({}),
        status=200
    )
    response.cache_control.no_store = True
    return response
