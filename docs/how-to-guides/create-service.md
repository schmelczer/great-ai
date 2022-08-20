# How to create a GreatAI service

The core value of `great-ai` lies in its [GreatAI][great_ai.GreatAI] class. To take advantage of it, you need to create an instance wrapping your code.

Let's say that you have the following greeter function:

```python title="greeter.py"
def my_greeter_function(your_name):
    return f'Hi {your_name}!'
```

You can simply decorate (wrap) this function using the [@GreatAI.create][great_ai.GreatAI.create] factory.

```python title="greeter.py"
from great_ai import GreatAI

@GreatAI.create
def greeter(your_name):
    return f'Hi {your_name}!'
```

??? info "Why not simply use `@GreatAI?`"
    The purpose of [@GreatAI.create][great_ai.GreatAI.create] is simply to provide you with type-checking through MyPy, Pylance, and similar libraries. However, the overloading support for `__new__` is lacking in MyPy. Thus, a static factory method is used instead.

## With types

Even though it's not required by GreatAI, [type annotating your codebase](https://realpython.com/python-type-checking/){ target=_blank } can save you from lots of trivial mistakes; that's why it's highly advised. Simply add the expected types to your function's signature.

```python title="type_safe_greeter.py"
from great_ai import GreatAI

@GreatAI.create
def type_safe_greeter(your_name: str) -> str:
    return f'Hi {your_name}!'
```

This not only allows you to statically type-check your code, but by default, GreatAI will check it during runtime as well using [typeguard](https://github.com/agronholm/typeguard){ target=_blank }.

## With async

Asynchronous code can result in immense performance gains in some instances. For example, you might rely on a third-party service, do database access, or [call a remote GreatAI instance](/how-to-guides/call-remote). In these cases, you can make your function `async` without any other changes.

```python title="async_greeter.py"
from great_ai import GreatAI
from asyncio import sleep

@GreatAI.create
async def async_greeter(your_name: str) -> str:
    await sleep(2)  # simulate IO-bound operation
    return f'Hi {your_name}!'
```

## With decorators

GreatAI can decorate already decorated functions. The only restriction is that [@GreatAI.create][great_ai.GreatAI.create] must come last. There are two built-in decorators that you can use to customise your function, but you can use any third-party decorator as well.

### Using `@use_model`

If you have previously saved a model with [save_model][great_ai.save_model], you can inject it into your function by calling [@use_model][great_ai.use_model].

```python title="greeter_with_model.py"
from great_ai import GreatAI, use_model

@GreatAI.create
@use_model('name_of_my_model', version='latest')  #(1)
def type_safe_greeter(your_name: str, model) -> str:
    return f'Hi {your_name}!'

assert type_safe_greeter('Andras').output == 'Hi Andras'
```

1. By default, the parameter named `model` will be replaced by the loaded model. This behaviour can be customised by setting the `model_kwarg_name`. This way, even multiple models can be injected into a single function.

!!! important
    You must call [@use_model][great_ai.use_model] before [@GreatAI.create][great_ai.GreatAI.create]. Note that decorators are applied starting from the bottom-most one. Feel free to use [@use_model][great_ai.use_model] in other places of the codebase, and it works equally well outside GreatAI services. 

### Using `@parameter`

If you wish to turn off logging or specify custom validation for your parameters, you can use the [@parameter][great_ai.parameter] decorator.

!!! note
    By default, all parameters that are not affected by an explicit [@parameter][great_ai.parameter] or [@use_model][great_ai.use_model] are automatically decorated with [@parameter][great_ai.parameter] when [@GreatAI.create][great_ai.GreatAI.create] is called.

```python title="greeter_with_validation.py"
from great_ai import GreatAI, use_model

@GreatAI.create
@parameter('your_name', disable_logging=True)
def type_safe_greeter(your_name: str, model) -> str:
    return f'Hi {your_name}!'

assert type_safe_greeter('Andras').output == 'Hi Andras'
```

!!! important
    You must call [@parameter][great_ai.parameter] before [@GreatAI.create][great_ai.GreatAI.create]. Note that decorators are applied starting from the bottom-most one. Feel free to use [@parameter][great_ai.parameter] in other places of the codebase, and it works equally well outside GreatAI services. 

## Complex example

The following example summarises the options you have when instantiating a GreatAI service.

```python title="complex.py"
from great_ai import save_model, GreatAI, parameter, use_model, log_metric

save_model(4, 'secret-number')  #(1)

@GreatAI.create
@parameter('positive_number', validate=lambda n: n > 0, disable_logging=True)
@use_model('secret-number', version='latest', model_kwarg_name='secret')
def add_number(positive_number: int, secret: int) -> int:
    log_metric(
        'log directly into the returned Trace', 
        positive_number * 2
    )
    return positive_number + secret

assert add_number(1).output == 5
```

1. Refer to [the configuration page](/how-to-guides/configure-service) for specifying where to store your models. 
