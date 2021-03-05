# For components on the main page
from flask import Blueprint, abort, request, jsonify
import db

main_page = Blueprint('main_page', __name__)

@main_page.route('/map', methods=['GET'])
def get_map_data(): 
    year = int(request.args['year'])
    month = int(request.args['month']) if 'month' in request.args else 0
    source = request.args['source'] if 'source' in request.args else ''
    country = request.args['country'] if 'country' in request.args else ''
    disease = request.args['disease'] if 'disease' in request.args else ''
    return jsonify(db.get_num_reports_by_country(source, year, month, country, disease, merge=True))

@main_page.route('/sidebar', methods=['GET'])
def get_sidebar_data():
    year = int(request.args['year'])
    month = int(request.args['month']) if 'month' in request.args else 0 
    source = request.args['source'] if 'source' in request.args else '' 
    country = request.args['country'] if 'country' in request.args else ''
    disease = request.args['disease'] if 'disease' in request.args else ''
    return jsonify(db.get_article_summary(source, year, month, country, disease))

@main_page.route('/modal', methods=['GET'])
def get_modal_data():
    url = request.args['url']
    return jsonify(db.get_article(url))

@main_page.route('/piechart/disease', methods=['GET'])
def get_piechart_disease_data():
    year = int(request.args['year'])
    month = int(request.args['month']) if 'month' in request.args else 0
    source = request.args['source'] if 'source' in request.args else ''
    country = request.args['country'] if 'country' in request.args else ''
    disease = request.args['disease'] if 'disease' in request.args else ''
    return jsonify(db.get_num_reports_by_disease(source, year, month, country, disease, maxResults=10, prettify=True))

@main_page.route('/comparator/actual', methods=['GET'])
def get_comparator_actual_data():
    country = request.args['country'] if 'country' in request.args else ''
    disease = request.args['disease'] if 'disease' in request.args else ''
    source = request.args['source'] if 'source' in request.args else ''
    return jsonify(db.get_num_reports_by_year(source, country, disease))

@main_page.route('/comparator/percentage', methods=['GET'])
def get_comparator_percentage_data():
    country = request.args['country'] if 'country' in request.args else ''
    disease = request.args['disease'] if 'disease' in request.args else ''
    source = request.args['source'] if 'source' in request.args else ''
    totalSource = request.args['totalSource'] if 'totalSource' in request.args else ''

    result = db.get_num_reports_by_year(source, country, disease)
    total = db.get_num_reports_by_year(totalSource)
    percentage = []
    for i, v in enumerate(result): 
        percentage.append({
            'date': result[i]['date'],
            'value': round(result[i]['value'] * 100 / total[i]['value'], 2)
        })
    return jsonify(percentage)