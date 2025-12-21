import asyncio
import sys

from maf_workflow.workflow import execute_workflow


async def main(message) -> None:
    await execute_workflow(message)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py '<message_text>'")
    else:
        asyncio.run(main(sys.argv[1]))
