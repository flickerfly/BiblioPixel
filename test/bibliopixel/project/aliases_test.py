import unittest
import test.bibliopixel.patch
from bibliopixel.project import aliases, alias_lists, importer


def patch(**kwds):
    return test.bibliopixel.patch.patch(alias_lists, 'PROJECT_ALIASES', kwds)


class AliasTest(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(aliases.resolve(''), '')

    def test_resolve(self):
        self.assertEqual(
            aliases.resolve('off'), 'bibliopixel.animation.off.OffAnim')
        self.assertEquals(aliases.resolve('foo'), 'foo')

        with patch(foo='bar'):
            self.assertEquals(aliases.resolve('foo'), 'bar')
            self.assertEquals(aliases.resolve('@foo.bing'), 'bar.bing')
            self.assertEquals(aliases.resolve('bar.bing.@foo'), 'bar.bing.bar')
            self.assertEquals(aliases.resolve('x@foo'), 'x@foo')

    def test_preserve_separators(self):
        s = '.asdfa./#fahdwrdr./#435'
        self.assertEqual(aliases.resolve(s), s)

    def test_marker(self):
        with patch(foo='bar.com/a.html'):
            result = aliases.resolve('https://@foo#tag')

        self.assertEqual(result, 'https://bar.com/a.html#tag')

    def test_existence(self):
        failed = []
        for cl in alias_lists.BUILTIN_ALIASES.values():
            try:
                importer.import_symbol(cl)
            except:
                failed.append(cl)

        if failed:
            print('Failed', *failed, sep='\n')
        self.assertFalse(failed)

    def test_additional_aliases(self):
        additional = {'foo': 'bar', 'remote': 'distance'}
        self.assertEqual(aliases.resolve('foo', additional), 'bar')
        self.assertEqual(aliases.resolve('remote', additional), 'distance')

    def test_not_needed(self):
        just_one = ''
        failed, not_equal = [], []

        for alias, path in alias_lists.BUILTIN_ALIASES.items():
            if just_one and alias != just_one:
                continue
            python_path = '.'.join(path.split('.', 2)[:2])
            expected = importer.import_symbol(path)
            try:
                actual = importer.import_symbol(alias, python_path=python_path)
            except:
                failed.append(alias)
                if just_one:
                    raise
            else:
                if actual is not expected:
                    not_equal.append(alias)

        self.assertEquals([sorted(failed), sorted(not_equal)],
                          [sorted(FAILED), sorted(NOT_EQUAL)])


# Aliases that would fail to load at all if they were removed
FAILED = (
    'apa102', 'dummy', 'lpd8806', 'matrix_calibration', 'matrix_test',
    'mirror', 'off', 'pi_ws281x', 'receiver', 'remote', 'simpixel',
    'sk9822', 'spi', 'strip_test', 'ws2801', 'ws281x')

# Aliases that load and get the wrong value
NOT_EQUAL = 'matrix', 'reprocess', 'serial'
