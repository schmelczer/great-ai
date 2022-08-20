# Summarising scientific publications from a tech-transfer perspective

This is a simplified example illustrating how `great-ai` is used in practice at [ScoutinScience](https://www.scoutinscience.com/){ target=_blank }. The subpages show `great-ai` in action by going over the lifecycle of fine-tuning and deploying a BERT-based software service.

??? note "Propriety data"
    The purpose of this example is to show you different ways in which `great-ai` can assist you. The exact NLP task being solved is not central. Stemming from this and from the difficult nature of obtaining appropriate training data, the propriety dataset used for the experiments is not shared.

## Objectives

1. You will see how the [great_ai.utilities](/reference/utilities) can integrate into your Data Science workflow.
2. You will see how [great_ai.large_file](/reference/large-file) can be used to version and store your trained model.
3. You will see how [GreatAI][great_ai.GreatAI] should be used to prepare your model for a robust and responsible deployment.
4. You will see multiple ways of customising your deployment.

## Overview

One of the core features of the ScoutinScience platform is summarising research papers from a tech-transfer perspective. In short, extractive summarisation is preferred using a binary classifier trained on clients' judgement of sentence interestingness. Thus, documents are sentences, and the expected output is a binary label showing whether a sentence is "worthy" of being in the tech-transfer summary. Explaining each decision is imperative since ScoutinScience embraces applying only explainable AI (XAI) methods wherever feasible.

!!! success
    You are ready to start the tutorial. Feel free to return to the [summary](#summary) section once you're finished.

<div style="display: flex; justify-content: space-evenly;" markdown>
[:material-database: Examine data](data.ipynb){ .md-button .md-button--primary }

[:fontawesome-solid-chart-simple: Train model](train.ipynb){ .md-button .md-button--primary }

[:material-cloud-tags: Deploy service](deploy.ipynb){ .md-button .md-button--primary }
</div>

## Summary

### [Data notebook](data.ipynb)

We load and analyse the data by calculating inter-rater reliability and checking the feasibility of using an AI-based approach by testing the accuracy of a trivial baseline method.

### [Training notebook](train.ipynb)

We simply fine-tune SciBERT.

After training and evaluating a model, it is exported using [great_ai.save_model][]. For more info, check out [the configuration how-to page](/how-to-guides/configure-service).

### [Deployment notebook](deploy.ipynb)

We customise the GreatAI configuration, create custom caching for the model and implement an inference function that can be hardened by wrapping it in a [GreatAI][great_ai.GreatAI] instance. We also extract the attention weights as a quasi-explanation.

Finally, we test the model's inference function through the GreatAI dashboard. [The only thing left is to deploy the hardened service properly.](/how-to-guides/use-service)

#### [Additional files](additional-files.md)

There are some other files required for deploying the notebook. For example, the config file for S3 and MongoDB or a Dockerfile for building a custom image. These are gathered and shown on a separate page.
