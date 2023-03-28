import configparser
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from helpers.ada_receipt import create_ada_receipt
from helpers.get_issuer import get_issuer
import json


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

    counter = 1
    while True:
        
        print("⚓ Απόδειξη # " + str(counter))
        ada = input("[>] Παρακαλώ δώστε έναν ΑΔΑ: \n")        
        print("Δημιουργία απόδειξης, παρακαλώ περιμένετε...")

        response = create_ada_receipt(ada, CONFIG)
        if response["success"]:
            print(f"[✓] H απόδειξη με όνομα {response['filename']} δημιουργήθηκε.")
            counter = counter + 1
        else:
            if not response["connection_error"]:
                print(f"[!!] Απέτυχε η δημιουργία απόδειξης με ΑΔΑ {response['ada']}. Ενδέχεται ο ΑΔΑ να είναι εσφαλμένος.")
            else:
                print(f"[!!] Απέτυχε η δημιουργία απόδειξης με ΑΔΑ {response['ada']} λόγω αποτυχίας σύνδεσης με τη Δι@ύγεια.")

        print("=============================================")
