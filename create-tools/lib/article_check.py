"""Is a looked-up Wikipedia article the thing meant? Shared by `names.py lookup` and `wiki_cite.py`
(sprint 033), so the two never drift.

`--expect KEYWORD` checks the **article**: its short description and first line must say the keyword,
or it may be a namesake ("Army Medical School" quietly cited the US school; "Hideo Kodama" is a
politician). `--expect-item KEYWORD` (names.py only) checks the Wikidata **item** as well: its
description and class, for an article whose item is something else (the Duffy blood group's item is
the ACKR1 gene product). The item check is opt-in: it warned on right items in six of sprint 030's
authors' lookups ("Second Geneva Convention" is a treaty).

A batch can carry a keyword per title, `Title=keyword`; a title with none takes the run's
`--expect`. Standard library only.
"""

def untex(text):
    """Plain text without the TeX a formula leaves behind in an extract ("{\\displaystyle …}")."""
    while (i := text.find('{\\displaystyle')) >= 0:
        depth, j = 0, i
        for j in range(i, len(text)):
            depth += {'{': 1, '}': -1}.get(text[j], 0)
            if depth == 0:
                break
        text = text[:i].rstrip() + text[j + 1:]
    return text


def expectations(titles, default=None):
    """[(title, keyword or None)]: `Title=keyword` gives a title its own keyword, and any other
    title takes `default`. An `=` with nothing after it is part of the title."""
    out = []
    for t in titles:
        title, sep, keyword = t.rpartition('=')
        if sep and title.strip() and keyword.strip():
            out.append((title.strip(), keyword.strip()))
        else:
            out.append((t, default))
    return out


def article_mismatch(name, description, first_line, keyword):
    """Why the article `name` may be a namesake: `keyword` is in neither its description nor its
    first line. None when it is, or when there is no keyword."""
    if not keyword:
        return None
    if keyword.lower() in f'{description or ""} {first_line or ""}'.lower():
        return None
    return f'"{name}" does not say {keyword!r}: is it a namesake? ({description or first_line or "no description"})'


def item_mismatch(name, qid, item_description, classes, keyword):
    """Why the article's Wikidata item may be something else: `keyword` is in neither the item's
    description nor its classes. None when it is, or when there is no keyword."""
    if not keyword:
        return None
    if keyword.lower() in f'{item_description or ""} {" ".join(classes)}'.lower():
        return None
    what = ', '.join(classes) or 'no class'
    return (f'"{name}"\'s Wikidata item {qid} is a {what} ({item_description or "no description"}), which does '
            f'not say {keyword!r}: read the item; if it is the thing meant, described in other words, keep it, '
            f'and if it is something else, find the item the article means on Wikidata')
