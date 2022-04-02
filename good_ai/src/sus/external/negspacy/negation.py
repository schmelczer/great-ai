import logging

from spacy.language import Language
from spacy.matcher import PhraseMatcher
from spacy.tokens import Token

from .termsets import termset

default_ts = termset("en").get_patterns()


@Language.factory(
    "negex",
    default_config={
        "neg_termset": default_ts,
        "extension_name": "negex",
        "chunk_prefix": list(),
    },
)
class Negex:
    """
        A spaCy pipeline component which identifies negated tokens in text.

        Based on: NegEx - A Simple Algorithm for Identifying Negated Findings and Diseasesin Discharge Summaries
    Chapman, Bridewell, Hanbury, Cooper, Buchanan

    Parameters
    ----------
    nlp: object
        spaCy language object
    termset_lang: str
        language code, if using default termsets (e.g. "en" for english)
    extension_name: str
        defaults to "negex"; whether entity is negated is then available as ent._.negex
    pseudo_negations: list
        list of phrases that cancel out a negation, if empty, defaults are used
    preceding_negations: list
        negations that appear before an entity, if empty, defaults are used
    following_negations: list
        negations that appear after an entity, if empty, defaults are used
    termination: list
        phrases that "terminate" a sentence for processing purposes such as "but". If empty, defaults are used

    """

    def __init__(
        self,
        nlp: Language,
        name: str,
        neg_termset: dict,
        extension_name: str,
        chunk_prefix: list,
    ):
        if not Token.has_extension(extension_name):
            Token.set_extension(extension_name, default=False, force=True)

        ts = neg_termset
        expected_keys = [
            "pseudo_negations",
            "preceding_negations",
            "following_negations",
            "termination",
        ]
        if not set(ts.keys()) == set(expected_keys):
            raise KeyError(
                f"Unexpected or missing keys in 'neg_termset', expected: {expected_keys}, instead got: {list(ts.keys())}"
            )

        self.pseudo_negations = ts["pseudo_negations"]
        self.preceding_negations = ts["preceding_negations"]
        self.following_negations = ts["following_negations"]
        self.termination = ts["termination"]

        self.nlp = nlp
        self.extension_name = extension_name
        self.build_patterns()
        self.chunk_prefix = list(nlp.tokenizer.pipe(chunk_prefix))

    def build_patterns(self):
        # efficiently build spaCy matcher patterns
        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")

        self.pseudo_patterns = list(self.nlp.tokenizer.pipe(self.pseudo_negations))
        self.matcher.add("pseudo", None, *self.pseudo_patterns)

        self.preceding_patterns = list(
            self.nlp.tokenizer.pipe(self.preceding_negations)
        )
        self.matcher.add("Preceding", None, *self.preceding_patterns)

        self.following_patterns = list(
            self.nlp.tokenizer.pipe(self.following_negations)
        )
        self.matcher.add("Following", None, *self.following_patterns)

        self.termination_patterns = list(self.nlp.tokenizer.pipe(self.termination))
        self.matcher.add("Termination", None, *self.termination_patterns)

    def process_negations(self, doc):
        """
        Find negations in doc and clean candidate negations to remove pseudo negations

        Parameters
        ----------
        doc: object
            spaCy Doc object

        Returns
        -------
        preceding: list
            list of tuples for preceding negations
        following: list
            list of tuples for following negations
        terminating: list
            list of tuples of terminating phrases

        """
        ###
        # does not work properly in spacy 2.1.8. Will incorporate after 2.2.
        # Relying on user to use NER in meantime
        # see https://github.com/jenojp/negspacy/issues/7
        ###
        # if not doc.is_nered:
        #     raise ValueError(
        #         "Negations are evaluated for Named Entities found in text. "
        #         "Your SpaCy pipeline does not included Named Entity resolution. "
        #         "Please ensure it is enabled or choose a different language model that includes it."
        #     )
        preceding = list()
        following = list()
        terminating = list()

        matches = self.matcher(doc)
        pseudo = [
            (match_id, start, end)
            for match_id, start, end in matches
            if self.nlp.vocab.strings[match_id] == "pseudo"
        ]

        for match_id, start, end in matches:
            if self.nlp.vocab.strings[match_id] == "pseudo":
                continue
            pseudo_flag = False
            for p in pseudo:
                if start >= p[1] and start <= p[2]:
                    pseudo_flag = True
                    continue
            if not pseudo_flag:
                if self.nlp.vocab.strings[match_id] == "Preceding":
                    preceding.append((match_id, start, end))
                elif self.nlp.vocab.strings[match_id] == "Following":
                    following.append((match_id, start, end))
                elif self.nlp.vocab.strings[match_id] == "Termination":
                    terminating.append((match_id, start, end))
                else:
                    logging.warnings(
                        f"phrase {doc[start:end].text} not in one of the expected matcher types."
                    )
        return preceding, following, terminating

    def termination_boundaries(self, doc, terminating):
        """
        Create sub sentences based on terminations found in text.

        Parameters
        ----------
        doc: object
            spaCy Doc object
        terminating: list
            list of tuples with (match_id, start, end)

        returns
        -------
        boundaries: list
            list of tuples with (start, end) of spans

        """
        sent_starts = [sent.start for sent in doc.sents]
        terminating_starts = [t[1] for t in terminating]
        starts = sent_starts + terminating_starts + [len(doc)]
        starts.sort()
        boundaries = list()
        index = 0
        for i, start in enumerate(starts):
            if not i == 0:
                boundaries.append((index, start))
            index = start
        return boundaries

    def negex(self, doc):
        """
        Negates entities of interest

        Parameters
        ----------
        doc: object
            spaCy Doc object

        """
        preceding, following, terminating = self.process_negations(doc)
        boundaries = self.termination_boundaries(doc, terminating)
        for b in boundaries:
            sub_preceding = [i for i in preceding if b[0] <= i[1] < b[1]]
            sub_following = [i for i in following if b[0] <= i[1] < b[1]]

            for e in doc[b[0] : b[1]]:
                if any(pre < e.i for pre in [i[1] for i in sub_preceding]):
                    e._.set(self.extension_name, True)
                    continue
                if any(fol > e.i for fol in [i[2] for i in sub_following]):
                    e._.set(self.extension_name, True)
                    continue
                if self.chunk_prefix:
                    if any(
                        e.text.lower().startswith(c.text.lower())
                        for c in self.chunk_prefix
                    ):
                        e._.set(self.extension_name, True)
        return doc

    def __call__(self, doc):
        return self.negex(doc)
