from typing import Iterable, List, Optional

from great_ai import ClassificationOutput, GreatAI, use_model
from sklearn.pipeline import Pipeline

from helpers import lemmatize, preprocess


@GreatAI.deploy
@use_model("small-domain-prediction-v2", version="latest")
def predict_domain(
    text: str, model: Pipeline, target_confidence: float = 20
) -> List[ClassificationOutput]:
    """
    Predict the scientific domain of the input text.
    Return labels until their sum likelihood is larger than target_confidence.
    """
    assert 0 <= target_confidence <= 100, "invalid argument"

    processed = [(word, lemmatize(word)) for word in preprocess(text).split(" ")]
    token_mapping = dict(processed)
    clean_input = " ".join(v[1] for v in processed)

    feature_names = [
        token_mapping.get(name)
        for name in model.named_steps["vectorizer"].get_feature_names_out()
    ]

    prediction = model.predict_proba([clean_input])[0]
    best_classes = sorted(enumerate(prediction), key=lambda v: v[1], reverse=True)

    results: List[ClassificationOutput] = []
    for class_index, probability in best_classes:
        results.append(
            ClassificationOutput(
                label=model.named_steps["classifier"].classes_[class_index],
                confidence=round(probability * 100),
                explanation=_get_explanation(
                    weights=model.named_steps["classifier"].feature_log_prob_[
                        class_index
                    ],
                    words=feature_names,
                ),
            )
        )

        if sum(r.confidence for r in results) >= target_confidence:
            break

    return results


def _get_explanation(
    weights: Iterable[float],
    words: Iterable[Optional[str]],
) -> List[str]:
    most_influential = sorted(
        ((weight, word) for weight, word in zip(weights, words) if word),
        reverse=True,
    )[:5]

    return [word for _, word in most_influential]
