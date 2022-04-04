from calendar import c
import os
from pyrsistent import v
import requests
import time
import json
import base64
import uuid
import csv
from threading import Thread

FHIR_BASE_URL = os.getenv('FHIR_BASE_URL')

def execute_flare(query_number, flare_exec_url, sq):
    start = time.time()

    headers = {
        "Content-Type": "application/sq+json"}

    resp = requests.post(f'{flare_exec_url}', data=sq, headers=headers)
    end = time.time()

    return {"query_number": query_number, 
            "query_exec_type": "flare",
            "time_taken_seconds": end - start, "n_resources_found": resp.json()}

def get_next_link(link_elem):
    for elem in link_elem:
        if elem['relation'] == 'next':
            return elem['url']

    return None

def page_through_results_and_collect(resp):

    result_list = []
    next_link = get_next_link(resp.json()['link'])
    result_list = list(map(lambda entry: {"patient": entry['resource']['subject']['reference'].split('/')[1], "code": entry['resource']['code']['coding'][0]['code'], "value": entry['resource']['valueQuantity']['value']}, resp.json()['entry']))

    while next_link:

        resp = requests.get(next_link)
        result_list_temp = list(map(lambda entry: {"patient": entry['resource']['subject']['reference'].split('/')[1]}, resp.json()['entry']))
        next_link = get_next_link(resp.json()['link'])
        result_list = result_list + result_list_temp

    return result_list


def exec_perf_test(test):
    start = time.time()
    query = f'{FHIR_BASE_URL}/{test["query"]}'
    resp = requests.get(query)
    result_list = page_through_results_and_collect(resp)
    end = time.time()
    test['time-taken'] = end - start
    test['res-found'] = len(result_list)
    return test


def exec_perf_tests():

    with open('performance-tests.json', 'r') as perf_test_file:
        perf_tests = json.load(perf_test_file)
        perf_results = []

        for test in perf_tests['test-queries']:

            perf_result = exec_perf_test(test)
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