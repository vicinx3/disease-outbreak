from flask import Blueprint, abort, request, jsonify
from covid_utils import *

covid_page = Blueprint('covid_page', __name__)

@covid_page.route('/last_day', methods=['GET'])
def get_last_day_data():
    return jsonify({'last_day': get_last_day(), 'marks': get_slider_marks()})

@covid_page.route('/map', methods=['GET'])
def get_map_data():
    date = int(request.args['date'])
    category = request.args['category']
    daily = request.args['daily'] == 'true'
    return jsonify(get_cases_by_country_and_category(date, category, daily))

@covid_page.route('/table', methods=['GET'])
def get_table_data():
    date = int(request.args['date'])
    return jsonify(get_cases_by_country(date))


@covid_page.route('/line_chart', methods=['GET'])
def get_line_chart_data():
    daily = request.args['daily'] == 'true'
    return jsonify(get_cases_by_day(daily))

@covid_page.route('/comparator', methods=['GET'])
def get_comparator_data():
    country = request.args['country'] if 'country' in request.args else ''
    return jsonify(get_comparator_graph_data(country))