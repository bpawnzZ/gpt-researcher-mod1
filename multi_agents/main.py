from dotenv import load_dotenv
from .agents import ChiefEditorAgent
import asyncio
import json
import os

# Run with LangSmith if API key is set
if os.environ.get("LANGCHAIN_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
load_dotenv()

def open_task():
    with open('task.json', 'r') as f:
        task = json.load(f)

    if not task:
        raise Exception("No task provided. Please include a task.json file in the root directory.")

    return task

async def run_research_task(query, websocket=None, stream_output=None, headers=None):
    task = {
        "query": query,
        "max_sections": 3,
        "publish_formats": {
            "markdown": True,
            "pdf": True,
            "docx": True
        },
        "follow_guidelines": False,
        "model": "gpt-4o",
        "guidelines": [
            "The report MUST be written in APA format",
            "Each sub section MUST include supporting sources using hyperlinks. If none exist, erase the sub section or rewrite it to be a part of the previous section",
            "The report MUST be written in spanish"
        ],
        "verbose": True
    }

    chief_editor = ChiefEditorAgent(task, websocket, stream_output, headers)
    research_report = await chief_editor.run_research_task()

    if websocket and stream_output:
        await stream_output("logs", "research_report", research_report, websocket)

    return research_report

async def main():
    task = open_task()

    chief_editor = ChiefEditorAgent(task)
    research_report = await chief_editor.run_research_task()

    return research_report

if __name__ == "__main__":
    asyncio.run(main())