from __future__ import annotations

import re
import sys
from calendar import DECEMBER, JANUARY, NOVEMBER, OCTOBER, SEPTEMBER
from datetime import datetime
from typing import Annotated, Literal
from warnings import warn

from pydantic import Field, validate_call

type Title = Literal[
    "Armistice",
    "Beaujolais Nouveau",
    "Black Friday",
    "Christmas",
    "Cyber Monday",
    "Double Ninth Festival",
    "Día de los Muertos",
    "Feast of Saint Ambrose",
    "Feast of the Immaculate Conception",
    "Halloween",
    "Hobbit Day",
    "Journées Européennes du Patrimoine",
    "Labor Day",
    "Mid-Autumn Festival",
    "National Day Golden Week",
    "New Year's Eve",
    "Pi Day",
    "Rentrée",
    "Santo Stefano (Boxing Day)",
    "Singles' Day",
    "Star Wars Day",
    "Thanksgiving",
    "Towel day",
    "Winter Solstice",
]

type Label = Literal[
    'China',
    'Family',
    'France',
    'Italy',
    'Mexico',
    'Pop',
    'USA',
]


class Event:
    @validate_call
    def __init__(
            self,
            title: Annotated[str, Field(
                description='The name of the event.',
                examples=["Thanksgiving", "Christmas"],
            )],

            description: Annotated[str, Field(
                max_length=350,
                description="""
            A 300-character guide for attending guests.

            Covers:
            1. What the event honors, celebrates, or its origin/purpose.
            2. Essential traditions, dress code, key items to bring, food, or drink.
            3. Essential etiquette and traditional greetings or phrases to say.

            Tone: Helpful, sweet, clear, and action-oriented.
            """
            )],
            start: Annotated[datetime, Field(
                description="Start date and time of the event.",
                ge=datetime(2026, 9, 1),
                le=datetime(2027, 1, 2))],

            stop: Annotated[datetime, Field(
                description="End date and time of the event.",
                ge=datetime(2026, 9, 1),
                le=datetime(2027, 1, 2))],

            *labels: Annotated[Label, Field(
                description='Labels associated with the event.',
                min_length=1,
            )]):
        self.title = title.strip()
        self.description = re.sub(r"\s+", " ", description.strip())
        self.start = start
        self.stop = stop
        self.labels = set(labels)

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value: str, seen=set[str]()):
        if value in seen:
            warn(f"Event title '{value}' is already used.", UserWarning, stacklevel=3, skip_file_prefixes=(sys.prefix,))

        seen.add(value)
        self.__title = value

    def __lt__(self, other: Event) -> bool:
        return self.stop < other.stop if self.start == other.start else self.start < other.start


