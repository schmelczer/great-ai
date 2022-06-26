from great_ai import GreatAI


@GreatAI.create
def hello_world(name: str) -> str:
    return f"Hello {name}!"
