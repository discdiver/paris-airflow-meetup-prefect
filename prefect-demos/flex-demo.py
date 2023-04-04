import random
import httpx
from prefect import flow, task

@flow(retries=3)
def fetch_cat_fact():
    return httpx.get("https://catfact.ninja/fact?max_length=140").json()["fact"]

@task
def formatting(fact: str):
    return fact.title()

@task
def uppercase(fact: str):
    return fact.upper()

@task
def write_fact(fact: str):
    with open("fact.txt", "w+") as f:
        f.write(fact)
    return fact

@flow(log_prints=True)
def pipe():
    fact = fetch_cat_fact()
    for x in range(5):
        val = random.choice([True, False])
        if val:
            fact = formatting(fact)
        else: 
            fact = uppercase(fact)
    msg = write_fact(fact)
    print(msg)

if __name__ == "__main__":
    pipe()