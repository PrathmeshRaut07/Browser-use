import asyncio
import os

import dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use.agent.service import Agent
from browser_use.controller.service import Controller
from dotenv import load_dotenv
load_dotenv()
api_key=os.getenv("GOOGLE_API_KEY")



controller = Controller()


class WebpageInfo(BaseModel):
	link: str = 'https://appointment.mfa.gr/en/reservations/aero/ireland-grcon-dub/'


@controller.action('Go to the webpage', param_model=WebpageInfo)
def go_to_webpage(webpage_info: WebpageInfo):
	return webpage_info.link


async def main():
	task = (
		'Go to the Greece MFA webpage via the link I provided you.'
		'Check the visa appointment dates. If there is no available date in this month, check the next month.if about:blank url page is open ed than you can open new tab for process'
		'If there is no available date in both months, tell me there is no available date.'
	)

	model =ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp",api_key=api_key)
	agent = Agent(task, model, controller=controller, use_vision=True)

	result = await agent.run()


if __name__ == '__main__':
	asyncio.run(main())