# pip install -U marvin

from marvin import ai_fn

@ai_fn
def spam_rating(email_body: str) -> int:
    """Returns a number between 0 and 100 
    that represents how likely the email is spam """

print(spam_rating("Hey, just following up about dinner tomorrow."))

print(spam_rating("Hi, I am your CEO and need you to go buy gaming gift cards."))

# first returned 42
# second returned 95