EVENTS: list[Event] = sorted((

    Event(
        "Rentrée",
        """
        Marks the back-to-school and post-summer work return in France.
        Wear smart professional or fresh school attire, stock up on new stationery,
        and greet colleagues with a cheerful "Bonne rentrée!"
        """,
        datetime(2026, SEPTEMBER, 1, 8, 0), datetime(2026, SEPTEMBER, 1, 18, 0),
        'France'
    ),

    Event(
        "Journées Européennes du Patrimoine",
        """
        Opens cultural monuments and historic sites to the public for free exploration.
        Wear comfortable walking shoes, bring a camera,
        and greet guides politely while discovering fascinating architectural heritage.
        """,
        datetime(2026, SEPTEMBER, 19, 9, 0), datetime(2026, SEPTEMBER, 20, 19, 0),
        'France'
    ),

    Event(
        "Mid-Autumn Festival",
        """
        Celebrates the autumn harvest and lunar worship under the brightest full moon.
        Wear comfortable festive attire and bring delicious mooncakes and tea to share.
        Greet others with "Happy Mid-Autumn Festival," express gratitude for family togetherness,
        and enjoy admiring the glowing lanterns.
        """,
        datetime(2026, SEPTEMBER, 25, 0, 0), datetime(2026, SEPTEMBER, 25, 23, 59),
        'China'
    ),

    Event(
        "National Day Golden Week",
        """
        Commemorates the founding of the People's Republic of China with national pride.
        Wear neat, festive clothing and carry your passport or travel essentials if exploring.
        Greet friends with "Happy National Day," be respectful during flag-raising ceremonies,
        and enjoy a joyous holiday week!
        """,
        datetime(2026, OCTOBER, 1, 0, 0), datetime(2026, OCTOBER, 7, 23, 59),
        'China'
    ),

    Event(
        "Double Ninth Festival",
        """
        Honors seniors and ancestor veneration on the ninth day of the ninth lunar month.
        Wear comfortable outdoor attire for climbing heights, bring chrysanthemum wine,
        and greet elders respectfully wishing them health and longevity.
        """,
        datetime(2026, OCTOBER, 19, 0, 0), datetime(2026, OCTOBER, 19, 23, 59),
        'China'
    ),

    Event(
        "Halloween",
        """
        Celebrates the spooky season and ancient traditions of costume fun.
        Wear a creative or playful costume, and bring candy or treats to share with trick-or-treaters.
        Greet people with a playful "Happy Halloween", practice polite trick-or-treating etiquette,
        and enjoy the festive thrills!
        """,
        datetime(2026, OCTOBER, 31, 18, 0), datetime(2026, OCTOBER, 31, 23, 59),
    ),

    Event(
        "Singles' Day",
        """
        Celebrates being single with massive online shopping sprees and treating oneself.
        Wear fun casual clothes, keep your cart ready for flash sales, and greet friends with joyful shopping energy!
        """,
        datetime(2026, NOVEMBER, 11, 0, 0), datetime(2026, NOVEMBER, 11, 23, 59),
        'China'
    ),

    Event(
        "Armistice",
        """
        Commemorates the armistice signed between the Allies of World War I and Germany.
        Wear respectful dark attire, observe a moment of silence at the 11th hour, and reflect on peace and remembrance.
        """,
        datetime(2026, NOVEMBER, 11, 8, 0), datetime(2026, NOVEMBER, 11, 18, 0),
        'France'
    ),

    Event(
        "Beaujolais Nouveau",
        """
        Celebrates the release of the year's fresh wine harvest in French tradition.
        Wear chic casual attire and bring a cheerful attitude to taste the fruity new vintage.
        Greet guests with "Le Beaujolais Nouveau est arrivé!," sip mindfully with local cheese,
        and enjoy a lively bistro atmosphere.
        """,
        datetime(2026, NOVEMBER, 19, 0, 0), datetime(2026, NOVEMBER, 19, 23, 59),
        'France'
    ),

    Event(
        "Thanksgiving",
        """
        The 1621 harvest feast and gratitude. Traditional attire is cozy and casual.
        Bring a side dish or bottle of wine, and come hungry for turkey, stuffing, and pie!
        Say "Happy Thanksgiving," remember to compliment the cook, and enjoy a warm, joyful feast with loved ones.
        """,
        datetime(2026, NOVEMBER, 26, 12, 0), datetime(2026, NOVEMBER, 26, 23, 59),
        'USA'
    ),

    Event(
        "Black Friday",
        """
        Marks the kick-off of the holiday shopping season with major retail deals.
        Wear comfortable walking shoes and casual layers, and bring your shopping list and patience.
        Greet fellow shoppers politely, practice good line etiquette, and score some wonderful gifts!
        """,
        datetime(2026, NOVEMBER, 27, 6, 0), datetime(2026, NOVEMBER, 27, 23, 59),
        'USA'
    ),

    Event(
        "Cyber Monday",
        """
        Celebrates online shopping with digital discounts and tech deals from home.
        Wear comfy loungewear, have your payment details ready, and keep a wish list handy.
        Share great find links with friends cheerfully, stay secure online, and enjoy stress-free holiday browsing.
        """,
        datetime(2026, NOVEMBER, 30, 0, 0), datetime(2026, NOVEMBER, 30, 23, 59),
        'Pop'
    ),

    Event(
        "Winter Solstice",
        """
        Honors the longest night of the year and the return of longer daylight.
        Wear cozy warm sweaters and prepare traditional foods like sweet rice dumplings.
        Greet family with warm wishes for health, gather closely by the hearth,
        and celebrate the peaceful turning of the seasons.
        """,
        datetime(2026, DECEMBER, 21, 0, 0), datetime(2026, DECEMBER, 21, 23, 59),
        'China'
    ),

    Event(
        "Christmas",
        """
        Join the festive cheer with gift exchanges and joyous carols. Wear a fun festive sweater or smart casual attire.
        Bring beautifully wrapped gifts or a holiday treat like cookies.
        Greet others warmly with "Merry Christmas" and share in the joy.
        """,
        datetime(2026, DECEMBER, 25, 0, 0), datetime(2026, DECEMBER, 25, 23, 59),
    ),

    Event(
        "New Year's Eve",
        """
        Bids farewell to the passing year and welcomes the new one with hope and joy.
        Wear sparkling, celebratory evening attire and bring a toast beverage or party snacks.
        Greet friends with "Happy New Year!", countdown with enthusiasm, and celebrate safely into the night.
        """,
        datetime(2026, DECEMBER, 31, 20, 0), datetime(2027, JANUARY, 1, 1, 0),
    ),

))

