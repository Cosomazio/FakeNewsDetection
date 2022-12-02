from neo4j import GraphDatabase

driver = GraphDatabase.driver(uri="bolt://localhost:11003",auth=("neo4j","pass"))
session = driver.session()


q1 = """
call apoc.import.json("/Users/cosimocorbisiero/Documents/GitHub/FakeNewsDetection/CommunityDetection/noteTweet.json")
"""

q2="""
match(n) return COUNT(n)
"""
session.run(q1)
(session.run(q2))
