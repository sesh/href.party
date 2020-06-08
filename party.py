import sys
from datetime import datetime, timezone

from sources.sources import *

BASE_HTML = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="description" content="">
    <title>Headlines</title>
    <link rel="stylesheet" href="https://cdn.statically.io/gh/sesh/brntn-css-2/master/brntn2.css">

    <style>
        header, footer {
            align-items: center;
        }

        .container {
            font-size: 13px;
            max-width: 96%;
            margin: 0 auto;
        }

        ul {
            width: 100%;
        }

        .grid {
            flex-wrap: wrap;
        }

        li {
            border-bottom: 1px solid #f1f3f5;
            padding: 4px 0;
        }

        @media (min-width:30em) {
            .container {
                width: 84em;
            }

            ul {
                width: 26em;
            }
        }

         .tta {
            background-color: #ffec99;
            padding: 8px;
            margin: 1em 0;
            width: 100%;
            color: #343a40;
        }

        .tta .pre {
            background-color: #fcc419;
            border-radius: 2px;
            padding: 4px 8px;
            font-weight: bold;
            margin-right: 0.6em;
            color: #495057;
        }

        body {  background-color: #1d1f21;  color: #c5c8c6;}a:link {  color: #81a2be;}a:visited { color: #546e89}
    </style>
</head>
<body>
    <header class="container grid">
        <h1>href.party</h1>
        <p>A whole bunch of links</p>
    </header>
    <div class="container grid">
        {{content}}
    </div>
    <footer class="container grid">
        <p>Sites selected by <a href="https://twitter.com/sesh">@sesh</a>. New sources welcome via <a href="https://github.com/sesh/href.party">Github</a>.<p>
    </footer>
</body>
</html>
"""

if __name__ == "__main__":
    # --quick option to output the first and last sources only to speed things up

    html = nyt.as_html()

    if "--quick" not in sys.argv:
        html += npr.as_html()
        html += atlantic.as_html()
        html += theage.as_html()
        html += abc_au.as_html()
        html += guardian_au.as_html()

    html += "<div class='tta'><span class='pre'>Ad</span> Need a cheap VPS host? Try <a href='https://www.vultr.com/?ref=6899304'>Vultr</a> with $100 credit and support this site.</div>"

    if "--quick" not in sys.argv:
        html += theverge.as_html()
        html += techmeme.as_html(5)  # techmeme has some _long_ headlines
        html += itnews.as_html()
        html += hn500.as_html()
        html += hn.as_html()

    html += lobsters.as_html()

    html += "<div class='tta'><span class='pre'>Ad</span> I don't like Uber's vibe right now. Give <a href='https://www.ola.com.au'>Ola</a> a shot for your next ride and support this site.</div>"

    html += the_wirecutter.as_html()
    html += oz_bargain.as_html()
    html += strategist.as_html()

    with open("public/index.html", "w") as out:
        template = BASE_HTML
        template = template.replace("{{content}}", html)

        now_utc = datetime.now(timezone.utc)
        template = template.replace(
            "</footer>", f"<p>Generated on {now_utc.strftime('%b %d at %X')} UTC</p>"
        )
        out.write(template)
