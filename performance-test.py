import os
import requests
import time
import json
from requests.auth import HTTPBasicAuth
from threading import Thread

FHIR_BASE_URL = os.getenv('FHIR_BASE_URL', 'http://localhost:8082/fhir')
FHIR_USER = os.getenv('FHIR_USER')
FHIR_PW = os.getenv('FHIR_PW')

def get_next_link(link_elem):
    for elem in link_elem:
        if elem['relation'] == 'next':
            return elem['url']

    return None

def page_through_results_and_collect(resp):

    result_list = []
    next_link = get_next_link(resp.json()['link'])

    if len(resp.json()['entry']) > 0 and resp.json()['entry'][0]['resource']['resourceType'] == 'Patient':
        result_list = list(map(lambda entry: {"patient": entry['resource']['id']}, resp.json()['entry']))
    else:
        result_list = list(map(lambda entry: {"patient": entry['resource']['subject']['reference'].split('/')[1]}, resp.json()['entry']))

    while next_link:
        resp = requests.get(next_link, auth=HTTPBasicAuth(FHIR_USER, FHIR_PW))
        if resp.json()['entry'][0]['resource']['resourceType'] == 'Patient':
            result_list_temp = list(map(lambda entry: {"patient": entry['resource']['id']}, resp.json()['entry']))
        else:
            result_list_temp = list(map(lambda entry: {"patient": entry['resource']['subject']['reference'].split('/')[1]}, resp.json()['entry']))
        next_link = get_next_link(resp.json()['link'])
        result_list = result_list + result_list_temp

    return result_list


def exec_perf_test(test):
    start = time.time()
    query = f'{FHIR_BASE_URL}/{test["query"]}&_count=500'
    resp = requests.get(query, auth=HTTPBasicAuth(FHIR_USER, FHIR_PW))
    result_list = page_through_results_and_collect(resp)
    end = time.time()
    test['time-taken'] = end - start
    test['resources-found'] = len(result_list)
    return test


def exec_perf_tests():

    with open('performance-tests.json', 'r') as perf_test_file:
        perf_tests = json.load(perf_test_file)
        perf_results = []

        for test in perf_tests['test-queries']:
            perf_result = exec_perf_test(test)
            print(perf_result)
            perf_results.append(perf_result)

    with open("performance-test-results.json", "w") as outfile:
        json.dump(perf_results, outfile)


exec_perf_tests()

concurrent = 0
for index in range(0, 10):
    for i in range(concurrent):
        t = Thread(target=exec_perf_tests(index))
        t.daemon = False
        t.start()