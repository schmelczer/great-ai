from pathlib import Path

from great_ai.utilities.external.pylatexenc.latex2text import LatexNodes2Text


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
