# ![µLIMS Logo](/microLIMS/static/images/logo.png) 

(Micro Laboratory Information System)

a Django CRUD app that implements a light-weight project management system for sample logging, testing, and reporting with user authentication and authorization. Functions and usage are from perspective of a testing laboratory(no client portal). This means the lab is responsible for logging, tracking, and managing tests. Inspired by my experience of a LIMS :woman_scientist:

## Installation

Make sure you have docker installed and cloned the repo. Make sure you have the correct environmental files. An example file has been provided.

Build the image:
``` 
$ docker-compose build 
```
Run the container:
```
$ docker-compose up -d
```
Navigate to [http://localhost:8000/](http://localhost:8000/) to view the project homepage
## Usage

Setup: Create a superuser from command line or the admin panel. You can create normal users after this step. This is essentially because the LIMS is a subsciption/ pay per user service. Create "companies" and "tests/testing method" for your LIMS. This will be the company using your testing system and the tests that your lab is able to perform. 

Usage/Process Flow: Create a project for the company. Each project can have multiple samples and each samples can have multiple test attributed to it. You can delete samples before testing is initiated but once samples are in testing you may only cancel. Cancellation is done per test, per sample or per project. Once testing is completed you will see it reflected in the testing status for sample test, sample or project, if applicable. 

## Contributing 

Please reach out and let me know your thoughts on this project :blush:

## License 
[MIT](https://choosealicense.com/licenses/mit/)
