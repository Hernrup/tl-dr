from error import BadRequestError, NotFoundError
import json
from . import api, JsonResponse
import http.client


@api.errorhandler(BadRequestError)
def bad_request(error):
    return JsonResponse(json.dumps({'error': str(error)}), 404)


@api.errorhandler(NotFoundError)
def not_found_error(error):
    return JsonResponse(json.dumps({'error': str(error)}), 404)


@api.errorhandler(NotImplementedError)
def not_implemented_error(error):
    err = {
        'error': 'This function is not implemented yet. {}'.format(str(error))
    }
    return JsonResponse(json.dumps(err), http.client.NOT_IMPLEMENTED)
