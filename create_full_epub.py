#!/usr/bin/env python3
"""Create complete EPUB for Inadequate Equilibria with full text"""

import os
import zipfile
from datetime import datetime
import json
from bs4 import BeautifulSoup

# Book metadata
BOOK_TITLE = "Inadequate Equilibria"
BOOK_SUBTITLE = "Where and How Civilizations Get Stuck"
AUTHOR = "Eliezer Yudkowsky"
PUBLISHER = "Machine Intelligence Research Institute"
LANGUAGE = "en"
IDENTIFIER = "inadequate-equilibria-2017"
PUBLICATION_DATE = "2017"

def clean_html_content(html_content, chapter_title):
    """Clean and format HTML content"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove any remaining unwanted elements
    for tag in soup.find_all(['script', 'style', 'nav', 'aside', 'form', 'button']):
        tag.decompose()

    # Remove class and id attributes for cleaner output
    for tag in soup.find_all(True):
        tag.attrs = {key: value for key, value in tag.attrs.items()
                    if key not in ['class', 'id', 'style']}

    # Add chapter heading if not present
    h1 = soup.find('h1')
    if not h1 or chapter_title.lower() not in h1.get_text().lower():
        new_h1 = soup.new_tag('h1')
        new_h1.string = chapter_title
        if soup.body:
            soup.body.insert(0, new_h1)

    return str(soup)

def create_epub():
    """Create EPUB file with full content"""

    # Load the full chapters
    with open('full_chapters.json', 'r', encoding='utf-8') as f:
        chapters_data = json.load(f)

    # Create directories
    os.makedirs("epub_full/META-INF", exist_ok=True)
    os.makedirs("epub_full/OEBPS", exist_ok=True)

    # Create mimetype file
    with open("epub_full/mimetype", "w") as f:
        f.write("application/epub+zip")

    # Create container.xml
    container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>'''

    with open("epub_full/META-INF/container.xml", "w") as f:
        f.write(container_xml)

    # Create stylesheet
    css = '''body {
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.6;
    margin: 1.5em;
    color: #222;
}

h1 {
    font-size: 2em;
    margin-top: 1em;
    margin-bottom: 0.75em;
    font-weight: bold;
    line-height: 1.2;
}

h2 {
    font-size: 1.5em;
    margin-top: 1.2em;
    margin-bottom: 0.6em;
    font-weight: bold;
}

h3 {
    font-size: 1.2em;
    margin-top: 1em;
    margin-bottom: 0.5em;
    font-weight: bold;
}

p {
    margin: 0.75em 0;
    text-align: justify;
}

blockquote {
    margin: 1em 2em;
    font-style: italic;
    border-left: 3px solid #ccc;
    padding-left: 1em;
}

ul, ol {
    margin: 0.75em 0;
    padding-left: 2em;
}

li {
    margin: 0.5em 0;
}

strong {
    font-weight: bold;
}

em {
    font-style: italic;
}

a {
    color: #0066cc;
    text-decoration: underline;
}

hr {
    margin: 2em 0;
    border: none;
    border-top: 1px solid #ccc;
}

table {
    margin: 1em 0;
    border-collapse: collapse;
}

td, th {
    padding: 0.5em;
    border: 1px solid #ddd;
}'''

    with open("epub_full/OEBPS/stylesheet.css", "w") as f:
        f.write(css)

    # Create title page
    title_html = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{BOOK_TITLE}</title>
    <link rel="stylesheet" type="text/css" href="stylesheet.css"/>
</head>
<body>
    <div style="text-align: center; margin-top: 3em;">
        <h1 style="font-size: 2.5em; margin-bottom: 0.5em;">{BOOK_TITLE}</h1>
        <h2 style="font-weight: normal; font-style: italic;">{BOOK_SUBTITLE}</h2>
        <p style="margin-top: 3em; font-size: 1.3em;">by</p>
        <p style="font-size: 1.5em; font-weight: bold;">{AUTHOR}</p>
        <p style="margin-top: 4em;">{PUBLISHER}</p>
        <p>{PUBLICATION_DATE}</p>
        <p style="margin-top: 2em; font-size: 0.9em;">Licensed under CC NC-BY-SA 4.0</p>
    </div>
</body>
</html>'''

    with open("epub_full/OEBPS/title.xhtml", "w", encoding='utf-8') as f:
        f.write(title_html)

    # Create chapter files with full content
    chapter_info = []
    for chapter_num in sorted([int(k) for k in chapters_data.keys()]):
        chapter = chapters_data[str(chapter_num)]

        chapter_html = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Chapter {chapter_num}: {chapter['title']}</title>
    <link rel="stylesheet" type="text/css" href="stylesheet.css"/>
</head>
<body>
{chapter['content']}
</body>
</html>'''

        with open(f"epub_full/OEBPS/chapter{chapter_num}.xhtml", "w", encoding='utf-8') as f:
            f.write(chapter_html)

        chapter_info.append({
            'number': chapter_num,
            'title': chapter['title'],
            'word_count': chapter['word_count']
        })

    # Create content.opf
    manifest_items = ['<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>']
    manifest_items.append('<item id="css" href="stylesheet.css" media-type="text/css"/>')
    spine_items = ['<itemref idref="title"/>']

    for info in chapter_info:
        manifest_items.append(f'<item id="chapter{info["number"]}" href="chapter{info["number"]}.xhtml" media-type="application/xhtml+xml"/>')
        spine_items.append(f'<itemref idref="chapter{info["number"]}"/>')

    content_opf = f'''<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:title>{BOOK_TITLE}: {BOOK_SUBTITLE}</dc:title>
        <dc:creator>{AUTHOR}</dc:creator>
        <dc:language>{LANGUAGE}</dc:language>
        <dc:identifier id="bookid">{IDENTIFIER}</dc:identifier>
        <dc:publisher>{PUBLISHER}</dc:publisher>
        <dc:date>{PUBLICATION_DATE}</dc:date>
        <dc:rights>CC NC-BY-SA 4.0</dc:rights>
        <dc:description>A book about a generalized notion of efficient markets, and how we can use this notion to guess where society will or won't be effective at pursuing some widely desired goal.</dc:description>
        <meta property="dcterms:modified">{datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")}</meta>
    </metadata>
    <manifest>
        {chr(10).join('        ' + item for item in manifest_items)}
        <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    </manifest>
    <spine toc="ncx">
        {chr(10).join('        ' + item for item in spine_items)}
    </spine>
</package>'''

    with open("epub_full/OEBPS/content.opf", "w", encoding='utf-8') as f:
        f.write(content_opf)

    # Create toc.ncx
    nav_points = []
    for i, info in enumerate(chapter_info, 1):
        nav_points.append(f'''        <navPoint id="navPoint-{i+1}" playOrder="{i+1}">
            <navLabel>
                <text>Chapter {info['number']}: {info['title']}</text>
            </navLabel>
            <content src="chapter{info['number']}.xhtml"/>
        </navPoint>''')

    toc_ncx = f'''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta name="dtb:uid" content="{IDENTIFIER}"/>
        <meta name="dtb:depth" content="1"/>
        <meta name="dtb:totalPageCount" content="0"/>
        <meta name="dtb:maxPageNumber" content="0"/>
    </head>
    <docTitle>
        <text>{BOOK_TITLE}</text>
    </docTitle>
    <navMap>
        <navPoint id="navPoint-1" playOrder="1">
            <navLabel>
                <text>Title Page</text>
            </navLabel>
            <content src="title.xhtml"/>
        </navPoint>
{chr(10).join(nav_points)}
    </navMap>
</ncx>'''

    with open("epub_full/OEBPS/toc.ncx", "w", encoding='utf-8') as f:
        f.write(toc_ncx)

    # Create EPUB zip file
    epub_filename = "Inadequate_Equilibria_Eliezer_Yudkowsky.epub"

    with zipfile.ZipFile(epub_filename, 'w', zipfile.ZIP_DEFLATED) as epub:
        # mimetype must be first and uncompressed
        epub.write("epub_full/mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)

        # Add all other files
        for root, dirs, files in os.walk("epub_full"):
            for file in files:
                if file != "mimetype":
                    file_path = os.path.join(root, file)
                    arc_path = file_path[10:]  # Remove "epub_full/" prefix
                    epub.write(file_path, arc_path)

    # Print summary
    total_words = sum(info['word_count'] for info in chapter_info)
    print(f"\n{'='*60}")
    print(f"✓ EPUB created successfully: {epub_filename}")
    print(f"{'='*60}")
    print(f"Total chapters: {len(chapter_info)}")
    print(f"Total word count: {total_words:,} words")
    print(f"\nChapter breakdown:")
    for info in chapter_info:
        print(f"  Ch {info['number']}: {info['title'][:40]:40} ({info['word_count']:5,} words)")

    return epub_filename

if __name__ == "__main__":
    create_epub()
