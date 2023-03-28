import os,os.path
import re

INPUT_DIR = '/home/user/Desktop/Προς_Ανάρτηση/Προς_Ανάρτηση_ΔΔ'
OUTPUT_DIR = '/home/user/Desktop/Προς_Ανάρτηση/Προς_Ανάρτηση_ΔΔ'


if __name__ == "__main__":
    pattern = re.compile(r'(\d+).+\.rtf')
    print("⚓ Αυτόματη μετατροπή αρχείων RTF σε PDF ⚓")
    counter = 0
    for file_name in os.listdir(INPUT_DIR):
        match = pattern.search(file_name)
        if match:
            counter = counter + 1
            protocolNumber = int(match.group(1))
            rtf_full_path = os.path.join(INPUT_DIR, file_name)
            os.system('soffice --headless --convert-to pdf --outdir ' + OUTPUT_DIR + ' "' + rtf_full_path + '" &>/dev/null')
            os.system('mv "' + rtf_full_path.split(".")[0] + '.pdf"' + ' ' + OUTPUT_DIR + '/' + str(protocolNumber) + '.pdf')
            print(f"[{counter}][✓] Επιτυχής δημιουργία του αρχείου {protocolNumber}.pdf")
        else:
            continue

    print("==========================")
    print(f"[i] Συνολικά δημιουργήθηκαν {counter} αρχεία PDF, τα οποία βρίσκονται στη διαδρομή {OUTPUT_DIR}")
    print("==========================")
    input("[>] Πιέστε οποιοδήποτε πλήκτρο για να τερματιστεί το πρόγραμμα...")

