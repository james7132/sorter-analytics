# from google.cloud import bigquery
from werkzeug.exceptions import BadRequest
import flask
import util
import datetime


# client = bigquery.Client()

def sorter_post(request):
    time = datetime.now()
    json = request.get_json(force=True, silent=True)
    if not json:
        raise BadRequest()

    source_id = util.get_source_id(json)
    results = util.get_sorter_results(json)
    source = util.get_sorter_source(source_id)
    util.validate_results(results, source)

    return flask.make_response('', 200)


def sorter_options(request):
    # CORS:
    #
    # Allows GET requests from any origin with the Content-Type
    # header and caches preflight response for an 3600s
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600'
    }

    return ('', 204, headers)


def sorter(request):
    try:
        return {
            'POST': sorter,
            'OPTIONS': sorter_options,
        }[request.method](request)
    except KeyError:
        return util.create_error_response(BadRequest())
    except Exception as e:
        return util.create_error_response(e)
