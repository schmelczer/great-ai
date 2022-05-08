import re
from typing import Dict, Iterable, List

from preprocess import preprocess
from pydantic import BaseModel
from sklearn.pipeline import Pipeline

from great_ai import log_argument, log_metric, use_model
from great_ai.utilities.clean import clean


class DomainPrediction(BaseModel):
    domain: str
    probability: float
    explanation: List[str]


@use_model("small-domain-prediction-v2", version="latest")
@log_argument("text", validator=lambda t: len(t) > 0)
def predict_domain(
    text: str, model: Pipeline, cut_off_probability: float = 0.2
) -> List[DomainPrediction]:
    assert 0 <= cut_off_probability <= 1
    log_metric("text_length", len(text))

    cleaned = clean(text, convert_to_ascii=True)
    text = re.sub(r"[^a-zA-Z0-9]", " ", cleaned)

    feature_names = model.named_steps["vectorizer"].get_feature_names_out()

    token_mapping = {preprocess(original): original for original in text.split(" ")}

    features = model.named_steps["vectorizer"].transform(
        [" ".join(token_mapping.keys())]
    )
    prediction = model.named_steps["classifier"].predict_proba(features)[0]
    best_classes = sorted(enumerate(prediction), key=lambda v: v[1], reverse=True)

    results: List[DomainPrediction] = []
    for class_index, probability in best_classes:
        weights = model.named_steps["classifier"].feature_log_prob_[class_index]

        results.append(
            DomainPrediction(
                domain=model.named_steps["classifier"].classes_[class_index],
                probability=round(probability * 100),
                explanation=_get_explanation(
                    feature_names=feature_names,
                    features=features.A[0],
                    weights=weights,
                    token_mapping=token_mapping,
                ),
            )
        )

        if sum(r.probability for r in results) >= cut_off_probability * 100:
            break

    return results


def _get_explanation(
    feature_names: Iterable[str],
    features: Iterable[float],
    weights: Iterable[float],
    token_mapping: Dict[str, str],
) -> List[str]:
    influential = [
        (value * weight, name)
        for name, value, weight in zip(feature_names, features, weights)
        if value
    ]

    most_influential = sorted(influential, reverse=True)[:5]

    return [token_mapping[v[1]] for v in most_influential]
