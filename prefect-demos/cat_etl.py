import httpx


def fetch_cat_fact():  
    return httpx.get("https://catfact.ninja/fact?max_length=140").json()["fact"]


def formatting(fact: str): 
    return fact.title()


def write_fact(fact: str): 
    with open("fact.txt", "w+") as f:
        f.write(fact)
    return fact


def pipe():  
    fact = fetch_cat_fact()
    formatted_fact = formatting(fact)
    msg = write_fact(formatted_fact)
    print(msg)


if __name__ == "__main__":
    pipe()