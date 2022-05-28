#!/usr/bin/env python
# coding: utf-8

# # Train a domain classifier on the [semantic scholar dataset](https://api.semanticscholar.org/corpus)
#
# ## Part 3: Create production inference function
#
# In the [previous notebook](train.ipynb), we trained our AI model. Now, it's time to create **G**eneral **R**obust **E**nd-to-end **A**utomated **T**rustworthy deployment from it using the `GreatAI` Python package.

# In[1]:


import re
from typing import List

from great_ai import ClassificationOutput, GreatAI, use_model
from great_ai.utilities.clean import clean
from sklearn.pipeline import Pipeline

# In[2]:


@GreatAI.deploy
@use_model("small-domain-prediction-v2", version="latest")
def predict_domain(
    text: str, model: Pipeline, target_confidence: int = 20
) -> List[ClassificationOutput]:
    """
    Predict the scientific domain of the input text.
    Return labels until their sum likelihood is larger than target_confidence.
    """
    assert 0 <= target_confidence <= 100, "invalid argument"

    preprocessed = re.sub(r"[^a-zA-Z ]", "", clean(text, convert_to_ascii=True))
    features = model.named_steps["vectorizer"].transform([preprocessed])
    prediction = model.named_steps["classifier"].predict_proba(features)[0]

    best_classes = sorted(enumerate(prediction), key=lambda v: v[1], reverse=True)

    results: List[ClassificationOutput] = []
    for class_index, probability in best_classes:
        results.append(
            ClassificationOutput(
                label=model.named_steps["classifier"].classes_[class_index],
                confidence=round(probability * 100),
                explanation=[
                    word
                    for _, word in sorted(
                        (
                            (weight, word)
                            for weight, word, count in zip(
                                model.named_steps["classifier"].feature_log_prob_[
                                    class_index
                                ],
                                model.named_steps["vectorizer"].get_feature_names_out(),
                                features.A[0],
                            )
                            if count > 0
                        ),
                        reverse=True,
                    )
                ][:5],
            )
        )

        if sum(r.confidence for r in results) >= target_confidence:
            break

    return results


# In[3]:


result = predict_domain(
    """
    State-of-the-art methods for zero-shot visual recognition formulate learning as a joint embedding problem of images and side information. In these formulations the current best complement to visual features are attributes: manually encoded vectors describing shared characteristics among categories. Despite good performance, attributes have limitations: (1) finer-grained recognition requires commensurately more, and (2) attributes do not provide a natural language interface. We propose to overcome these limitations by training neural language models from scratch; i.e. without pre-training and only consuming words and characters. Our proposed models train end-to-end to align with the fine-grained and category-specific content of images. Natural language provides a flexible and compact way of encoding only the salient visual aspects for distinguishing categories. By training on raw text, our model can do inference on raw text as well, providing humans a familiar mode both for annotation and retrieval. Our model achieves strong performance on zero-shot text-based image retrieval and significantly outperforms the attribute-based state-of-the-art for zero-shot classification on the CaltechUCSD Birds 200-2011 dataset. """
)

from pprint import pprint

pprint(result.dict(), width=120)
