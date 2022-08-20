# Train and deploy a SOTA model

Let's see `great-ai` in action by going over the lifecycle of a simple service.

## Objectives

1. You will see how the [great_ai.utilities](/reference/utilities) can integrate into your Data Science workflow.
2. You will use [great_ai.large_file](/reference/large-file) to version and store your trained model.
3. You will use [GreatAI][great_ai.GreatAI] to prepare your model for a robust and responsible deployment.

## Overview

You will train a field of study (domain) classifier for scientific sentences. The exact task was proposed by the [SciBERT paper](https://arxiv.org/abs/1903.10676){ target=_blank } in which SciBERT [achieved an F1-score of 0.6571](https://paperswithcode.com/sota/sentence-classification-on-paper-field){ target=_blank }. We are going to outperform it using a trivial text classification model: a [Linear SVM](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html){ target=_blank }.

We use the same synthetic dataset derived from the [Microsoft Academic Graph](https://www.microsoft.com/en-us/research/project/microsoft-academic-graph/){ target=_blank }. The dataset is [available here](https://github.com/allenai/scibert/tree/master/data/text_classification/mag){ target=_blank }.

!!! success
    You are ready to start the tutorial. Feel free to return to the [summary](#summary) section once you're finished.

<div style="display: flex; justify-content: space-evenly;" markdown>
[:fontawesome-solid-chart-simple: Train it](train.ipynb){ .md-button .md-button--primary }

[:material-cloud-tags: Deploy it](deploy.ipynb){ .md-button .md-button--primary }
</div>

## Summary

### [Training notebook](train.ipynb)

We load and preprocess the dataset while relying on [great_ai.utilities.clean][great_ai.utilities.clean.clean] for doing the heavy-lifting. Additionally, the preprocessing is parallelised using [great_ai.utilities.simple_parallel_map][]

After training and evaluating a model, it is exported using [great_ai.save_model][].

??? tip "Remote storage"
    To store your model remotely, you must set your credentials before calling `save_model`.

    For example, to use [AWS S3](https://aws.amazon.com/s3){ target=_blank }:
    ```python
    from great_ai.large_file import LargeFileS3

    LargeFileS3.configure(
        aws_region_name='eu-west-2',
        aws_access_key_id='MY_AWS_ACCESS_KEY',
        aws_secret_access_key='MY_AWS_SECRET_KEY',
        large_files_bucket_name='my_bucket_for_models'
    )

    from great_ai import save_model

    save_model(model, key='my-domain-predictor')
    ```

    For more info, checkout [the configuration how-to page](/how-to-guides/configure-service).

### [Deployment notebook](deploy.ipynb)

We create an inference function that can be hardened by wrapping it in a [GreatAI][great_ai.GreatAI] instance.

```python
from great_ai import GreatAI, use_model
from great_ai.utilities import clean

@GreatAI.create
@use_model('my-domain-predictor')   #(1)
def predict_domain(sentence, model):
    inputs = [clean(sentence)]
    return str(model.predict(inputs)[0])
```

1.  [@use_model][great_ai.use_model] loads and injects your model into the `predict_domain` function's `model` argument.
    You can freely reference it, knowing that the function is always provided with it.

Finally, we test the model's inference function through the GreatAI dashboard. [The only thing left is to deploy the hardened service properly.](/how-to-guides/use-service)

<div style="display: flex; justify-content: space-evenly;" markdown>  
[:material-book: Learn about all the features](/how-to-guides/create-service){ .md-button .md-button--primary }

[:material-test-tube: Look at more examples](/examples/simple/data){ .md-button .md-button--secondary }
</div>
