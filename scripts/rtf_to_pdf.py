import os,os.path
import re

INPUT_DIR = '/home/user/Desktop/Προς_Ανάρτηση/Προς_Ανάρτηση_ΔΔ'
OUTPUT_DIR = '/home/user/Desktop/Προς_Ανάρτηση/Προς_Ανάρτηση_ΔΔ'


if __name__ == "__main__":
    pattern = re.compile(r'\d+')
    
    for file_name in os.listdir(INPUT_DIR):
        match = pattern.search(file_name)
        if match:
            protocolNumber = int(match.group())
            rtf_full_path = os.path.join(INPUT_DIR, file_name)
            os.system('soffice --headless --convert-to pdf --outdir ' + OUTPUT_DIR + ' "' + rtf_full_path + '"')
            os.system('mv "' + rtf_full_path.split(".")[0] + '.pdf"' + ' ' + OUTPUT_DIR + '/' + str(protocolNumber) + '.pdf')
        else:
            continue
