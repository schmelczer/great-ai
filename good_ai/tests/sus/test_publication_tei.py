import unittest
from pathlib import Path

from src.good_ai.utilities.publication_tei import PublicationTEI

from .data.parsed import authors, content, metadata, sentences

DATA_PATH = Path(__file__).parent.resolve() / "data"


class TestPublicationTEI(unittest.TestCase):
    test_xml: str

    @classmethod
    def setUpClass(cls) -> None:
        with open(
            DATA_PATH / "10.1136_bmjspcare-2021-003026.pdf.tei.xml", encoding="utf-8"
        ) as f:
            cls.test_xml = f.read()

    def test_metadata_extraction(self) -> None:
        self.assertEqual(PublicationTEI(self.test_xml).publication_metadata, metadata)

    def test_authors(self) -> None:
        self.assertEqual(PublicationTEI(self.test_xml).authors, authors)

    def test_content(self) -> None:
        self.assertEqual(PublicationTEI(self.test_xml).content, content)

    def test_sentences(self) -> None:
        self.assertEqual(PublicationTEI(self.test_xml).sentences, sentences)

    def test_empty1(self) -> None:
        tei = PublicationTEI("<TEI/>")
        tei.publication_metadata, tei.publication_metadata, tei.authors, tei.content, tei.sentences

    def test_empty2(self) -> None:
        tei = PublicationTEI("")
        tei.publication_metadata, tei.publication_metadata, tei.authors, tei.content, tei.sentences

    def test_missing_fields(self) -> None:
        with open(DATA_PATH / "bad.tei.xml", encoding="utf-8") as f:
            tei = PublicationTEI(f.read())
        tei.publication_metadata, tei.publication_metadata, tei.authors, tei.content, tei.sentences
