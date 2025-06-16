"""Unit tests for message splitting utilities in bot.py."""

import ast
import types
from pathlib import Path
import unittest


def _load_bot_functions():
    """Dynamically load split helpers from bot.py without executing it."""
    bot_path = Path(__file__).resolve().parents[1] / "bot.py"
    source = bot_path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    module = types.ModuleType("bot_funcs")

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in (
            "split_frame_message_into_array",
            "split_cf_message_into_array",
        ):
            code = compile(ast.Module([node], type_ignores=[]), filename="bot.py", mode="exec")
            exec(code, module.__dict__)

    return module.split_frame_message_into_array, module.split_cf_message_into_array


class SplitMessageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        frame_func, cf_func = _load_bot_functions()
        cls.split_frame = staticmethod(frame_func)
        cls.split_cf = staticmethod(cf_func)

    def test_split_frame_valid(self):
        msg = "[{Hello},{World}]"
        self.assertEqual(self.split_frame(msg), ["Hello", "World"])

    def test_split_frame_invalid_returns_original(self):
        msg = "Invalid message"
        self.assertEqual(self.split_frame(msg), [msg])

    def test_split_cf_valid(self):
        msg = "[{Foo}, {Bar}]"
        self.assertEqual(self.split_cf(msg), ["Foo", "Bar"])

    def test_split_cf_invalid_returns_original(self):
        msg = "[Foo, Bar]"  # missing curly braces
        self.assertEqual(self.split_cf(msg), [msg])

    def test_nested_braces(self):
        msg = "[{{A}}, {B}]"
        self.assertEqual(self.split_frame(msg), ["{A}", "B"])


if __name__ == "__main__":
    unittest.main()

