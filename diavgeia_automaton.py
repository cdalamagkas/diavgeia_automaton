import requests
import PyPDF2
import re
import os
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
import configparser
from helpers.ada_receipt import create_ada_receipt
import glob
import time


DEFAULT_HEADERS = {'Accept': 'application/json','Connection': 'Keep-Alive'}


def validate(metadata):

    # Convert issueDate to Greek format (dd/mm/YYYY) for user friendliness
    issueDate = datetime.strptime(metadata['issueDate'].split('T')[0], "%Y-%m-%d")
    issueDate = issueDate.strftime('%d/%m/%Y')

    print("Θα προβούμε στην ανάρτηση της πράξης με αρ.πρωτ. " + metadata['protocolNumber'] + " και τα εξής χαρακτηριστικά:")
    print("[i] Ημερομηνία έκδοσης πράξης: " + issueDate)
    print("[i] Ποσό με ΦΠΑ: " + str(metadata['extraFieldValues']['amountWithVAT']['amount']))
    print("[i] ΑΛΕ/ΚΑΕ: " + metadata['extraFieldValues']['amountWithKae'][0]['kae'])
    print("[i] Ποσό ΑΛΕ/ΚΑΕ με ΦΠΑ: " + str(metadata['extraFieldValues']['amountWithKae'][0]['amountWithVAT']) + "\n")

    answer = input("[>] Εγκρίνετε την ανάρτηση; (y/n): ")
    if answer == "y":
        return True
    else:
        print("Απορρίψατε την ανάρτηση. Επιστροφή...")
        return False


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("config.ini")

    CONFIG = {
        "RECEIPTS_DIR": config['DEFAULT']['DESTINATION_RECEIPTS'],
        "AAY_DIR": config['DEFAULT']['AAY_LOCATION'],
        "FOREAS_EKDOSIS": config['DEFAULT']['FOREAS_EKDOSIS'],
        "BASE_URL": None,
        "TESTING": config["DEFAULT"]["TESTING"]
    }

    if CONFIG["TESTING"] == "true" or CONFIG["TESTING"] == "True":
        CONFIG["TESTING"] = True
    else:
        CONFIG["TESTING"] = False
    
    try:
        username = config['DEFAULT']['DIAVGEIA_API_USERNAME']
        password = config['DEFAULT']['DIAVGEIA_API_PASSWORD']
    except KeyError:
        username = None
        password = None
    
    if CONFIG["TESTING"]:
        CONFIG["BASE_URL"] = 'https://test3.diavgeia.gov.gr/luminapi/opendata/'
        username = "10599_api"
        password = "User@10599"
    else:
        CONFIG["BASE_URL"] = 'https://diavgeia.gov.gr/opendata/'
        if username is None and password is None:
            invalid = True
            while True:
                print("⚓ Εισαγωγή Διαπιστευτηρίων Δι@ύγεια ")
                username = input('[>] Παρακαλώ δώστε το όνομα χρήστη στη Δι@ύγεια: ')
                password = input('[>] Παρακαλώ δώστε τον κωδικό πρόσβασης στη Δι@ύγεια: ')
                #TODO check whether credentials are valid
                break

    if os.name == "posix":
        DIR_SEPARATOR = "/"
        SOFFICE = "soffice"
    else:
        DIR_SEPARATOR = "\\"
        SOFFICE = ""

    counter = 1
    while True:
        print("⚓ Ανάρτηση AAY # " + str(counter))
        protocolNumber = input("[>] Παρακαλώ δώστε Αριθμό Πρωτοκόλλου: ")
        
        aay_filename = glob.glob(CONFIG["AAY_DIR"] + "/*" + protocolNumber + "*")[0]
                
        # Convert RTF to PDF
        os.system('soffice --headless --convert-to pdf --outdir "' + CONFIG["AAY_DIR"] + '" "' + aay_filename + '"')
        os.system('mv "' + aay_filename.split(".")[0] + '.pdf"' + ' "' + CONFIG["AAY_DIR"] + '/' + protocolNumber + '.pdf"')

        aay_filename = CONFIG["AAY_DIR"] + '/' + protocolNumber + '.pdf'

        reader = PyPDF2.PdfReader(aay_filename)
        page = reader.pages[0]
        page_content = page.extract_text()
        
        if 'Μη αναρτητέα στο διαδίκτυο' not in page_content:
            cost = float(re.search(r'(\b\d{1,7}(\.\d{3})*(,\d{2})\b)', page_content).group(0).replace(".", "").replace(",", "."))
            ale = re.search(r'([0-9]{10})', page_content).group(0)

            issueDate = re.search(r'(\d{2}\/\d{2}\/\d{4})', page_content).group(0).strip()
            issueDate = datetime.strptime(issueDate, '%d/%m/%Y')
            issueDate = issueDate.strftime('%Y-%m-%d') + 'T00:00:00.000Z'

            if CONFIG["TESTING"]:
                with open('./.testing/SampleDecisionMetadata.json', 'r') as file:
                    metadata = json.load(file)
            else:
                with open('metadata.json', 'r') as file:
                    metadata = json.load(file)
                
            metadata['protocolNumber'] = protocolNumber
            metadata['extraFieldValues']['amountWithVAT']['amount'] = cost
            metadata['extraFieldValues']['amountWithKae'][0]['kae'] = ale
            metadata['extraFieldValues']['amountWithKae'][0]['amountWithVAT'] = cost
            metadata['issueDate'] = issueDate

            if validate(metadata):

                data = {'metadata': json.dumps(metadata, ensure_ascii=False).encode('utf8').decode()}
                
                if CONFIG["TESTING"]:
                    pdf = open("./.testing/SampleDecision.pdf", 'rb')    
                else:
                    pdf = open(aay_filename, 'rb')

                files = [('decisionFile', pdf)]
                while True:
                    try:
                        print("Ανάρτηση απόφασης στη Δι@ύγεια...")
                        response = requests.post(url=CONFIG["BASE_URL"] + '/decisions', data=data, files=tuple(files), auth=HTTPBasicAuth(username, password), headers=DEFAULT_HEADERS)
                    except requests.ConnectionError:
                        print("[!!] Σφάλμα σύνδεσης με τη Δι@ύγεια.")
                        print("[i] Νέα προσπάθεια ανάρτησης σε 10 δευτερόλεπτα...") 
                        print("[i] Για ακύρωση πατήστε CTRL + C")
                        time.sleep(10)
                        continue
                    break

                if response.status_code == 200:
                    decision = response.json()
                    print("[✓] Η απόφαση αναρτήθηκε επιτυχώς με ΑΔΑ: " + decision['ada'])
                    print("Δημιουργία απόδειξης...")
                    while True:
                        success = create_ada_receipt(decision["ada"], CONFIG)
                        if not success:
                            continue
                        else:
                            break
                
                elif response.status_code == 400:
                    print("[!!] Σφάλμα στην υποβολή της πράξης")
                    err_json = response.json()
                    for err in err_json['errors']:
                        print("{0}: {1}".format(err['errorCode'], err['errorMessage']))
                elif response.status_code == 401:
                    print("[!!] Σφάλμα αυθεντικοποίησης")
                elif response.status_code == 403:
                    print("[!!] Απαγόρευση πρόσβασης")
                else:
                    print("[!!] ERROR " + str(response.status_code))

                counter = counter + 1
                print("=============================================================")

            else:
                continue
        
        else:
            print('[!!] Μη αναρτητέα!')
            continue
