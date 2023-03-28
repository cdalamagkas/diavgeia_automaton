import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from helpers.ada_receipt import create_ada_receipt
from helpers.get_issuer import get_issuer
import configparser
import json


SOURCE_TXT = "/home/user/Desktop/ΔΙΑΥΓΕΙΑ/ΑΠΟΔΕΙΞΕΙΣ_ΝΕΟ"
FILENAME_TXT = "ada_receipts.txt"

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read("diavgeia_config.ini")

    CONFIG = {
        "RECEIPTS_DIR": config['DEFAULT']['DESTINATION_RECEIPTS'],
        "AAY_DIR": config['DEFAULT']['AAY_LOCATION'],
        "BASE_URL": "https://diavgeia.gov.gr/opendata/"
    }
    with open("metadata.json", 'r') as file:
        metadata = json.load(file)
        CONFIG["ISSUER"] = get_issuer(metadata["organizationId"], CONFIG)
    
    print("⚓ Αυτόματη δημιουργία αποδείξεων από αρχείο κειμένου ⚓")
    counter = 1
    with open(SOURCE_TXT + "/" + FILENAME_TXT, 'r') as file:
        Lines = file.readlines()
        for line in Lines:
            line = line.strip()
            if line != "":
                response = create_ada_receipt(line, CONFIG)
                if response["success"]:
                    print(f"[{counter}][✓] H απόδειξη με όνομα {response['filename']} δημιουργήθηκε.")
                    counter = counter + 1
                else:
                    if not response["connection_error"]:
                        print(f"[!!] Απέτυχε η δημιουργία απόδειξης με ΑΔΑ {response['ada']}. Ενδέχεται ο ΑΔΑ να είναι εσφαλμένος.")
                    else:
                        print(f"[!!] Απέτυχε η δημιουργία απόδειξης με ΑΔΑ {response['ada']} λόγω αποτυχίας σύνδεσης με τη Δι@ύγεια.")
        counter = counter -1
        print("==========================")
        print(f"[i] Δημιουργήθηκαν συνολικά {counter} αποδείξεις οι οποίες αποθηκεύτηκαν στη διαδρομή {CONFIG['RECEIPTS_DIR']}")
        print("==========================")
        input("[>] Πιέστε οποιοδήποτε πλήκτρο για να τερματιστεί το πρόγραμμα...")

