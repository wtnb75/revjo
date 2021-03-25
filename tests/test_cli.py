import unittest
from click.testing import CliRunner
import json
import tempfile
from rjo._cli import cli
from rjo import VERSION


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_help(self):
        res = self.runner.invoke(cli, ["--help"])
        self.assertEqual(0, res.exit_code)
        self.assertIn(" --version ", res.output)
        self.assertIn(" --help ", res.output)
        self.assertIn(" convert", res.output)

    def test_version(self):
        res = self.runner.invoke(cli, ["--version"])
        self.assertEqual(0, res.exit_code)
        self.assertEqual("rjo, version {}".format(VERSION), res.output.strip())

    def test_invalid_help(self):
        res = self.runner.invoke(cli, ["invalid"])
        self.assertNotEqual(0, res.exit_code)
        self.assertIn("Error: No such command", res.output)

    def test_convert_help(self):
        res = self.runner.invoke(cli, ["convert", "--help"])
        self.assertEqual(0, res.exit_code)
        self.assertIn(" --verbose ", res.output)

    def test_convert_verbose(self):
        res = self.runner.invoke(cli, ["convert", "--verbose", json.dumps({"hello": "world"})])
        self.assertEqual(0, res.exit_code)
        self.assertIn("hello=world", res.output.strip())

    def test_convert(self):
        res = self.runner.invoke(cli, ["convert", json.dumps({"hello": "world"})])
        self.assertEqual(0, res.exit_code)
        self.assertIn("hello=world", res.output.strip())

    def test_convert_input(self):
        res = self.runner.invoke(cli, ["convert"], input=json.dumps({"hello": "world"}, indent=2))
        self.assertEqual(0, res.exit_code)
        self.assertIn("hello=world", res.output.strip())

    def test_convert_input_stdin(self):
        res = self.runner.invoke(cli, ["convert", "--input", "-"], input=json.dumps({"hello": "world"}, indent=2))
        self.assertEqual(0, res.exit_code)
        self.assertIn("hello=world", res.output.strip())

    def test_convert_input_file(self):
        with tempfile.NamedTemporaryFile("r+") as tf:
            json.dump({"hello": "world"}, fp=tf)
            tf.flush()
            res = self.runner.invoke(cli, ["convert", "--input", tf.name])
        self.assertEqual(0, res.exit_code)
        self.assertIn("hello=world", res.output.strip())
