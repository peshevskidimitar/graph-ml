import os

from neo4j import GraphDatabase, basic_auth
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.environ["NEO4J_URI"],
    auth=basic_auth(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
)

mcp = FastMCP("neo4j-mcp")


@mcp.tool()
def get_cast(movie_title: str) -> list:
    """
    Returns the list of actors in a given movie.
    """
    query = """
    MATCH (p:Person)-[:ACTED_IN]->(m:Movie {title: $title})
    RETURN p.name AS person
    """
    with driver.session() as session:
        result = session.run(query, title=movie_title)
        return [record["person"] for record in result]


if __name__ == "__main__":
    mcp.run("streamable-http")
