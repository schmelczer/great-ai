import unittest

from src.great_ai.utilities import match_names


class TestMatchNames(unittest.TestCase):
    def test_grid(self) -> None:
        names = [
            ["Al-Nasiry, S.", "Al-Nasiry S"],
            ["De Leo, A. (Andreina)"],
            [
                "DeBenedictis, J.N. (Julia)",
                "DeBenedictis, N. (Julia)",
                "DeBenedictis, J.",
                "Julia DeBenedictis",
            ],
            ["Diesen, J.A.Y. van"],
            ["Nio, C Yung"],
            ["Uyen Chau Nguyen"],
            ["Hagger M.S.", "Martin Hagger"],
            ["Izabela-Cristina STANCU"],
            ["Verborgh R.", "Ruben Verborgh"],
            ["Droshout, D.T.G.G.M.L. (Dimitri)"],
            ["El Demellawy"],
            ["Sebastiaan van de Velde", "van de Velde, Sebastiaan"],
            ["Sebastiaan Brand"],
            ["Bertil FM Blok", "B.F.M. Blok"],
            ["Bob Zadok Blok"],
            ["Shannon Spruit"],
            ["Shannon Kroes"],
            [
                "MSc Jérémie Decouchant",
                "PhD, Jérémie Decouchant",
                "PhD Jérémie Decouchant",
                "Jérémie Decouchant",
                "MD, PhD Jérémie Decouchant",
            ],
            ["Jeremie Gobeil"],
            ["Wouters, B.B.R.E.F.", "Wouters B.B. R.  E.F."],
            ["Elias Caldeira Dantas, A.M. (Aline)"],
            ["Ed Harris"],
            ["Ed Deprettere ", "    Ed   Deprettere "],
            ["András Schmelczer"],
            ["Enden, G. van den (Gitta)"],
            ["Ruben van Dijk"],
            ["Richard van Dijk"],
            ["Xinping Guan", "X. Guan"],
            ["Xiaohong Guan", "X. Guan"],
            ["Pruimboom, Tim", "Pruimboom T."],
            ["Sanchez-Faddeev H.", "Sanchez-Faddeev, Hernando"],
            ["Duijnhoven - Jansen, E.M. van", "Emma M. van Jansen"],
        ]

        all_names = [n for t in names for n in t]

        for n1 in all_names:
            for n2 in all_names:
                is_match = match_names(n1, n2)
                groups = [t for t in names if n1 in t]
                with self.subTest(n1=n1, n2=n2):
                    if any(n2 in g for g in groups):
                        self.assertTrue(is_match, "false negative")
                    elif all(n2 not in g for g in groups):
                        self.assertFalse(is_match, "false match")

    def test_empty(self) -> None:
        self.assertFalse(match_names("", ""))
        self.assertFalse(match_names(None, ""))
        self.assertFalse(match_names(None, None))
        self.assertFalse(match_names("", None))
        self.assertFalse(match_names("Oliver", None))
