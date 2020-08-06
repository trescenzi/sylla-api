from bottle import route, run, hook, response, request

import csv, json, os
import markdown
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
_name_seeds_key = 'nameSeeds';

def processNameSeeds(nameSeeds):
    if not isinstance(nameSeeds, list):
        nameSeeds = nameSeeds.strip()
        if ',' in nameSeeds:
            print('splitting on commas')
            nameSeeds = nameSeeds.split(',')
        else:
            nameSeeds = nameSeeds.split()
    syllables = [syllable for name in nameSeeds for syllable in syllySplit(name)]
    return processSyllables(syllables)

@route('/')
def help():
    with open('./README.md') as file:
        return markdown.markdown(file.read())

@route('/names', method=['POST', 'GET'])
def names():
    """ /names
        Returns a variable number of names.

        Allowed Methods: POST, GET

        Params are as follows:
        - numNames : number 
            The number of names to generate
        - numSyllablesPerName : number
            The number of syllables per name to use when generating the names
        - nameSeeds : str | list
            A list of names to use as seeds for generating the new name. If
            provided as a string it can be space or comma seperated.

        GET requests should provide them as query params, POST as a json body.
    """

    data = request.json or request.query
    nameList = processNameSeeds(data[_name_seeds_key]) if _name_seeds_key in data else processedNames
    try:
        return json.dumps({
            'names': generateNames(nameList,
                                   int(data[_num_names_key]) if _num_names_key in data else 1 , 
                                   int(data[_num_syllables_key]) if _num_syllables_key in data else 2),
        })
    except:
        errors = ['GET / for docs']
        if not _num_names_key in data:
            errors.append('Please provide numeric value for key numNames')
        if not _num_syllables_key in data:
            errors.append('Please provide numberic value for key numSyllablesPerName')
        if not _num_names_key in data and not _num_syllables_key in data:
            errors.append('An unknown error has occured')
        response.status = 400
        return ''.join(errors)

@route('/name', method=['POST', 'GET'])
def name():
    """ /name
        Returns a single name.

        Allowed Methods: POST, GET

        Params are as follows:
        - numSyllables : number
            The number of syllables to include in the name
        - nameSeeds : str | list
            A list of names to use as seeds for generating the new name. If
            provided as a string it can be space or comma seperated.
        
        GET requests should provide them as query params, POST as a json body.
    """
    data = request.json or request.query
    nameList = processNameSeeds(data[_name_seeds_key]) if _name_seeds_key in data else processedNames
    try:
        return generateNames(nameList, 1, int(data['numSyllables']) if 'numSyllables' in data else 2)[0]
    except:
        response.status = 400
        if not 'numSyllables' in data:
            return 'Please provide numberic value for key numSyllables. GET / for docs'
        else:
            return 'An unknown error has occured. GET / for docs'

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
