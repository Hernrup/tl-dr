from markdown import Markdown
import dateutil.parser
import itertools


def _md_factory():
    md = Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.meta',
        'markdown.extensions.toc'
    ])
    return md


def _parse_metadata(metadata):
    """Return the dict containing document metadata"""
    MULTI_ITEM_KEYS = ['tags']
    HTML_ITEM_KEYS = ['abstract']
    DATE_KEYS = ['date']

    for k, v in metadata.items():
        if k not in MULTI_ITEM_KEYS:
            metadata[k] = _metadata_to_single_value(metadata[k])
        else:
            metadata[k] = _metadata_to_list(metadata[k])

        if k in HTML_ITEM_KEYS:
            metadata[k] = _metadata_to_html(metadata[k])

        if k in DATE_KEYS:
            metadata[k] = _metadata_to_datetime(metadata[k])

    return metadata


def _metadata_to_single_value(value):
    if len(value) > 1:
        raise ValueError('multiple values found where one expected')
    return value[0]


def _metadata_to_html(value):
    return _md_factory().convert(value)


def _metadata_to_list(value):
    # flatten
    l = list(itertools.chain(*[v.split(',') for v in value]))
    # strip
    l = [v.strip() for v in l]
    # uniqueify
    l = set(l)
    return l


def _metadata_to_datetime(value):
    return dateutil.parser.parse(value)


def parse(source_path):
    """Parse content and metadata of markdown files"""
    md = _md_factory()

    with open(source_path) as f:
        data = f.read()
        content = md.convert(data)

    try:
        metadata = _parse_metadata(md.Meta)
    except AttributeError:
        metadata = {}

    return Article(
        title=metadata.get('title'),
        abstract=metadata.get('abstract'),
        date=metadata.get('date'),
        tags=metadata.get('tags'),
        image=metadata.get('image'),
        md=data,
        html=content
    )


class Article():

    def __init__(self, title, abstract, date, tags, image, md, html):
        self.title = title
        self.abstract = abstract
        self.date = date
        self.tags = tags
        self.image = image
        self.md = md
        self.html = html
