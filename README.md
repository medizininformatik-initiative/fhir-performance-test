# fhir-performance-test

This repository allows a German DIC to test the performance of its own FHIR Server implementation.

It references other repositories, which allows one to not only test any FHIR Server, but also allows a DIC to test existing
example FHIR Servers on their hardware and/or generate specific testdata to resemble a common load on the FHIR Server.



## Setting up your FHIR server

You can use this repository with an existing FHIR server of your choice or use the test setup provided here: <https://github.com/medizininformatik-initiative/fhir-server-examples> to setup one of the example FHIR servers. - Follow the repository for instructions.

Please be aware that if you are using the example FHIR server repository it will expose the fhir endpoints on localhost depending on the chosen server see `Supported Servers` section of the repositories readme. You will then have to change your environment variables below accordingly.


## Environment variables performance test

Set the following environment variables for your performance test using
`export <env-var-name-here>=<env-var-value-here>`

|Env variable | description| default value|
|---|---|---|
|FHIR_BASE_URL| Base url of the fhir server (e.g. http://localhost:8082/fhir)|http://localhost:8082/fhir|
|FHIR_USER| FHIR user for basic auth - other auth not supported||
|FHIR_PW| FHIR password for basic auth - other auth not supported | |

## Create testdata for the performance test

To create testdata for the performance test check out the mii-fhir-tesdata-generator repository: <https://github.com/juliangruendner/mii-fhir-testdata-generator> and copy the gen-desc-descriptions from the "gen-desc-descriptions" folder of this repository to the `input` folder of the mii-fhir-tesdata-generator.

Then in the mii-fhir-tesdata-generator execute `docker-compose up` and wait for the testdata generator to generate the testdata - this can take a while. You will then find the final generated testdata in the largerFhirBundles folder of the testdata generator repository as .ndjson files.

## Upload the testdata to your fhir server

To upload the testdata to your fhir server copy the .ndjson files you generated above from the testdata generator `largerFhirBundles` folder to the `performance_testdata` folder of this repository, set the following environment variables according to `Environment variables performance test` of this readme and execute
`python3 upload-testdata.py` to upload the bundles to your server.


## Run the performance tests

To run the performance tests execute the `python3 performance-test.py` script of this repository.
For this also set the environment variables according to `Environment variables performance test` of this readme.

The performance test will run and create a small report in json format: 
`performance-test-results.json`, which can be shared with others.



