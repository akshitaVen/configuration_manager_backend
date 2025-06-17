from app.core.couchdb import get_couch_server
from fastapi import HTTPException


def create_new_configuration(config_name: str):
    config_name = config_name.strip().lower().replace(" ", "_")
    print("config name received: ", config_name)
    if not config_name:
        raise HTTPException(status_code=400, detail="Configuration name is required.")


    couch = get_couch_server() # gets couch db server object
    print("Connected with couch db server ")
    print("couch: ", couch)
    # check if a configuration in this name is already present
    for db in couch:
        print("db name: ")
        print(db)

    if config_name in couch:
        raise HTTPException(status_code=400, detail="Configuration already exists.")
    
    # if not present, create a confiiuration db. 
    db = couch.create(config_name)

    # inside db sst up 2 documents: configuration, logs
    config_doc_id = 'configuration'
    config_doc = { 
        '_id': config_doc_id,

    }
    configuration_response = db.save(config_doc) #[id, rev]
    print(f"Document {configuration_response[0]} created succesfully with revision {configuration_response[1]}")

    changelogs_doc_id = 'changelogs'
    changelogs_doc = {
        '_id': changelogs_doc_id,
    }
    changelogs_response = db.save(changelogs_doc) #[id, rev]
    print(f"Document {changelogs_response[0]} created succesfully with revision {changelogs_response[1]}")

    return 

    # set up configuration db sync with cloud 

  
    # db["configuration"] = {
    #     "type": "configuration",
    #     "parameters": {},
    #     "metadata": {},
    # }

    # db["changelogs"] = {
    #     "type": "changelogs",
    #     "logs": [],
    # }

    # return {"message": f"Configuration '{config_name}' created successfully."}
