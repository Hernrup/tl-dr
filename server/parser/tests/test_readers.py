# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import os

import six

from parser import readers

from unittest.mock import patch
import unittest
from parser import DEFAULT_CONFIG
from datetime import Datetime

CUR_DIR = os.path.dirname(__file__)
CONTENT_PATH = os.path.join(CUR_DIR, 'content')


def _path(*args):
    return os.path.join(CONTENT_PATH, *args)


def get_settings(**kwargs):
    """Provide tweaked setting dictionaries for testing
    Set keyword arguments to override specific settings.
    """
    settings = DEFAULT_CONFIG.copy()
    for key, value in kwargs.items():
        settings[key] = value
    return settings


class ReaderTest(unittest.TestCase):

    def read_file(self, path, **kwargs):
        # Isolate from future API changes to readers.read_file
        r = readers.Readers(settings=get_settings(**kwargs))
        return r.read_file(base_path=CONTENT_PATH, path=path)

    def assertDictHasSubset(self, dictionary, subset):
        for key, value in subset.items():
            if key in dictionary:
                real_value = dictionary.get(key)
                self.assertEqual(
                    value,
                    real_value,
                    'Expected %s to have value %s, but was %s' %
                    (key, value, real_value))
            else:
                self.fail(
                    'Expected %s to have value %s, but was not in Dict' %
                    (key, value))


class TestAssertDictHasSubset(ReaderTest):
    def setUp(self):
        self.dictionary = {
            'key-a': 'val-a',
            'key-b': 'val-b'
        }

    def tearDown(self):
        self.dictionary = None

    def test_subset(self):
        self.assertDictHasSubset(self.dictionary, {'key-a': 'val-a'})

    def test_equal(self):
        self.assertDictHasSubset(self.dictionary, self.dictionary)

    def test_fail_not_set(self):
        six.assertRaisesRegex(
            self,
            AssertionError,
            r'Expected.*key-c.*to have value.*val-c.*but was not in Dict',
            self.assertDictHasSubset,
            self.dictionary,
            {'key-c': 'val-c'})

    def test_fail_wrong_val(self):
        six.assertRaisesRegex(
            self,
            AssertionError,
            r'Expected .*key-a.* to have value .*val-b.* but was .*val-a.*',
            self.assertDictHasSubset,
            self.dictionary,
            {'key-a': 'val-b'})


class DefaultReaderTest(ReaderTest):

    def test_readfile_unknown_extension(self):
        with self.assertRaises(TypeError):
            self.read_file(path='article_with_metadata.unknownextension')

    @unittest.skipUnless(patch, 'Needs Mock module')
    def test_find_empty_alt(self):
        with patch('pelican.readers.logger') as log_mock:
            content = ['<img alt="" src="test-image.png" width="300px" />',
                       '<img src="test-image.png"  width="300px" alt="" />']

            for tag in content:
                readers.find_empty_alt(tag, '/test/path')
                log_mock.warning.assert_called_with(
                    u'Empty alt attribute for image %s in %s',
                    u'test-image.png',
                    u'/test/path',
                    extra={'limit_msg':
                           'Other images have empty alt attributes'}
                )


