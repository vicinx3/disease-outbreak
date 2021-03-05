from flask import Blueprint, abort, request, jsonify
from prediction_utils import *

prediction_page = Blueprint('prediction_page', __name__)

@prediction_page.route('/map', methods=['GET'])
def get_map_data():
    offset = int(request.args['offset'])
    country = request.args['country'] if 'country' in request.args else ''
    disease = request.args['disease'] if 'disease' in request.args else ''
    return jsonify(get_outbreaks_by_country(offset, country, disease))

@prediction_page.route('/table', methods=['GET'])
def get_table_data():
    return jsonify(get_outbreaks())