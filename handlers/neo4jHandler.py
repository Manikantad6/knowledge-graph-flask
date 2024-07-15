from neo4j import GraphDatabase, basic_auth
from config import neo4jConfig
import json
def queryMoviesDB():
  driver = neo4jConfig.getMoviesDBDriver()

  cypher_query = '''
  MATCH (movie:Movie {title:$favorite})<-[:ACTED_IN]-(actor)-[:ACTED_IN]->(rec:Movie)
  RETURN distinct rec.title as title LIMIT 20
  '''

  with driver.session(database="neo4j") as session:
    results = session.read_transaction(
      lambda tx: tx.run(cypher_query,
                        favorite="The Matrix").data())
  driver.close()
  return results


def query(cypher_query):
  driver = driver()
  with driver.session(database="neo4j") as session:
    results = session.read_transaction(
      lambda tx: tx.run(cypher_query,
                        favorite="The Matrix").data())
    for record in results:
      print(record['title'])

## INSERTING INTO DB
def insert():
  driver = neo4jConfig.getDriver()

  with driver.session(database="neo4j") as session:
    results = session.write_transaction(create_graph)
    print(results)
    driver.close()


def create_graph(tx):
    # Example nodes and relationships
    nodes = [
        ("New York City", "city"),
        ("California", "state"),
        ("United States", "country"),
        ("Los Angeles", "city")
    ]
    relationships = [
        ("New York City", "United States", "city"),
        ("California", "United States", "state"),
        ("Los Angeles", "California", "city")
    ]

    # Create nodes
    for name, label in nodes:
        tx.run("CREATE (n:Node {name: $name, label: $label})", name=name, label=label)

    # Create relationships
    for start, end, relation in relationships:
        tx.run("""
            MATCH (a:Node {name: $start}), (b:Node {name: $end})
            CREATE (a)-[:RELATION {type: $relation}]->(b)
            """, start=start, end=end, relation=relation)
        


## DELETE ALL NODES
def delete_data():
    driver = neo4jConfig.getDriver()
    # Run deletion within a session
    with driver.session() as session:
        session.write_transaction(delete_all_nodes)

    # Close the driver
    driver.close()


## Delete all nodes from db
def delete_all_nodes(tx):
  # Delete all relationships and nodes
  tx.run("MATCH ()-[r]-() DELETE r")
  tx.run("MATCH (n) DELETE n")


def queryGeoDB():
   cypher_query = '''
   MATCH (n)
   OPTIONAL MATCH (n)-[r]->(m)
   RETURN n, r, m
   '''
   driver = neo4jConfig.getDriver()
   with driver.session(database="neo4j") as session:
    results = session.read_transaction(
      lambda tx: tx.run(cypher_query,
                        favorite="The Matrix").data())
    driver.close()
    print(results)
    return json.dumps(results)
   

# Function to create nodes and relationships in Neo4j
def create_graph(tx, country, state, city):
    query = (
        "MERGE (c:Country {name: $country}) "
        "MERGE (s:State {name: $state}) "
        "MERGE (ci:City {name: $city, isCapital: false}) "
        "MERGE (c)-[:HAS_STATE]->(s) "
        "MERGE (s)-[:HAS_CITY]->(ci)"
    )
    tx.run(query, country=country, state=state, city=city)


def insertFromCSV(df):
    driver = neo4jConfig.getDriver()
    # Insert data into Neo4j
    with driver.session() as session:
        for index, row in df.iterrows():
            session.write_transaction(create_graph, row['Country'], row['State'], row['City'])
    driver.close
    return "Inserted Successfully"

