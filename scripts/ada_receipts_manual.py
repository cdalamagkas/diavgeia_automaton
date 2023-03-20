import configparser
import sys
import os
parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)
from helpers.ada_receipt import create_ada_receipt


if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read(parent + "/config.ini")

    CONFIG = {
        "RECEIPTS_DIR": config['DEFAULT']['DESTINATION_RECEIPTS'],
        "AAY_DIR": config['DEFAULT']['AAY_LOCATION'],
        "FOREAS_EKDOSIS": config['DEFAULT']['FOREAS_EKDOSIS'],
        "BASE_URL": "https://diavgeia.gov.gr/opendata/"
    }

    counter = 1
    while True:
        
        print("⚓ Απόδειξη # " + str(counter))
        ada = input("[>] Παρακαλώ δώστε έναν ΑΔΑ: \n")        
        print("Δημιουργία απόδειξης, παρακαλώ περιμένετε...")

        success = create_ada_receipt(ada, CONFIG)
        if not success:
            print("Παρακαλώ προσπαθήστε ξανά")
            continue
        else:
            counter = counter + 1
        
        print("=============================================")
