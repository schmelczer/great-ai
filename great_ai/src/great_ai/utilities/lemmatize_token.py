from spacy.tokens import Token

from .data import american_spellings


def lemmatize_token(
    token: Token,
    add_negation: bool = False,
    add_part_of_speech: bool = False,
) -> str:
    lemma = token.lemma_.lower()

    lemma = american_spellings.get(lemma, lemma)

    if add_part_of_speech:
        lemma = f"{lemma}_{token.pos_}"
    if add_negation and token._.negex:
        lemma = f"NOT_{lemma}"

    return lemma
