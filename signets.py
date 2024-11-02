from flask import Flask, request, Response
import xml.etree.ElementTree as ET
from constants import *
import os

app = Flask(__name__)

def load_file(filename):
    if not os.path.exists(filename):
        filename = f'{RESPONSES_DIR}/error.xml'

    with open(filename, 'r') as file:
        return file.read()
    
def extract_value_from_xml(xml_string, tag_name):
    root = ET.fromstring(xml_string)
    
    namespaces = {
        'soap': 'http://schemas.xmlsoap.org/soap/envelope/',
        'ets': 'http://etsmtl.ca/'
    }

    element = root.find('.//ets:' + tag_name, namespaces)

    return element.text.strip() if element is not None else None
    
def get_response(filename):
    content = load_file(filename)
    return Response(content, status=200, mimetype='text/xml')

@app.route('/', methods=['POST'])
def soap_endpoint():
    soap_action = request.headers.get('SOAPAction', '').strip('""')
    print(soap_action)

    if soap_action == "http://etsmtl.ca/donneesAuthentificationValides":
        return get_response(f'{AUTH_DIR}/donneeAuthValides.xml')

    if soap_action == "http://etsmtl.ca/infoEtudiant":
        return get_response(f'{INFO_DIR}/infoEtudiant.xml')
    
    if soap_action == "http://etsmtl.ca/listeProgrammes":
        return get_response(f'{PROGRAMMES_DIR}/programmes.xml')
    
    if soap_action == "http://etsmtl.ca/lireHoraireDesSeances":
        session = extract_value_from_xml(request.data, 'pSession')

        if not session:
            error_data = load_file(f'{RESPONSES_DIR}/error.xml')
            return Response(error_data, mimetype='text/xml')
            
        return get_response(f'{HORAIRES_DIR}/session_{session}.xml')    

    if soap_action == "http://etsmtl.ca/listeSessions":
        return get_response(f'{SESSIONS_DIR}/sessions.xml')       

    if soap_action == "http://etsmtl.ca/listeCours":
        print(request.data)
        return get_response(f'{COURS_DIR}/cours.xml')
    
    if soap_action == "http://etsmtl.ca/lireEvaluationCours":
        session = extract_value_from_xml(request.data, 'pSession')
        if not session:
            return Response('Missing pSession', mimetype='text/plain')
        
        return get_response(f'{EVALUATIONS_COURS_DIR}/session_{session}.xml')

    if soap_action == "http://etsmtl.ca/listeHoraireEtProf":
        session = extract_value_from_xml(request.data, 'pSession')
        if not session:
            return Response('Missing pSession', mimetype='text/plain')

        return get_response(f'{HORAIRE_PROF_DIR}/session_{session}.xml')

    if soap_action == "http://etsmtl.ca/listeElementsEvaluation":
        sigle = extract_value_from_xml(request.data, 'pSigle')
        groupe = extract_value_from_xml(request.data, 'pGroupe')
        session = extract_value_from_xml(request.data, 'pSession')
        
        if not sigle:
            return Response('Missing pSigle', mimetype='text/plain')
        if not groupe:
            return Response('Missing pGroupe', mimetype='text/plain')
        if not session:
            return Response('Missing pSession', mimetype='text/plain')

        return get_response(f'{EVALUATIONS_DIR}/{sigle}_{groupe}_{session}.xml')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
