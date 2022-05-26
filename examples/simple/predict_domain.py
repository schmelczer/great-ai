from typing import Dict, Iterable, List
from great_ai import GreatAI, use_model, ClassificationOutput
from sklearn.pipeline import Pipeline

from helpers import lemmatize, preprocess


@GreatAI.deploy
@use_model("small-domain-prediction-v2", version="latest")
def predict_domain(text: str, model: Pipeline, target_confidence: float = 20) -> List[ClassificationOutput]:
    """
    Predict the scientific domain of the input text.
    Return labels until their sum likelihood is larger than target_confidence.
    """
    assert 0 <= target_confidence <= 100, "invalid argument"

    text = preprocess(text)

    token_mapping = {lemmatize(original): original for original in text.split(" ")}
    feature_names = [
        token_mapping.get(name)
        for name in model.named_steps["vectorizer"].get_feature_names_out()
    ]

    features = model.named_steps["vectorizer"].transform(
        [" ".join(token_mapping.keys())]
    )
    prediction = model.named_steps["classifier"].predict_proba(features)[0]
    best_classes = sorted(enumerate(prediction), key=lambda v: v[1], reverse=True)

    results: List[ClassificationOutput] = []
    for class_index, probability in best_classes:
        weights = model.named_steps["classifier"].feature_log_prob_[class_index]
        domain = model.named_steps["classifier"].classes_[class_index]

        results.append(
            ClassificationOutput(
                label=domain,
                confidence=round(probability * 100),
                explanation=_get_explanation(
                    weights=weights,
                    counts=features.A[0],
                    words=feature_names,
                ),
            )
        )

        if sum(r.confidence for r in results) >= target_confidence:
            break

    return results


def _get_explanation(
    weights: Iterable[float],
    counts: Iterable[float],
    words: Iterable[str],
) -> List[str]:
    most_influential = sorted((
        (weight, word)
        for weight, count, word in zip(weights, counts, words)
        if count > 0
    ), reverse=True)[:5]

    return [word for _, word in most_influential]