class MdReaderTest(ReaderTest):

    def test_article_with_metadata(self):
        reader = readers.MarkdownReader(settings=get_settings())
        content, metadata = reader.read(
            _path('article_with_md_extension.md'))
        expected = {
            'category': 'test',
            'title': 'Test md File',
            'summary': '<p>I have a lot to test</p>',
            'date': Datetime(2010, 12, 2, 10, 14),
            'modified': Datetime(2010, 12, 2, 10, 20),
            'tags': ['foo', 'bar', 'foobar'],
        }
        self.assertDictHasSubset(metadata, expected)

        content, metadata = reader.read(
            _path('article_with_markdown_and_nonascii_summary.md'))
        expected = {
            'title': 'マックOS X 10.8でパイソンとVirtualenvをインストールと設定',
            'summary': '<p>パイソンとVirtualenvをまっくでインストールする方法について明確に説明します。</p>',
            'category': '指導書',
            'date': Datetime(2012, 12, 20),
            'modified': Datetime(2012, 12, 22),
            'tags': ['パイソン', 'マック'],
            'slug': 'python-virtualenv-on-mac-osx-mountain-lion-10.8',
        }
        self.assertDictHasSubset(metadata, expected)

    def test_article_with_footnote(self):
        reader = readers.MarkdownReader(settings=get_settings())
        content, metadata = reader.read(
            _path('article_with_markdown_and_footnote.md'))
        expected_content = (
            '<p>This is some content'
            '<sup id="fnref-1"><a class="footnote-ref" href="#fn-1"'
            '>1</a></sup>'
            ' with some footnotes'
            '<sup id="fnref-footnote"><a class="footnote-ref" '
            'href="#fn-footnote">2</a></sup></p>\n'

            '<div class="footnote">\n'
            '<hr>\n<ol>\n<li id="fn-1">\n'
            '<p>Numbered footnote&#160;'
            '<a class="footnote-backref" href="#fnref-1" '
            'title="Jump back to footnote 1 in the text">&#8617;</a></p>\n'
            '</li>\n<li id="fn-footnote">\n'
            '<p>Named footnote&#160;'
            '<a class="footnote-backref" href="#fnref-footnote"'
            ' title="Jump back to footnote 2 in the text">&#8617;</a></p>\n'
            '</li>\n</ol>\n</div>')
        expected_metadata = {
            'title': 'Article with markdown containing footnotes',
            'summary': (
                '<p>Summary with <strong>inline</strong> markup '
                '<em>should</em> be supported.</p>'),
            'date': Datetime(2012, 10, 31),
            'modified': Datetime(2012, 11, 1),
            'multiline': [
                'Line Metadata should be handle properly.',
                'See syntax of Meta-Data extension of '
                'Python Markdown package:',
                'If a line is indented by 4 or more spaces,',
                'that line is assumed to be an additional line of the value',
                'for the previous keyword.',
                'A keyword may have as many lines as desired.',
            ]
        }
        self.assertEqual(content, expected_content)
        self.assertDictHasSubset(metadata, expected_metadata)

    def test_article_with_file_extensions(self):
        reader = readers.MarkdownReader(settings=get_settings())
        # test to ensure the md file extension is being processed by the
        # correct reader
        content, metadata = reader.read(
            _path('article_with_md_extension.md'))
        expected = (
            "<h1>Test Markdown File Header</h1>\n"
            "<h2>Used for pelican test</h2>\n"
            "<p>The quick brown fox jumped over the lazy dog's back.</p>")
        self.assertEqual(content, expected)
        # test to ensure the mkd file extension is being processed by the
        # correct reader
        content, metadata = reader.read(
            _path('article_with_mkd_extension.mkd'))
        expected = ("<h1>Test Markdown File Header</h1>\n<h2>Used for pelican"
                    " test</h2>\n<p>This is another markdown test file.  Uses"
                    " the mkd extension.</p>")
        self.assertEqual(content, expected)
        # test to ensure the markdown file extension is being processed by the
        # correct reader
        content, metadata = reader.read(
            _path('article_with_markdown_extension.markdown'))
        expected = ("<h1>Test Markdown File Header</h1>\n<h2>Used for pelican"
                    " test</h2>\n<p>This is another markdown test file.  Uses"
                    " the markdown extension.</p>")
        self.assertEqual(content, expected)
        # test to ensure the mdown file extension is being processed by the
        # correct reader
        content, metadata = reader.read(
            _path('article_with_mdown_extension.mdown'))
        expected = ("<h1>Test Markdown File Header</h1>\n<h2>Used for pelican"
                    " test</h2>\n<p>This is another markdown test file.  Uses"
                    " the mdown extension.</p>")
        self.assertEqual(content, expected)

    def test_article_with_markdown_markup_extension(self):
        # test to ensure the markdown markup extension is being processed as
        # expected
        page = self.read_file(
            path='article_with_markdown_markup_extensions.md',
            MARKDOWN={
                'extension_configs': {
                    'markdown.extensions.toc': {},
                    'markdown.extensions.codehilite': {},
                    'markdown.extensions.extra': {}
                }
            }
        )
        expected = ('<div class="toc">\n'
                    '<ul>\n'
                    '<li><a href="#level1">Level1</a><ul>\n'
                    '<li><a href="#level2">Level2</a></li>\n'
                    '</ul>\n'
                    '</li>\n'
                    '</ul>\n'
                    '</div>\n'
                    '<h2 id="level1">Level1</h2>\n'
                    '<h3 id="level2">Level2</h3>')

        self.assertEqual(page.content, expected)

    def test_article_with_filename_metadata(self):
        page = self.read_file(
            path='2012-11-30_md_w_filename_meta#foo-bar.md',
            FILENAME_METADATA=None)
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
        }
        self.assertDictHasSubset(page.metadata, expected)

        page = self.read_file(
            path='2012-11-30_md_w_filename_meta#foo-bar.md',
            FILENAME_METADATA=r'(?P<date>\d{4}-\d{2}-\d{2}).*')
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
            'date': Datetime(2012, 11, 30),
        }
        self.assertDictHasSubset(page.metadata, expected)

        page = self.read_file(
            path='2012-11-30_md_w_filename_meta#foo-bar.md',
            FILENAME_METADATA=(
                r'(?P<date>\d{4}-\d{2}-\d{2})'
                r'_(?P<Slug>.*)'
                r'#(?P<MyMeta>.*)-(?P<author>.*)'))
        expected = {
            'category': 'yeah',
            'author': 'Alexis Métaireau',
            'date': Datetime(2012, 11, 30),
            'slug': 'md_w_filename_meta',
            'mymeta': 'foo',
        }
        self.assertDictHasSubset(page.metadata, expected)

    def test_article_with_optional_filename_metadata(self):
        page = self.read_file(
            path='2012-11-30_md_w_filename_meta#foo-bar.md',
            FILENAME_METADATA=r'(?P<date>\d{4}-\d{2}-\d{2})?')
        expected = {
            'date': Datetime(2012, 11, 30),
            'reader': 'markdown',
        }
        self.assertDictHasSubset(page.metadata, expected)

        page = self.read_file(
            path='empty.md',
            FILENAME_METADATA=r'(?P<date>\d{4}-\d{2}-\d{2})?')
        expected = {
            'reader': 'markdown',
        }
        self.assertDictHasSubset(page.metadata, expected)
        self.assertNotIn('date', page.metadata, 'Date should not be set.')

    def test_duplicate_tags_or_authors_are_removed(self):
        reader = readers.MarkdownReader(settings=get_settings())
        content, metadata = reader.read(
            _path('article_with_duplicate_tags_authors.md'))
        expected = {
            'tags': ['foo', 'bar', 'foobar'],
            'authors': ['Author, First', 'Author, Second'],
        }
        self.assertDictHasSubset(metadata, expected)

    def test_empty_file(self):
        reader = readers.MarkdownReader(settings=get_settings())
        content, metadata = reader.read(
            _path('empty.md'))

        self.assertEqual(metadata, {})
        self.assertEqual(content, '')

    def test_empty_file_with_bom(self):
        reader = readers.MarkdownReader(settings=get_settings())
        content, metadata = reader.read(
            _path('empty_with_bom.md'))

        self.assertEqual(metadata, {})
        self.assertEqual(content, '')
