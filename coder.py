import os
import sys

from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from langchain_google_genai import ChatGoogleGenerativeAI
import asyncio

from browser_use import Agent, Browser, Controller

async def main():
    browser = Browser()
    async with await browser.new_context() as context:
        model =ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp",api_key=api_key)

        # Initialize browser agent
        agent1 = Agent(
            task='Open an online code editor programiz.',
            llm=model,
            browser_context=context,
        )
        executor = Agent(
            task='Executor. Execute the code written by the coder and suggest some updates if there are errors.',
            llm=model,
            browser_context=context,
        )

        coder = Agent(
            task='Coder. Your job is to write and complete code. You are an expert coder. Code a simple calculator. Write the code of printing odd numbers the coding interface after agent1 has opened the link.',
            llm=model,
            browser_context=context,
        )
        await agent1.run()
        await executor.run()
        await coder.run()

asyncio.run(main())