if __name__ == "__main__":
    from pathlib import Path
    import pysbd


    def reformat(path: Path):
        """
        Reformats the source code.
        - sort events by datetimes
        - use month constants
        - fill paragraphs
        - double-quote the Title literal values and Event titles
        - single-quote the Label literal values and Event labels
        - sort Literals
        """

        import ast
        import json
        from calendar import month_name
        from typing import cast, TypeIs

        MAXLENGTH = 120

        PUNCT = re.compile(r"[,;:](?=\s)")
        SEGMENT = pysbd.Segmenter(language="en", clean=False).segment
        MONTHS = {name.upper(): number for number, name in enumerate(month_name) if name}
        LITERAL_QUOTES = {"Title": '"', "Label": "'"}  # quote mark of each Literal's values
        TITLE_QUOTE = '"'  # Event.title
        LABEL_QUOTE = "'"  # Event.labels (the variadic arguments, from index LABELS_INDEX)
        LABELS_INDEX = 4

        def quote(value: str, mark: str) -> str:
            """Write `value` as a Python string literal delimited by `mark` (a single or double quote)."""
            body = json.dumps(value, ensure_ascii=False)[1:-1]  # double-quoted escaping, without the quotes
            if mark == '"':
                return f'"{body}"'
            # switch to single quotes: unescape \" and escape '
            body = body.replace('\\"', '"').replace("'", "\\'")
            return f"'{body}'"

        def fill(sentence: str, maxlength: int) -> list[str]:
            """Split a sentence into pieces of at most `maxlength` chars.

            Prefer breaking after punctuation, then at a space.
            """
            pieces = []
            while len(sentence) > maxlength:
                # Last punctuation (followed by whitespace) that keeps the piece within maxlength.
                cut = max(
                    (m.end() for m in PUNCT.finditer(sentence) if m.end() <= maxlength),
                    default=0,
                )
                if not cut:
                    # Fallback: last space that fits.
                    cut = sentence.rfind(" ", 0, maxlength + 1)
                if cut <= 0:
                    # A single word that's too long: break after it.
                    cut = sentence.find(" ") % len(sentence) or len(sentence)
                pieces.append(sentence[:cut].rstrip())
                sentence = sentence[cut:].lstrip()
            pieces.append(sentence)
            return pieces

        def fill_paragraph(text: str, maxlength: int) -> str:
            lines: list[str] = []
            line = ""
            for sentence in SEGMENT(text):
                for piece in fill(sentence.strip(), maxlength):
                    if line and len(line) + 1 + len(piece) > maxlength:
                        lines.append(line)
                        line = piece
                    else:
                        line = f"{line} {piece}".strip()
            if line:
                lines.append(line)
            return "\n".join(lines)

        def dt_repr(dt: datetime) -> str:
            fields = [dt.year, month_name[dt.month].upper(), dt.day, dt.hour, dt.minute]
            if dt.second:
                fields.append(dt.second)
            return f"datetime({', '.join(map(str, fields))})"

        def locate(source: str):
            """Return the UTF-8 bytes of `source` and a function giving a node's (begin, end) byte offsets."""
            data = source.encode()
            starts = [0]
            for raw in data.splitlines(keepends=True):
                starts.append(starts[-1] + len(raw))

            def span(node: ast.expr | ast.stmt) -> tuple[int, int]:
                # ast columns are UTF-8 byte offsets
                return starts[node.lineno - 1] + node.col_offset, starts[node.end_lineno - 1] + node.end_col_offset

            return data, span

        def apply(data: bytes, edits: list[tuple[int, int, bytes]]) -> str:
            for begin, end, new in sorted(edits, reverse=True):  # back to front keeps offsets valid
                data = data[:begin] + new + data[end:]
            return data.decode()

        def is_call(node: ast.AST, name: str) -> TypeIs[ast.Call]:
            return isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == name

        def instances[T](iterable, typ: type[T]):
            for item in iterable:
                if isinstance(item, typ):
                    yield item

        def event_calls(tree: ast.AST):
            return [call for call in instances(ast.walk(tree), ast.Call) if is_call(call, "Event")]

        def event_argument(call: ast.Call, index: int, name: str) -> ast.expr | None:
            if len(call.args) > index:
                return call.args[index]
            return next((k.value for k in call.keywords if k.arg == name), None)

        def literal_datetime(call: ast.AST) -> datetime | None:
            """Evaluate `datetime(2026, SEPTEMBER, 1, 8, 0)` or `datetime(2026, 9, 1)` without running any code."""
            if not is_call(call, "datetime") or call.keywords:
                return None
            values: list[int] = []
            for arg in call.args:
                if isinstance(arg, ast.Constant) and type(arg.value) is int:
                    values.append(arg.value)
                elif isinstance(arg, ast.Name) and arg.id in MONTHS:
                    values.append(MONTHS[arg.id])
                else:
                    return None
            try:
                return datetime(*values)
            except (TypeError, ValueError):
                return None

        def month_names(source: str) -> str:
            """Write every datetime of an `Event(...)` with the plain english month name."""
            data, span = locate(source)
            edits = []
            for event in event_calls(ast.parse(source)):
                for node in instances(ast.walk(event), ast.expr | ast.stmt):
                    if (value := literal_datetime(node)) is not None:
                        begin, end = span(node)
                        edits.append((begin, end, dt_repr(value).encode()))
            return apply(data, edits)

        def calendar_import(source: str) -> str:
            """Keep `from calendar import ...` in sync with the month names actually used."""
            tree = ast.parse(source)
            used = sorted({name.id for name in instances(ast.walk(tree), ast.Name) if name.id in MONTHS})
            if not used:
                return source
            data, span = locate(source)
            for node in tree.body:
                if (isinstance(node, ast.ImportFrom) and node.module == "calendar" and node.level == 0
                        and all(a.name in MONTHS and a.asname is None for a in node.names)):
                    line = f"from calendar import {', '.join(used)}"
                    if len(line) > MAXLENGTH:
                        line = "from calendar import (\n" + "".join(f"    {name},\n" for name in used) + ")"
                    begin, end = span(node)
                    return apply(data, [(begin, end, line.encode())])
            return source

        def literal_values(source: str) -> str:
            """Write the values of the `Title` (double-quoted) and `Label` (single-quoted) literals,
            one per line, sorted (and unique)."""
            data, span = locate(source)
            edits = []
            for node in ast.parse(source).body:
                if not (isinstance(node, ast.TypeAlias)
                        and isinstance(node.name, ast.Name) and node.name.id in LITERAL_QUOTES):
                    continue
                literal = node.value
                if not (isinstance(literal, ast.Subscript) and isinstance(literal.value, ast.Name)
                        and literal.value.id == "Literal"):
                    continue
                subscript = literal.slice
                items = subscript.elts if isinstance(subscript, ast.Tuple) else [subscript]
                strings: list[str] = []
                for constant in instances(items, ast.Constant):
                    if isinstance(value := constant.value, str):
                        strings.append(value)
                if len(strings) != len(items):
                    continue  # only handle plain string values
                indent = " " * node.col_offset
                mark = LITERAL_QUOTES[node.name.id]
                lines = "".join(
                    f"{indent}    {quote(value, mark)},\n"
                    for value in sorted(set(strings))
                )
                begin, end = span(literal)
                edits.append((begin, end, f"Literal[\n{lines}{indent}]".encode()))
            return apply(data, edits)

        def event_strings(source: str) -> str:
            """Write the title of every `Event(...)` double-quoted and its labels single-quoted."""
            data, span = locate(source)
            edits = []

            def requote(arg: ast.expr | None, mark: str):
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    begin, end = span(arg)
                    if not data[begin:end].startswith((b'"""', b"'''")):  # leave multi-line strings alone
                        edits.append((begin, end, quote(arg.value, mark).encode()))

            for event in event_calls(ast.parse(source)):
                requote(event_argument(event, 0, "title"), TITLE_QUOTE)
                for label in event.args[LABELS_INDEX:]:
                    requote(label, LABEL_QUOTE)
            return apply(data, edits)

        def wrap_descriptions(source: str) -> str:
            """Re-wrap the description of every `Event(...)`."""
            data, span = locate(source)
            edits = []
            for event in event_calls(ast.parse(source)):
                arg = event_argument(event, 1, "description")
                if isinstance(constant := arg, ast.Constant) and isinstance(value := constant.value, str):
                    begin, end = span(constant)
                    if not data[begin:end].startswith(b'"""') or b"\\" in data[begin:end]:
                        continue  # only handle plain triple-quoted strings
                    indent = " " * constant.col_offset
                    body = fill_paragraph(" ".join(value.split()), MAXLENGTH - len(indent))
                    body = body.replace("\n", "\n" + indent)
                    edits.append((begin, end, f'"""\n{indent}{body}\n{indent}"""'.encode()))
            return apply(data, edits)

        def literal_argument(call: ast.Call, index: int, name: str) -> datetime | None:
            arg = event_argument(call, index, name)
            return literal_datetime(arg) if arg is not None else None

        def sort_events(source: str) -> str:
            """Order the events of `sorted((Event(...), ...))` by start, then stop, like `Event.__lt__`."""
            tree = ast.parse(source)
            data, span = locate(source)
            for call in ast.walk(tree):
                if not is_call(call, "sorted") or not call.args:
                    continue
                container = call.args[0]
                if not isinstance(container, (ast.Tuple, ast.List)):
                    continue
                items = container.elts
                events = cast(list[ast.Call], [item for item in items if is_call(item, "Event")])
                if not events or len(events) != len(items):
                    continue
                sort_keys: list[tuple[datetime, datetime]] = []
                for event in events:
                    begin_dt = literal_argument(event, 2, "start")
                    end_dt = literal_argument(event, 3, "stop")
                    if begin_dt is None or end_dt is None:
                        return source  # a datetime that is not a literal: can't order it statically
                    sort_keys.append((begin_dt, end_dt))
                order = sorted(range(len(events)), key=lambda i: sort_keys[i])  # stable, like runtime `sorted`
                spans = [span(event) for event in events]
                return apply(data, [(begin, end, data[spans[j][0]:spans[j][1]])
                                    for (begin, end), j in zip(spans, order)])
            return source

        def reformat_source(source: str) -> str:
            for step in (literal_values, event_strings, month_names, calendar_import, wrap_descriptions, sort_events):
                source = step(source)
            return source

        old = path.read_text(encoding="utf-8")
        new = reformat_source(old)
        if new != old:
            path.write_text(new, encoding="utf-8")
            print(f"{path.name} reformatted.")
        else:
            print(f"{path.name} already formatted.")


    def report_missing_events():
        from typing import get_args

        actual: set[str] = {event.title for event in EVENTS}
        expected: set[str] = set(get_args(Title.__value__))
        if missing := expected - actual:
            names: list[str] = sorted(repr(title) for title in missing)
            print("Missing Events:", ", ".join(names))


    report_missing_events()
    reformat(Path(__file__))
