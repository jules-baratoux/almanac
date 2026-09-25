from __future__ import annotations

import re
from calendar import DECEMBER, JANUARY, NOVEMBER, OCTOBER, SEPTEMBER
from datetime import datetime
from typing import Annotated, Literal

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

    def __lt__(self, other: Event) -> bool:
        return self.stop < other.stop if self.start == other.start else self.start < other.start


EVENTS: list[Event] = sorted((

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
