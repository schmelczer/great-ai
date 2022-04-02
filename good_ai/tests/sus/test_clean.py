import unittest

from src.sus.clean import clean


class TestClean(unittest.TestCase):
    def test_xml_handling(self) -> None:
        xml = '<strong>Hi, </strong> my name<br/>is <span style="color: hotpink;"> András</span>! &lt;&#51; <> < ></><> &lt;&gt; <|'
        clean_xml = "Hi, my name is András! <3 <> <|"
        clean_xml_ascii = "Hi, my name is Andras! <3 <> <|"

        self.assertEqual(clean(xml), clean_xml)
        self.assertEqual(clean(xml, ignore_xml=True, ignore_latex=True), xml)
        self.assertEqual(clean(xml, convert_to_ascii=True), clean_xml_ascii)

    def test_simple_latex_handling(self) -> None:
        latex = 'Bj\\"{o}rn is \\textit{happy} 🙂'
        clean_latex = "Björn is happy 🙂"
        clean_latex_ascii = "Bjorn is happy"

        self.assertEqual(clean(latex), clean_latex)
        self.assertEqual(clean(latex, ignore_latex=True), latex)
        self.assertEqual(clean(latex, convert_to_ascii=True), clean_latex_ascii)

    def test_cursed(self) -> None:
        cursed = """
        t̴̨̢̝̻͚͓͉̀̄̃́͜o̸͉̰̼͖͖̅̀̓̿̇̚͝ ̶̢͕̄͊̾͑̂̀̉͑ṱ̸̨̛͈̣̠̤͍̰̂̅͋̀́h̸̹̐͗̅̉͐͂͝e̶̜̳̞̍͘ ̴̟̗̻̤̤̮̒̂̋̓́͐͘͜m̵̺̫̥̙̣̥͐̌͜o̴̖͙̙̎̒͂o̷̬̤͑̆̂̉̊̂n̸̥͒̊
        """
        cleaned = "to the moon"

        self.assertEqual(clean(cursed), cursed.strip())
        self.assertEqual(clean(cursed, convert_to_ascii=True), cleaned)

    def test_whitespace(self) -> None:
        text = """
        
        word1

          word2 \n\n\n\t
        wo\t\f rd3


        """  # noqa: W293
        cleaned = "word1 word2 wo rd3"

        self.assertEqual(clean(text, convert_to_ascii=True), cleaned)
        self.assertEqual(clean(text, ignore_xml=True, ignore_latex=True), cleaned)
        self.assertEqual(clean(text), cleaned)

    def test_hyphens(self) -> None:
        text = """
            break - word
            break- word
            break -word
            break    -word
            break-\tword
        """
        cleaned = "break - word break-word break-word break-word break-word"

        self.assertEqual(clean(text), cleaned)

    def test_bracket_removal(self) -> None:
        text = "something [0], and [frefe, ferf]"
        cleaned = "something, and"

        self.assertEqual(clean(text, remove_brackets=True), cleaned)
        self.assertEqual(
            clean(text, ignore_xml=True, ignore_latex=True, remove_brackets=True),
            cleaned,
        )
        self.assertEqual(
            clean(text, convert_to_ascii=True, remove_brackets=True), cleaned
        )
        self.assertEqual(clean(text), text)

    def test_latex_math_handling(self) -> None:
        latex = "An increase of 3% was achieved with $q_1 = \\frac{3}{5}$."
        bad_latex = "An increase of 3% was achieved with $q_1 = \\frac{3}/5$."
        clean_latex = "An increase of 3% was achieved with q_1 = 3/5."
        clean_bad_latex = "An increase of 3% was achieved with q_1 = 3//5."

        self.assertEqual(clean(latex), clean_latex)
        self.assertEqual(clean(bad_latex), clean_bad_latex)
        self.assertEqual(clean(latex, ignore_latex=True), latex)
        self.assertEqual(clean(bad_latex, ignore_latex=True), bad_latex)

    def test_everything(self) -> None:
        text = """
         Hi % 3 &gt;2   <h2 color="red">my paper</h2> there! cost- effective cost - effective cost -effective \\frac{1/2} hi \\frac{1}{2} \\textit{italic} \\`acc\\^ented text 北亰 ﬁ æ Ĳ ĳ ﬀ András öô 2132 rgrv \n\\ &nbsp; fd [32] [Bei et al., 2003]\n  🤡 🙄 😶‍🌫️ 🇲🇲
        """
        cleaned = "Hi% 3 >2 my paper there! cost-effective cost - effective cost-effective 1/2/hi 1/2 italic accented text Bei Jing fi ae IJ ij ff Andras oo 2132 rgrv fd"

        self.assertEqual(
            clean(text, convert_to_ascii=True, remove_brackets=True), cleaned
        )

    def test_empty(self) -> None:
        self.assertEqual(clean("", convert_to_ascii=True), "")

    def test_punctuation_fixing(self) -> None:
        text = " Dear reader ( or  listener ) , welcome ! "
        fixed = "Dear reader (or listener), welcome!"
        self.assertEqual(clean(text), fixed)
