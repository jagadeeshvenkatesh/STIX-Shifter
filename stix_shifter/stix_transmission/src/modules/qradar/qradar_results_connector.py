from ..base.base_results_connector import BaseResultsConnector
import json
from .....utils.error_response import ErrorResponder


class QRadarResultsConnector(BaseResultsConnector):
    def __init__(self, api_client):
        self.api_client = api_client

    def create_results_connection(self, search_id, offset, length):
        min_range = offset
        max_range = offset + length
        # Grab the response, extract the response code, and convert it to readable json

        response = self.api_client.get_search_results(search_id, 'application/json', min_range, max_range)
        response_code = response.code

        # Construct a response object
        return_obj = dict()
        response_dict = json.loads(response.read())
        
        if response_code == 200:
            return_obj['success'] = True
            return_obj['data'] = response_dict['events']
        else:
            ErrorResponder.fill_error(return_obj, response_dict, ['message'])

        return return_obj
