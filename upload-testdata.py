import os
import requests
import time

folder_to_load = "performance_testdata"
FHIR_BASE_URL = os.getenv('FHIR_BASE_URL')
FHIR_USER = os.getenv('FHIR_USER')
FHIR_PW = os.getenv('FHIR_PW')


for file in os.listdir(folder_to_load):
    if file.endswith(".ndjson"):
        filepath = os.path.join(f'./{folder_to_load}', file)

        with open(filepath) as fp:
            Lines = fp.readlines()
            print("loading file:" + filepath)
            start = time.time()
            for line in Lines:
                headers = {'Content-Type': "application/fhir+json"}
                payload = line
                resp = requests.post(FHIR_BASE_URL, data=line, headers=headers)
            end = time.time()
            print("seconds taken for upload:", end-start)
