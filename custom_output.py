"""
Show how to use custom outputs.

@dev You need to add OPENAI_API_KEY to your environment variables.
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from browser_use import ActionResult, Agent, Controller

load_dotenv()

controller = Controller()


class DoneResult(BaseModel):
	post_title: str
	post_url: str
	num_comments: int
	hours_since_post: int


@controller.registry.action('Done with task', param_model=DoneResult)
async def done(params: DoneResult):
	result = ActionResult(is_done=True, extracted_content=params.model_dump_json())
	return result

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")
async def main():
	task = 'Go to hackernews show hn and give me the number 1 post in the list'
	llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp",api_key=api_key),
	agent = Agent(task=task, llm=llm, controller=controller)

	history = await agent.run()

	result = history.final_result()
	if result:
		parsed = DoneResult.model_validate_json(result)
		print('--------------------------------')
		print(f'Title: {parsed.post_title}')
		print(f'URL: {parsed.post_url}')
		print(f'Comments: {parsed.num_comments}')
		print(f'Hours since post: {parsed.hours_since_post}')


if __name__ == '__main__':
	asyncio.run(main())