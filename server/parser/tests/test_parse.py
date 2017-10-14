# -*- coding: utf-8 -*-
import os
import parser
import datetime
import pytest
import logging

logging.getLogger().level = logging.INFO


CUR_DIR = os.path.dirname(__file__)
CONTENT_PATH = os.path.join(CUR_DIR, 'content')


def _path(*args):
    return os.path.join(CONTENT_PATH, *args)


class TestMdReader():

    def test_article_with_metadata(self):
        article = parser.parse(
            _path('article_with_md_extension.md'))
        expected = {
            'category': 'test',
            'title': 'Test md File',
            'abstract': '<p>I have a lot to test</p>',
            'date': datetime.datetime(2010, 12, 2, 10, 14),
            'image': None,
            'tags': {'foo', 'bar', 'foobar'}
        }
        assert article.title == expected['title']
        assert article.abstract == expected['abstract']
        assert article.date == expected['date']
        assert article.image == expected['image']
        assert article.tags == expected['tags']

        article = parser.parse(
            _path('article_with_markdown_and_nonascii_summary.md'))
        expected = {
            'title': 'マックOS X 10.8でパイソンとVirtualenvをインストールと設定',
            'abstract': '<p>パイソンとVirtualenvをまっくでインストールする方法について明確に説明します。</p>',
            'date': datetime.datetime(2012, 12, 20),
            'tags': {'パイソン', 'マック'},
            'slug': 'python-virtualenv-on-mac-osx-mountain-lion-10.8',
        }
        assert article.title == expected['title']
        assert article.abstract == expected['abstract']
        assert article.tags == expected['tags']

    def test_article_with_markdown_markup_extension(self):
        # test to ensure the markdown markup extension is being processed as
        # expected
        article = parser.parse(
            _path('article_with_markdown_markup_extensions.md'))

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

        assert article.html == expected

    def test_duplicate_tags_or_authors_are_removed(self):
        article = parser.parse(
            _path('article_with_duplicate_tags_authors.md'))
        assert article.tags == {'foo', 'bar', 'foobar'}

    def test_empty_file(self):
        article = parser.parse(_path('empty.md'))

        assert article.title is None
        assert article.html == ''
