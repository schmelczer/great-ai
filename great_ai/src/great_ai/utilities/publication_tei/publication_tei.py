import os
import re
from functools import cached_property, lru_cache
from pathlib import Path
from typing import Any, List, Optional, Pattern, Tuple, Union

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag
from sus.publication_tei.models.element import Paragraph

from ..clean import clean
from ..lemmatize_text import lemmatize_text
from ..matcher import filter_sentences
from ..unique import unique
from .models import (
    Affiliation,
    Author,
    Bookmark,
    BookmarkTitle,
    Element,
    Meta,
    MetaType,
    PublicationMetadata,
    Text,
    Title,
)
from .titles_of_interest import titles_of_interest

THIS_FOLDER = Path(os.path.dirname(os.path.abspath(__file__)))


class PublicationTEI:
    # remove template sentenaces, such as copyright notices
    agressive_cleaning_enabled = True

    def __init__(self, tei: str):
        self._document_order_counter = 0

        if tei:
            self.soup = BeautifulSoup(tei, "xml")
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

    @cached_property
    def bookmarks(self) -> List[Bookmark]:
        candidates: List[Bookmark] = [
            *self._find_matching_meta("Abstract", "abstract_start")[0],
            *self._find_matching_title("Abstract"),
            *self._find_matching_title("Author contribution"),
            *self._find_matching_meta("Acknowledgement", "acknowledgements_start")[0],
            *self._find_matching_title("Acknowledgement"),
            *self._find_matching_title("Conflict of interest"),
        ]

        _, start = self._find_matching_meta(None, "abstract_end")

        candidates += [
            *self._find_matching_title("Background", start),
            *self._find_matching_title("Methods", start),
            *self._find_matching_title("Results", start),
            *self._find_matching_title("Discussion", start),
            *self._find_matching_title("Introduction", start),
            *self._find_matching_title("Conclusion", start),
            *self._find_matching_title("Outlook", start),
            *self._find_matching_meta("Annex", "annex_start", start)[0],
        ]

        candidates = sorted(candidates, key=lambda c: c.document_order)
        candidates = unique(candidates, key=lambda c: c.document_order)
        candidates = unique(candidates, key=lambda c: c.title)

        return candidates

    @cached_property
    def abstract_sentences(self) -> List[Text]:
        try:
            abstract_start = next(
                i
                for i, m in enumerate(self.content)
                if isinstance(m, Meta) and m.meta_type == "abstract_start"
            )
            abstract_end = next(
                i
                for i, m in enumerate(self.content)
                if isinstance(m, Meta) and m.meta_type == "abstract_end"
            )
            return [
                s
                for p in self.content[abstract_start:abstract_end]
                if isinstance(p, Paragraph)
                for s in p.sentences
            ]
        except StopIteration:
            pass  # let's try another way

        try:
            abstract_start = next(
                m.document_order for m in self.bookmarks if m.title == "Abstract"
            )
            abstract_sentences: List[Text] = []
            for c in self.content:
                if isinstance(c, Paragraph):
                    abstract_sentences.extend(
                        s for s in c.sentences if s.document_order > abstract_start
                    )
                elif len(abstract_sentences) >= 5:
                    break
            return abstract_sentences
        except StopIteration:
            pass  # let's try another way

        return self.sentences[:10]

    @cached_property
    def introduction_sentences(self) -> List[Text]:
        """Includes abstract"""
        introduction_end = 4

        try:
            introduction_start = [
                m.document_order for m in self.bookmarks if m.title == "Introduction"
            ][-1]

            for m in self.bookmarks:
                if m.title != "Introduction" and m.document_order > introduction_start:
                    introduction_end = m.document_order
                    break
        except IndexError:
            pass

        try:
            introduction_end = max(
                next(
                    i
                    for i, m in enumerate(self.content)
                    if isinstance(m, Meta) and m.meta_type == "abstract_end"
                ),
                introduction_end,
            )
        except StopIteration:
            pass

        introduction_sentences: List[Text] = []
        for c in self.content:
            if isinstance(c, Paragraph):
                introduction_sentences.extend(
                    s for s in c.sentences if s.document_order < introduction_end
                )

        return introduction_sentences

    @cached_property
    def conclusion_sentences(self) -> List[Text]:
        try:
            conclusion_start = next(
                m.document_order for m in self.bookmarks if m.title == "Conclusion"
            )
            conclusion_sentences: List[Text] = []
            for c in self.content:
                if isinstance(c, Paragraph):
                    conclusion_sentences.extend(
                        s for s in c.sentences if s.document_order > conclusion_start
                    )
                elif len(conclusion_sentences) >= 8:
                    break
            return conclusion_sentences
        except StopIteration:
            return self.sentences[-10:]

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
            elif not r.find_parents(
                ["abstract", "div", "figure"]
            ):  # figures are omitted as well
                results.extend(self._get_primitives(r))

        return results

    def _get_primitives(self, raw: Tag) -> List[Element]:
        results: List[Element] = []

        for r in raw.find_all(["head", "p"]):
            if r.name == "head" and r.get("coords") and r.get_text():
                text = self._parse_text(r)
                if text:
                    results.append(Title(text=text))
            elif r.name == "p" and r.find_all("s"):
                results.append(
                    Paragraph(
                        sentences=[
                            t
                            for t in [
                                self._parse_text(sentence, ignore_partial=True)
                                for sentence in r.find_all("s")
                                if sentence.get_text()
                            ]
                            if t
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

    def _parse_text(self, raw: Tag, ignore_partial: bool = False) -> Optional[Text]:
        text = raw.get_text()
        if text is None:
            return None

        if self.agressive_cleaning_enabled:
            filtered = filter_sentences(
                text,
                THIS_FOLDER / "templates.yaml",
                inverse=True,
                ignore_partial=ignore_partial,
            )
            text = " ".join(filtered)

        if not text.strip():
            return None

        return Text(
            content=text,
            document_order=self._generate_document_order_id(),
            coordinates=raw.get("coords"),
        )

    def _generate_document_order_id(self) -> int:
        value = self._document_order_counter
        self._document_order_counter += 1
        return value

    def _find_matching_meta(
        self,
        bookmark_title: Optional[BookmarkTitle],
        meta_type: MetaType,
        start: int = 0,
    ) -> Tuple[List[Bookmark], int]:
        for i, e in enumerate(self.content[start:], start=start):
            if not isinstance(e, Meta):
                continue

            if e.meta_type == meta_type:
                for e_next in self.content[i + 1 :]:
                    if isinstance(e_next, Title):
                        return [
                            Bookmark(
                                title=bookmark_title,
                                original_title=e_next.text.content,
                                document_order=e_next.text.document_order,
                                coordinates=e_next.text.coordinates,
                            )
                        ] if bookmark_title else [], i
                    if isinstance(e_next, Paragraph) and e_next.sentences:
                        return [
                            Bookmark(
                                title=bookmark_title,
                                original_title="",
                                document_order=e_next.sentences[0].document_order,
                                coordinates=e_next.sentences[0].coordinates,
                            )
                        ] if bookmark_title else [], i

        return [], 0

    def _find_matching_title(
        self,
        bookmark_title: BookmarkTitle,
        start: int = 0,
    ) -> List[Bookmark]:
        return [
            Bookmark(
                title=bookmark_title,
                original_title=e.text.content,
                document_order=e.text.document_order,
                coordinates=e.text.coordinates,
            )
            for e in self.content[start:]
            if isinstance(e, Title)
            and self._match_title(e.text.content, titles_of_interest[bookmark_title])
        ]

    @staticmethod
    def _match_title(title: str, keywords: Tuple[Union[Pattern, str], ...]) -> bool:
        title = PublicationTEI._process_section_title(title)

        if any(
            PublicationTEI._process_section_title(k) in title
            for k in keywords
            if isinstance(k, str)
        ):
            return True

        return any(k.match(title) for k in keywords if isinstance(k, Pattern))

    @staticmethod
    @lru_cache(maxsize=2000)
    def _process_section_title(title: str) -> str:
        title = re.sub(r"^\s*[ivx]+[.,)]? ", "", title)  # Remove leading Roman-numerals
        title = clean(title, convert_to_ascii=True)
        title = re.sub(
            r"[^a-zA-Z ]", "", title
        )  # Remove everything but letters and spaces (hypens are also removed)
        title_tokens = lemmatize_text(title)
        title = " ".join(t for t in title_tokens if t.strip())
        return title
