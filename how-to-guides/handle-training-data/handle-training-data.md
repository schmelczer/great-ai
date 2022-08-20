# How to manage training data

In order to simplify your training data management, `great-ai` provide two complementing approaches for inputting new data points.

## Upload data

At the start of your experiments' first iteration, after you've gathered suitable samples for training, you can call [great_ai.add_ground_truth][]. This automatically stores a timestamp and also allows you to assign tags to the data. Using these attributes, [great_ai.query_ground_truth][] can be called to get a filtered view of the training data.

!!! important "Train-test-validation splits"
    It is a best practice to lock away the test split of your data that is only used for the final quality assessment. This prevents you from accidentally training on it or inadvertently tuning the model to have the highest accuracy metrics on the test split. This, of course, may lead to dubious results; hence, care must be taken to avoid it.
    
    With [great_ai.add_ground_truth][], there is an option to tag the samples with `train`, `test`, and `validation` randomly, following a predefined distribution. This happens as soon as they're written in the database. Later, these can be queried by providing the name of the appropriate tags.

The nice thing about this is that the 'input-expected output' pairs are stored as traces. Thus, they behave exactly like regular prediction traces.

```python
from great_ai import add_ground_truth

add_ground_truth(
    [1, 2],
    ['odd', 'even'],
    tags='my_tag',
    train_split_ratio=1,  #(1)
    test_split_ratio=1
)
```

1. Note that the ratios don't have to add up to 1. They are just weights. There is also a `validation_split_ratio` which is 0 by default.

```python
>>> from great_ai import query_ground_truth
>>> query_ground_truth('my_tag')    
[Trace[str]({'created': '2022-07-12T18:36:12.825706',
   'exception': None,
   'feedback': 'odd',  #(1)
   'logged_values': {'input': 1},  #(2)
   'models': [],
   'original_execution_time_ms': 0.0,
   'output': 'odd',
   'tags': ['ground_truth', 'test', 'my_tag'], #(3) 
   'trace_id': '4fcf2ce6-a172-469d-94b2-874577655814'}),
 Trace[str]({'created': '2022-07-12T18:36:12.825706',
   'exception': None,
   'feedback': 'even',
   'logged_values': {'input': 2},
   'models': [],
   'original_execution_time_ms': 0.0,
   'output': 'even',
   'tags': ['ground_truth', 'train', 'my_tag'],
   'trace_id': 'abee0671-beb9-4284-8c3b-c65e5836ce38'})]
```

1. Expected output. This can also be accessed through the `.output` property.
2. The input value is stored here.
3. Notice how `ground_truth` is always included as a tag when using [great_ai.add_ground_truth][]. 

## Get feedback

After the initial data gathering, end-to-end feedback can also be integrated into the dataset. 

The scaffolded REST API contains endpoints for managing traces and their feedbacks.

![screenshot of swagger](/media/feedback.png){ loading=lazy }

When [great_ai.query_ground_truth][] is executed, it implicitly filters for traces that have feedback. Therefore, both the `ground_truth` and the `online` traces that have received feedback are returned. No matter the origin of the data, it can be accessed using the same API.

## Remove clutter

Traces can be deleted either through the REST API or by calling [great_ai.delete_ground_truth][]. The latter provides the same interface as [great_ai.query_ground_truth][] except it deletes the matched points.
