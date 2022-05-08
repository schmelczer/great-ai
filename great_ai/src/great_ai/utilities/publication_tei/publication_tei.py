from functools import cached_property
from typing import Any, List, Optional, Union

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from great_ai.utilities.publication_tei.models.element import Paragraph

from ..clean import clean
from .models import Affiliation, Author, Element, Meta, PublicationMetadata, Text, Title


class PublicationTEI:
    def __init__(self, tei: str):
        self._document_order_counter = 0

        if tei:
            cleaned_xml = clean(tei, ignore_xml=True)
            self.soup = BeautifulSoup(cleaned_xml, "xml")
        else:
            self.soup = BeautifulSoup()

    @cached_property
    def publication_metadata(self) -> PublicationMetadata:
        publication_date = (
            self.soup.publicationStmt.date.get("when")
            if self.soup.publicationStmt and self.soup.publicationStmt.date
            else None
        )

        keywords = (
            [self._element_to_text(k) for k in self.soup.keywords.find_all("term")]
            if self.soup.keywords
            else []
        )

        return PublicationMetadata(
            language=self.soup.teiHeader.get("xml:lang")
            if self.soup.teiHeader
            else None,
            title=self._element_to_text(self.soup.title),
            publisher=self._element_to_text(self.soup.publisher),
            doi=self._element_to_text(self.soup.find("idno", type="DOI")),
            md5=self._element_to_text(self.soup.find("idno", type="MD5")),
            publication_date=publication_date,
            keywords=keywords,
            reference_count=self.get_reference_count(),
        )

    def get_reference_count(self) -> int:
        references = self.soup.find("div", {"type": "references"})

        if not references:
            return 0

        return len(references.findAll("biblStruct"))

    @cached_property
    def authors(self) -> List[Author]:
        if not self.soup.analytic:
            return []

        return [
            self._parse_author(author)
            for author in self.soup.analytic.find_all("author")
        ]

    @cached_property
    def content(self) -> List[Element]:
        self._document_order_counter = 0
        return self._get_elements(self.soup)

    @cached_property
    def sentences(self) -> List[Text]:
        return [
            sentence
            for element in self.content
            if isinstance(element, Paragraph)
            for sentence in element.sentences
        ]

    def _parse_author(self, raw: Tag) -> Author:
        return Author(
            name=(
                clean(" ".join(name.get_text() for name in raw.persName))
                if raw.persName
                else None
            ),
            orcid=self._element_to_text(raw.find(attrs={"type": "ORCID"})),
            email=self._element_to_text(raw.email),
            corresponding=raw.get("role") == "corresp",
            affiliations=[
                self._parse_affiliation(aff) for aff in raw.find_all("affiliation")
            ],
            coordinates=raw.persName.get("coords") if raw.persName else None,
        )

    def _parse_affiliation(self, raw: Tag) -> Affiliation:
        return Affiliation(
            institutions=[
                self._element_to_text(v)
                for v in raw.find_all("orgName", attrs={"type": "institution"})
            ],
            departments=[
                self._element_to_text(v)
                for v in raw.find_all("orgName", attrs={"type": "department"})
            ],
            laboratories=[
                self._element_to_text(v)
                for v in raw.find_all("orgName", attrs={"type": "laboratory"})
            ],
            country=self._element_to_text(raw.address.country)
            if raw.address and raw.address.country
            else None,
            settlement=self._element_to_text(raw.address.settlement)
            if raw.address and raw.address.settlement
            else None,
        )

    def _get_elements(self, raw: Tag) -> List[Element]:
        results: List[Element] = []

        for r in raw.find_all(["abstract", "div", "head", "p"]):
            if r.name == "abstract":
                results.append(Meta(meta_type="abstract_start"))
                results.extend(self._get_primitives(r))
                results.append(Meta(meta_type="abstract_end"))
            elif r.name == "div" and r.get("type") == "acknowledgement":
                results.append(Meta(meta_type="acknowledgements_start"))
                results.extend(self._get_primitives(r))
                results.append(Meta(meta_type="acknowledgements_end"))
            elif r.name == "div" and r.get("type") == "annex":
                results.append(Meta(meta_type="annex_start"))
                results.extend(self._get_primitives(r))
                results.append(Meta(meta_type="annex_end"))
            elif not r.find_parents(["abstract", "div"]):
                results.extend(self._get_primitives(r))

        return results

    def _get_primitives(self, raw: Tag) -> List[Element]:
        results: List[Element] = []

        for r in raw.find_all(["head", "p"]):
            if r.name == "head" and r.get("coords") and r.get_text():
                results.append(Title(text=self._parse_text(r)))
            elif r.name == "p" and r.find_all("s"):
                results.append(
                    Paragraph(
                        sentences=[
                            self._parse_text(sentence)
                            for sentence in r.find_all("s")
                            if sentence.get_text()
                        ]
                    )
                )

        return results

    def _element_to_text(
        self, element: Optional[NavigableString], default: Any = None
    ) -> Union[str, Any]:
        return (
            clean(element.get_text(separator=" ", strip=True)) if element else default
        )

    def _parse_text(self, raw: Tag) -> Text:
        return Text(
            content=clean(raw.get_text()),
            document_order=self._generate_document_order_id(),
            coordinates=raw.get("coords"),
        )

    def _generate_document_order_id(self) -> int:
        value = self._document_order_counter
        self._document_order_counter += 1
        return value
