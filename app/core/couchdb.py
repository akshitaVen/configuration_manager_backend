import couchdb

def get_couch_server() -> couchdb.Server:
    # couch = couchdb.Server("http://localhost:5984")
    # return couchdb.Server("http://localhost:5984")  # Update with auth if needed
    return couchdb.Server('http://admin:changeme@localhost:5984/') # with auth
