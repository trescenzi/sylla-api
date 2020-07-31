from bottle import route, run, hook, response, request

import csv, json, os
from utils import syllySplit, processSyllables, generateNames

syllables = []
with open('./names.txt') as file:
    syllables = [syllable for name in file.readlines() if len(syllySplit(name)) > 1 for syllable in syllySplit(name)]

processedNames = processSyllables(syllables)

_allow_origin = '*'
_allow_methods = 'GET, POST, OPTIONS'
_allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With'
_num_syllables_key = 'numSyllablesPerName'
_num_names_key = 'numNames';

@route('/')
def help():
    return ''

@route('/names', method=['POST', 'GET'])
def names():
    if request.method is 'GET' or request.json is None:
        return json.dumps({
            'names': generateNames(processedNames),
        })
    else:
        data = request.json
        errors = []
        if not _num_names_key in data:
            errors.append('Please provide numeric value for key numNames')
        if not _num_syllables_key in data:
            errors.append('Please provide numberic value for key numSyllablesPerName')
        if len(errors) is not 0:
            response.status = 400
            return '\n'.join(errors)

        return json.dumps({
            'names': generateNames(processedNames, data['numNames'], data['numSyllablesPerName']),
        })

@route('/name', method=['POST', 'GET'])
def name():
    if request.method is 'GET' or request.json is None:
        return generateNames(processedNames)
    else:
        data = request.json
        if not 'numSyllablesPerName' in data:
            response.status = 400
            return 'Please provide numberic value for key numSyllablesPerName'
        return generateNames(processedNames, 1, data['numSyllablesPerName'])[0]

@hook('after_request')
def enable_cors():
    response.set_header('Access-Control-Allow-Origin', _allow_origin)
    response.set_header('Access-Control-Allow-Methods', _allow_methods)
    response.set_header('Access-Control-Allow-Headers', _allow_headers)
@route('/', method = 'OPTIONS')
@route('/<path:path>', method = 'OPTIONS')
def options_handler(path = None):
    return

# Get required port, default to 5000.
port = os.environ.get('PORT', 5000)

# Run the app.
run(host='0.0.0.0', port=port)
