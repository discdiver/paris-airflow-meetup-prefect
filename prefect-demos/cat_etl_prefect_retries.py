import random
import httpx
from prefect import flow, task

@task(retries=3)
def fetch_cat_fact():
    buggy_api_result = random.choice([True, False])
    if buggy_api_result:
        raise Exception("API Failure. 😢")
    return httpx.get("https://catfact.ninja/fact?max_length=140").json()["fact"]

@task
def formatting(fact: str):
    return fact.title()

@task
def write_fact(fact: str):
    with open("fact.txt", "w+") as f:
        f.write(fact)
    return "Success!"

@flow(log_prints=True)
def pipe():
    fact = fetch_cat_fact()
    formatted_fact = formatting(fact)
    msg = write_fact(formatted_fact)
    print(fact)

if __name__ == "__main__":
    pipe()