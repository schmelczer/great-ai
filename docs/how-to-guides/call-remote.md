# How to call remote GreatAI instances

Microservices architecture (or [SOA](https://en.wikipedia.org/wiki/Service-oriented_architecture)) work well with ML applications. This is because their interfaces are usually very narrow, while the functionality provided quite comprehensive. Hence, drawing the boundaries of responsibilities is more straightforward in the case of ML services than in the case of more traditional business applications. For this reason, it is common to have a tree of models (preferably wrapped in GreatAI instances) communicating with each other.

Although regular HTTP POST requests could be sent to each service's `/predict` endpoint, `great-ai` comes with two convenience functions: [call_remote_great_ai][great_ai.call_remote_great_ai] and [call_remote_great_ai_async][great_ai.call_remote_great_ai_async] to wrap this request. These provide you with some level of robustness and deserialisation.

!!! note "Inside notebooks"
    The async variant, [call_remote_great_ai_async][great_ai.call_remote_great_ai_async], requires a running event loop while the synchronous variant disallows other running event-loops. Therefore, when running inside a Jupyter Notebook, always call [call_remote_great_ai_async][great_ai.call_remote_great_ai_async].

## Simple example

Let's create two processes: a server and a client.

### Server

```python title="server.py"
from great_ai import GreatAI
from asyncio import sleep

@GreatAI.create
async def slow_greeter(your_name):
    await sleep(2)
    return f'Hi {your_name}!'
```
> Run this in development mode by executing `great-ai server.py` or `python3 -m great_ai server.py` if you're on Windows and [`great-ai` is not in your `PATH`](/how-to-guides/install).

### Client

```python title="client.py"
from great_ai import call_remote_great_ai

names = ['Olivér', 'Balázs', 'András']

results = [
    call_remote_great_ai(
        'http://localhost:6060',
        {
            'your_name': name
        }
    ).output #(1)
    for name in names
]

print(results)
```
1.  Only return the outputs so we don't clutter up the terminal.

> Run this script as a regular Python script by executing `python3 client.py`.

![screenshot of result](/media/remote-sync.png){ loading=lazy }

As you can see, everything worked as expected. There is one way to improve it though.
## An `async` example

Let's send multiple requests at the same time to speed up the overall execution time. To do this, we will use the [call_remote_great_ai_async][great_ai.call_remote_great_ai_async] function.

??? note "Why is this possible?"
    Note, that in `server.py`, the inference function is declared `async`. This means that multiple "copies" of it can run at the same time in the same thread. Since, there is no CPU-bottleneck, the server has a quite large throughpout (requests responded to per second), but its latency will stay around 2 seconds due to the async `sleep` command.

    If your great-ai server is not `async`, higher throughput can be achieved by running multiple instances of it, either manually, or by running it with multiple `uvicorn` workers like this: `ENVIRONMENT=production great-ai server.py --worker_count 4`

### Async client

```python title="async-client.py"
from great_ai import call_remote_great_ai_async
import asyncio

names = ['Olivér', 'Balázs', 'András']

async def main():
    futures = [
        call_remote_great_ai_async(
            'http://localhost:6060',
            {
                'your_name': name
            }
        ) for name in names
    ]
    
    results = await asyncio.gather(*futures)
    print([r.output for r in results])

asyncio.run(main())
```

> Replace `client.py` with this async client. Note that even though async support is significantly more streamlined in recent Python versions, it still requires a bit more boilerplate than its synchronous counterpart.

![screenshot of result](/media/remote-async.png){ loading=lazy }

This also works, and in some use cases might be considerably quicker.
