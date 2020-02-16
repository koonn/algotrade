# -*- coding: utf-8 -*-

from .context import algotrade

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(algotrade.read_fx())


if __name__ == '__main__':
    unittest.main()
