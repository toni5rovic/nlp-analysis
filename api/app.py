from flask import abort, Flask, jsonify
from flask import make_response
from flask import request
from flask_cors import CORS, cross_origin

import os, sys, json
import services

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#######################################
# POST API Endpoints
#######################################
#@cross_origin()
@app.route('/api/analysis/semantic', methods=['POST'])
def file_semantic_analysis():
    requestBody = request.get_json(silent=True)
    analysis_type = requestBody.get('type')
    text = requestBody.get('text')

    if analysis_type == "synonyms":
        result = services.synonyms(text)
        return services.serialize(result)
    elif analysis_type == "antonyms":
        result = services.antonyms(text)
        return services.serialize(result)
    elif analysis_type == "disambiguation":
        result = services.disambiguation(text)
        return services.serialize(result)

@app.route('/api/analysis/morphological', methods=['POST'])
@cross_origin()
def file_morphological_analysis():
    requestBody = request.get_json(silent=True)
    text = requestBody.get('text')
    result = services.morphological_analysis(text)
    return result

@app.route('/api/analysis/NER', methods=['POST'])
@cross_origin()
def file_ner_analysis():
    requestBody = request.get_json(silent=True)
    text = requestBody.get('text')
    result = services.ner_analysis(text)
    return services.serialize(result)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
