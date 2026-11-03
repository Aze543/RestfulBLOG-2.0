import re
import nh3
import hashlib



JUNK = r"(?:\s|&nbsp;|<br\s*/?>)"
ALLOWED_TAGS = {"p", "br", "strong", "em", "u", "s", "a", "ul", "ol", "li",
                "blockquote", "h2", "h3", "h4", "img", "pre", "code"}
ALLOWED_ATTRS = {"a": {"href", "title"}, "img": {"src", "alt"}}

def sanitize_html(html):
    return nh3.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        url_schemes={"http", "https", "mailto"},
    )
def clean_comment(html):
    html = html.strip()
    prev = None
    while html != prev:
        prev = html
        # 1. empty trailing paragraphs: <p>&nbsp;</p>, <p><br /></p>
        html = re.sub(rf"<p>{JUNK}*</p>\s*$", "", html, flags=re.I)
        # 2. junk at the end of the last paragraph: "text<br />&nbsp;</p>"
        html = re.sub(rf"{JUNK}+(?=</p>\s*$)", "", html, flags=re.I)
        # 3. junk at the very end
        html = re.sub(rf"{JUNK}+$", "", html, flags=re.I)
        html = html.strip()
    return html


def gravatar_url(email, size=200):
    digest = hashlib.sha256(email.strip().lower().encode()).hexdigest()
    return f"https://www.gravatar.com/avatar/{digest}?s={size}&d=identicon"
