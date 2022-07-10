# How to use a GreatAI service

After [creating a GreatAI service](/how-to-guides/cerate-service) by wrapping your prediction function, it's time to do some prediction.

Let's use the following example:

```python "type_safe_greeter.py"
from great_ai import GreatAI

@GreatAI.create
def type_safe_greeter(your_name: str) -> str:
    return f'Hi {your_name}'
```

