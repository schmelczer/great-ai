from great_ai import GreatAI


@GreatAI.create
def hello_world(name: str) -> str:
    """Learn more about GreatAI at https://github.com/schmelczer/great-ai"""
    
    return f"Hello {name}!"
