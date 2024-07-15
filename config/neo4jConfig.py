from neo4j import GraphDatabase, basic_auth

# Empty DB
def getDriver():
  return GraphDatabase.driver(
  "bolt://3.239.172.236:7687",
  auth=basic_auth("neo4j", "analog-output-commas"))

def getMoviesDBDriver():
  return GraphDatabase.driver(
  "bolt://44.211.56.60:7687",
  auth=basic_auth("neo4j", "boiler-divers-steps"))