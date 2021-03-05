# SENG3011_code-onavirus

# Code-onavirus D.O.T. (Disease Outbreak Tracker)

# API accessible at: www.codeonavirus.com

Designed and developed by:

- Kenvin Yu (z5207857)
- Evan Lee (z5207846)
- Eric Tan (z5205997)
- Victor Liu (z5207848)
- Ezra Eyaru (z5215204)

## Deliverable 1

Deliverable 1 contains a report that outlines the design of our API, inclduing information on how it will run on a web server, the parameters and return values from the API with examples of interaction and justification of the implementation language that we will be using for the API. The report will also include information on how we manage our team through delegating work and any tools that we will use for project management. All documentation will be located in the 'reports' folder.

## Deliverable 2

The first part of deliverable 2 contains the Swagger documentation and a functioning end point that can be tested. This also includes the site hosted by the API that can be accessed. Like the previous deliverable, documentation can be found in the 'reports' folder and all source code will be in the 'PHASE_1' folder.
Features include 
* Deployment as a REST Web service with a clearly documented API
* Ability to make requests to the API
* Generating an output file with errors

The second part of deliverable 2 contains the API documentation, implementation and report. There are four key features within this section:

1. API design details  
   Updated design details and team management reports that were previously published in Deliverable 1 of the project.

2. API testing  
   Testing processes used in the development of the API including data and test scripts which will be inside the Phase_1/TestScripts folder. This includes information
   about the testing environment, tools used, limitations and testing processes and an overview of test cases, input and output.

3. Swagger API documentation  
   This is an extension of the first part providing a hosted site that documents how to make calls to the API, specifically including information on the payload and return

4. API implementation  
   This section entails the actual implementation of the functioning API, in particular the code for the functioning API with log files that contain information about the input and output as well as information about resource usage and time efficiency.

Accessing code-onavirus atlas MongoDB:
mongo "mongodb+srv://codeonavirus-etwjy.mongodb.net/test" --username h_evan_lee

mongo "mongodb+srv://codeonavirus-etwjy.mongodb.net/test" --username codeonavirus

#### Database design

```javascript
    "article" : {
        "date_of_publication" :
        "url" :
        "headline" :
        "main_text" :
        "reports" : [
            "report" : {
                "diseases" :
                "syndromes" :
                "event_date" :
                "locations" : [
                    "location" : {
                        "city":
                        "state":
                        "country":
                        "continent":
                }
                ]
            }
        ]
        "key_terms": []
    }
```

Deliverable 3
-------------

Deliverable 3 requires a presentation of a barebones version of our final application. The sourcecode for the web application can be found in the folder labelled 'PHASE_2'. The slides associated with the presentation can be located in the 'reports' folder of the repository. In our presentation, we highlight the business value of our application, what has been currently implemented as well as our technical architecture of the web application. 

Following the presentation, sourcecode for 'PHASE_2' will be updated for Deliverable 4 and hence the prototype code will unfortunately not be saved. 

Deliverable 4
-------------

For the fourth and final deliverable, we will demonstrate our finished web-application as well as create a final report that serves as an updated collation of the design details and and management information reports completed prior with the addition of detail use cases. Once again, the report can be found in the 'reports' folder of the repository. As for the source code, it will all be contained in the 'PHASE_2' directory in the repository. To run the application, you will need to run both the backend and frontend. To setup and run the backend:
1. ``` cd ``` into ``` /PHASE_2/Application_SourceCode/backend ```
2. run ``` python3 -m venv env ``` to create a virtual environment in a folder titled 'env'
3. run ``` source env/bin/activate" ``` to activate the virtual environment
4. run ``` pip install -r requirements.txt ``` to install required modules
5. run ``` deactivate ``` to exit out of the virtual environment
6. You are not done setting up the backend server
7. To run the backend server after setting up ``` cd ``` into ``` /PHASE_2/Application_SourceCode/codeonavirus ```
8. run ``` npm run-script backend ``` to start the Flask backend server
To setup and run the frontend of the application :
1. ``` cd ``` into ``` /PHASE_2/Application_SourceCode/codeonavirus ```
2. run ``` npm install ``` to install the required packages
3. run ``` npm start ``` to start the application
# disease-outbreak
