from app.core.couchdb import get_couch_server
from fastapi import HTTPException
from datetime import datetime
from app.constants import CLOUD_DEV_COUCH_DB_SERVER_BASE_URL, LOCAL_COUCH_DB_SERVER_BASE_URL

def validate_config_name(couch, config_name):
    if not config_name:
        raise HTTPException(status_code=400, detail="Configuration name is required.")

    # TO DO: check if there are spaces and replace with underscore

    normalized_config_name = config_name.strip().lower().replace(" ", "_")
    print("config name received: ", normalized_config_name)

    if normalized_config_name in couch: # check if a configuration in this name is already present
        raise HTTPException(status_code=400, detail="Configuration already exists. Use a different configuration name.") # TO DO: Return the exception properly in function call
    
    return normalized_config_name, f"Config name '{normalized_config_name}' is valid and available."

def create_new_configuration(config_name: str):


    # gets couch db server object
    couch = get_couch_server() 
    print("Connected with couch db server ")
    print("couch: ", couch)

    normalized_config_name, message = validate_config_name(couch, config_name)
    print(message)
     
    # if not present, create a confiiuration db. 
    configuration_db = couch.create(normalized_config_name) # in the local server, creates a db with normalized_config_name. 
    print("COnfiguration db creation response: ", configuration_db)

    # inside db set up configuration document
    config_doc_id = 'configuration'
    config_doc = { 
        '_id': config_doc_id,
    }
    configuration_response = configuration_db.save(config_doc) #[id, rev]
    print(f"Document {configuration_response[0]} created succesfully with revision {configuration_response[1]}")

    # create a db for change logs
    changelog_db_name = f"{normalized_config_name}_changelogs"
    if changelog_db_name in couch:
        raise HTTPException(status_code=400, detail="Changelog DB already exists for this config.")
    changelogs_db = couch.create(changelog_db_name)
    print("Changelogs db creation response: ", changelogs_db)

    # create and add an entry/document for first log
    timestamp = datetime.utcnow().isoformat() + "Z"
    changelog_entry = {
        "timestamp": timestamp,
        "description": f"Configuration named '{normalized_config_name}' was created."
    }
    changelog_entry_response = changelogs_db.save(changelog_entry)
    print(f"Initial changelog created in '{changelog_db_name}' with ID {changelog_entry_response[0]}")

    # establish db sync, replication
    setup_continuous_replication(couch, normalized_config_name)
    setup_continuous_replication(couch, changelog_db_name)

# Good practice could be to periodically check if the sync conenction is intact.Notes the time the last sync was checked and shows it in the UI. 

    # get the relevent param metadata table.
    return 



def setup_continuous_replication(couch, source_db_name):
    # in _replicator db, check if the document is already present. 
    # if not present, create a document with source_db and target, continuous set to true
    _replicator_db = couch["_replicator"]
    print("_replicator_db connection response: ", _replicator_db)
    if source_db_name in _replicator_db:
        print(f"Replication already set up for {source_db_name}.")
        return 
    
    replication_document_id = source_db_name + "_rep"
    print("replication_document_id: ", replication_document_id)
    replication_job_json = {
        "_id": replication_document_id,
        "source": LOCAL_COUCH_DB_SERVER_BASE_URL+f"{source_db_name}",
        "target": CLOUD_DEV_COUCH_DB_SERVER_BASE_URL+f"{source_db_name}",
        "continuous": True,
        "create_target": True, #creates target db  if it doesnt exist
        # "user_ctx": { # not sure if i want this
        #     "name": "admin", 
        #     "roles": ["_admin"]
        # }
    }

    _replicator_document_response = _replicator_db.save(replication_job_json)
    print("_replicator_document_response: ", _replicator_document_response)