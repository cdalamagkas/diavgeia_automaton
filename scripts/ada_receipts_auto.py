import sys
import os
parent = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent)
from helpers.ada_receipt import create_ada_receipt
import configparser


SOURCE_TXT = "/home/user/Desktop/ΔΙΑΥΓΕΙΑ/ΑΠΟΔΕΙΞΕΙΣ_ΝΕΟ"
FILENAME_TXT = "ada_receipts.txt"

if __name__ == "__main__":

    config = configparser.ConfigParser()
    config.read(parent + "/config.ini")

    CONFIG = {
        "RECEIPTS_DIR": config['DEFAULT']['DESTINATION_RECEIPTS'],
        "AAY_DIR": config['DEFAULT']['AAY_LOCATION'],
        "FOREAS_EKDOSIS": config['DEFAULT']['FOREAS_EKDOSIS'],
        "BASE_URL": "https://diavgeia.gov.gr/opendata/"
    }
    print("⚓ Αυτόματη δημιουργία αποδείξεων από αρχείο κειμένου ⚓")
    with open(SOURCE_TXT + "/" + FILENAME_TXT, 'r') as file:
        Lines = file.readlines()
        for line in Lines:
            line = line.strip()
            if line != "":
                create_ada_receipt(line, CONFIG)
    input("Press Enter to continue...")

