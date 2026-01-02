import asyncio
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv

load_dotenv()


async def main():
    mcp_servers = {
        "neo4j": {
            "transport": "http",
            "url": "http://localhost:8000/mcp",
        }
    }

    client = MultiServerMCPClient(mcp_servers)

    tools = await client.get_tools()
    print(tools)

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    agent = create_agent(llm, tools)

    response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "Who acted in Toy Story?"}]}
    )
    print("---")
    for message in response["messages"]:
        print(message)
        print("---")
    print(response["messages"][-1].content)


asyncio.run(main())
