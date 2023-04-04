from marvin import ai_fn

@ai_fn
def list_fruits(n: int) -> list[str]:
    """Generate a list of n fruits"""

print(list_fruits(20))