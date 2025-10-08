from prd_findEmployees import findEmployee
from prd_findGroups import findGroups
from prd_populateGroups import processRelationships
from prd_cypher import executeCypher

def addEmployees():
    query = findEmployee()
    executeCypher(query)

def addGroups():
    query = findGroups()
    executeCypher(query)

def addRelationships():
    processRelationships()

#addEmployees()
#addGroups()
#addRelationships()