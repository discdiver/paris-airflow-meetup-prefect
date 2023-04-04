from prefect import flow, task
from anyio import run

@task
async def dummy_task(input_task=None):
    return

@flow
async def test_multiple_short_task_chains():
    breadth = 10
    level_1 = [await dummy_task.submit() for _ in range(breadth)]
    level_2 = [await dummy_task.submit(level_1[i]) for i in range(breadth)]


if __name__ == "__main__":
    run(test_multiple_short_task_chains)
    