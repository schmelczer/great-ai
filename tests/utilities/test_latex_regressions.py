from pathlib import Path

import pytest
from great_ai.utilities.external.pylatexenc.latex2text import LatexNodes2Text
from great_ai.utilities.external.pylatexenc.latexwalker import LatexWalkerParseError


def test_strict_input_checks_path_ancestry(tmp_path: Path) -> None:
    allowed = tmp_path / "allowed"
    sibling = tmp_path / "allowed_neighbor"
    allowed.mkdir()
    sibling.mkdir()
    (allowed / "inside.tex").write_text("inside")
    (sibling / "outside.tex").write_text("outside")
    (allowed / "link.tex").symlink_to(sibling / "outside.tex")
    converter = LatexNodes2Text()
    converter.set_tex_input_directory(str(allowed), strict_input=True)
    assert converter.latex_to_text(r"\input{inside}") == "inside"
    assert converter.latex_to_text(r"\input{../allowed_neighbor/outside}") == ""
    assert converter.latex_to_text(r"\input{link}") == ""


@pytest.mark.parametrize("text", [r"\verb", "\\verb   "])
def test_missing_verbatim_arguments_use_normal_parse_errors(text: str) -> None:
    converter = LatexNodes2Text()
    with pytest.raises(LatexWalkerParseError):
        converter.latex_to_text(text, tolerant_parsing=False)
    assert converter.latex_to_text(text, tolerant_parsing=True) == ""


def test_empty_matrix_has_a_text_representation() -> None:
    assert LatexNodes2Text().latex_to_text(r"\begin{pmatrix}\end{pmatrix}") == "[  ]"
