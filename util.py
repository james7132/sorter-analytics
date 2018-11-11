from werkzeug.exceptions import HTTPException, BadRequest, NotFound
import sources
import flask

source_KEY = 'source'
RESULTS_KEY = 'results'


def get_source_id(json):
    source_id = json.get(source_KEY)
    if source_id is None:
        raise BadRequest('source has not been provided.')
    return source_id


def get_sorter_source(source_id):
    sorter_source = sources.get_source(source_id)
    if sorter_source is None:
        raise NotFound('source ID does not have a corresponding source')
    return sorter_source


def get_sorter_results(json):
    results = json.get(RESULTS_KEY)
    if results is None:
        raise BadRequest('Reslts has not been provided.')
    return results


def validate_results(results, source):
    if len(results) <= 0:
        raise BadRequest('Results require at least one item.')
    for result_item in results:
        if result_item not in source:
            raise BadRequest(f'Result "{result_item}" not in source.')


def create_error_response(error):
    status_code = error.code if isinstance(error, HTTPException) else 500
    response = flask.jsonify(status=status_code, message=error.message)
    response.status_code = status_code
    return response
