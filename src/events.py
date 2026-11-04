from __future__ import annotations

import re
from calendar import DECEMBER, NOVEMBER, OCTOBER, SEPTEMBER
from datetime import date, timedelta
from enum import Enum
from typing import Annotated, Sequence

from annotated import Field
from dates import *
from dispatch import overload
from stats import amazigh_people, ehd_participants, french_people, jews, observant_jews, us_population, us_workers

type Title = Annotated[str, Field(
    description='The name of the event.',
    examples=[
        "Christmas",
        "Hanukkah",
        "Thanksgiving",
        "Towel day",
    ])
]

type Description = Annotated[str, Field(
    max_length=350,
    description="""
A 300-character guide for attending guests.

Covers:
1. What the event honors, celebrates, or its origin/purpose.
2. Essential traditions, dress code, key items to bring, food, or drink.
3. Essential etiquette and traditional greetings or phrases to say.

Tone: Helpful, sweet, clear, and action-oriented.
"""
)]

type Date = Annotated[date, Field(
    description="When a event starts or stops.",
    ge=date(2026, 1, 1),
    le=date(2027, 1, 13)
)]

type Days = Annotated[int, Field(
    description="The duration of an event in days.",
    ge=1)
]

type People = Annotated[int | float, Field(
    description="An estimated amount of people celebrating the event worldwide.",
    ge=1)
]


class Labels(Enum):
    """Labels associated with an event."""

    ALGERIA = "Algeria"
    CHINA = "China"
    FAMILY = "Family"
    FRANCE = "France"
    ISLAM = "Islam"
    ITALY = "Italy"
    ISRAEL = "Israel"
    MEXICO = "Mexico"
    POP = "Pop"
    USA = "USA"


class Event:

    @overload
    def __init__(
            self,
            title: Title,
            start: Date,
            end: Date,
            description: Description,
            people: People,
            *labels: Labels,
    ):
        self.title = title.strip()
        self.description = re.sub(r"\s+", " ", description.strip())
        self.start = start
        self.end = end
        self.people = people
        self.labels = labels

    @overload
    def __init__(
            self,
            title: Title,
            start: Date,
            description: Description,
            people: People,
            *labels: Labels,
    ):
        self.__init__(title, start, start + timedelta(days=1), description, people, *labels)

    @overload
    def __init__(
            self,
            title: Title,
            dates: Sequence[Date],
            description: Description,
            people: People,
            *labels: Labels,
    ):
        start: Date = min(dates)
        end: Date = max(dates)
        self.__init__(title, start, end, description, people, *labels)

    def __lt__(self, other: Event) -> bool:
        return self.end < other.end if self.start == other.start else self.start < other.start


EVENTS: list[Event] = sorted((

    Event(
        "Yennayer",
        YENNAYER,
        """
        Celebrates the Amazigh (Berber) New Year, rooted in the ancient agrarian calendar, welcoming the year 2977.
        Wear traditional Kabyle dress or silver jewelry, and share couscous, berkoukes, dried fruits and sweets.
        Greet others warmly with "Aseggas Ameggaz!" for a happy and prosperous new year.
        """,
        amazigh_people,
        Labels.ALGERIA
    ),

    Event(
        "Rentrée",
        date(2026, SEPTEMBER, 1),
        """
        Marks the back-to-school and post-summer work return in France.
        Wear smart professional or fresh school attire, stock up on new stationery,
        and greet colleagues with a cheerful "Bonne rentrée!"
        """,
        17_000_000,
        Labels.FRANCE
    ),

    Event(
        "Labor Day",
        LABOR_DAY,
        """
        Honors the American labor movement and workers' contributions.
        Wear casual weekend clothes or patriotic colors, bring grilled food and drinks for a backyard cookout,
        and enjoy a relaxing day off!
        """,
        us_workers,
        Labels.USA
    ),

    Event(
        "Rosh Hashanah",
        ROSH_HASHANAH,
        """
        Celebrates the Jewish New Year with introspection and sweet new beginnings.
        Wear smart holiday attire, dip apples in honey,
        and greet friends with "Shana Tova U'Metuka" for a sweet year ahead.
        """,
        jews,
        Labels.ISRAEL
    ),

    Event(
        "Programmer's Day",
        date(2026, SEPTEMBER, 13),
        """
        Honors programmers on the 256th day of the year, the number of values in a byte.
        Wear a geeky tech T-shirt and bring pizza, coffee, or cupcakes to share.
        Greet colleagues with "Happy Programmer's Day!", thank your dev team, and never deploy on a Friday!
        """,
        30_000_000,
        Labels.POP
    ),

    Event(
        "European Heritage Days",
        date(2026, SEPTEMBER, 19), date(2026, SEPTEMBER, 20),
        """
        The European Heritage Days are the most widely celebrated participatory cultural event shared by the people of Europe.
        The Council of Europe launched the initiative in 1985, and in 1999 was joined by the European Union.
        The Programme generates the greatest value, Euro for Euro, of any “European” cultural project.
        """,
        ehd_participants,
        Labels.FRANCE
    ),

    Event(
        "Yom Kippur",
        date(2026, SEPTEMBER, 20), date(2026, SEPTEMBER, 21),
        """
        The holiest day in Judaism, focused on atonement and sincere repentance.
        Wear white or modest comfortable clothing, fast for 25 hours,
        and greet others with wishes for an easy and meaningful fast.
        """,
        observant_jews,
        Labels.ISRAEL
    ),

    Event(
        "Hobbit Day",
        date(2026, SEPTEMBER, 22),
        """
        Celebrates the birthdays of Bilbo and Frodo Baggins in Middle-earth style.
        Wear cozy hobbit-inspired or casual outdoor attire, bring hearty food and drinks,
        and greet fans with a joyful "Happy Hobbit Day!"
        """,
        2_000_000,
        Labels.POP
    ),

    Event(
        "Mid-Autumn Festival",
        MID_AUTUMN_FESTIVAL,
        """
        Celebrates the autumn harvest and lunar worship under the brightest full moon.
        Wear comfortable festive attire and bring delicious mooncakes and tea to share.
        Greet others with "Happy Mid-Autumn Festival," express gratitude for family togetherness,
        and enjoy admiring the glowing lanterns.
        """,
        1_000_000_000,
        Labels.CHINA
    ),

    Event(
        "Sukkot",
        SUKKOT,
        """
        Commemorates the shelter of the Israelites in the desert.
        Dine under the leafy roof of a sukkah, and wave the lulav and etrog with gratitude.
        Welcome guests cheerfully with "Chag Sameach" and enjoy communal celebration under the stars!
        """,
        observant_jews,
        Labels.ISRAEL
    ),

    Event(
        "National Day Golden Week",
        *GOLDEN_WEEK,
        """
        Commemorates the founding of the People's Republic of China with national pride.
        Wear neat, festive clothing and carry your passport or travel essentials if exploring.
        Greet friends with "Happy National Day," be respectful during flag-raising ceremonies,
        and enjoy a joyous holiday week!
        """,
        1_300_000_000,
        Labels.CHINA
    ),

    Event(
        "Double Ninth Festival",
        date(2026, OCTOBER, 18), date(2026, OCTOBER, 19),
        """
        Honors seniors and ancestor veneration on the ninth day of the ninth lunar month.
        Wear comfortable outdoor attire for climbing heights, bring chrysanthemum wine,
        and greet elders respectfully wishing them health and longevity.
        """,
        100_000_000,
        Labels.CHINA
    ),

    Event(
        "Mole Day",
        date(2026, OCTOBER, 23),
        """
        Celebrates the mole, chemistry's unit of 6.02×10²³ particles, at 6:02 on 10/23.
        Wear a lab coat or a mole-themed shirt and bring guacamole or mole-shaped treats.
        Greet fellow chemists with "Happy Mole Day!", share a chemistry pun, and keep experiments safe.
        """,
        1_000_000,
        Labels.POP
    ),

    Event(
        "Heure d’hiver",
        date(2026, OCTOBER, 25),
        """
        Marks the end of daylight saving time in France. It was introduced following the 1973 oil crisis and in 2019,
        MEPs voted but failed to abolish it due to Covid-19. Clocks fall back at 3am to 2am.
        Enjoy an extra hour of sleep and see you in March!
        """,
        french_people,
        Labels.FRANCE
    ),

    Event(
        "Halloween",
        date(2026, OCTOBER, 31),
        """
        Celebrates the spooky season and ancient traditions of costume fun.
        Wear a creative or playful costume, and bring candy or treats to share with trick-or-treaters.
        Greet people with a playful "Happy Halloween", practice polite trick-or-treating etiquette,
        and enjoy the festive thrills!
        """,
        375_000_000,
    ),

    Event(
        "Día de Muertos",
        date(2026, NOVEMBER, 1), date(2026, NOVEMBER, 2),
        """
        Celebrates and honors deceased loved ones with vibrant traditions and altars.
        Wear colorful festive clothing or skeleton makeup, bring sugar skulls or pan de muerto,
        and greet others remembering ancestors with joy.
        """,
        100_000_000,
        Labels.MEXICO
    ),

    Event(
        "Algerian Revolution",
        ALGERIAN_REVOLUTION_DAY,
        """
        Commemorates the outbreak of the Algerian War of Independence on November 1, 1954. 
        Launched by the FLN it was also known as Toussaint Rouge before becoming a celebration of Algerian independence.
        Greet others with "Tahya El Djazair!" (Long live Algeria).
        """,
        46_000_000,
        Labels.ALGERIA
    ),

    Event(
        "Armistice Day",
        ARMISTICE,
        """
        Armistice Day, later known as Remembrance Day in the Commonwealth and Veterans Day in the United States,
        mark the armistice signed between the Allies of World War I and Germany at Compiègne.
        It took effect on the "eleventh hour of the eleventh day of the eleventh month" of 1918.
        """,
        100_000_000,
        Labels.FRANCE
    ),

    Event(
        "Beaujolais Nouveau",
        BEAUJOLAIS,
        """
        Celebrates the release of the year's fresh wine harvest in French tradition.
        Wear chic casual attire and bring a cheerful attitude to taste the fruity new vintage.
        Greet guests with "Le Beaujolais Nouveau est arrivé!," sip mindfully with local cheese,
        and enjoy a lively bistro atmosphere.
        """,
        10_000_000,
        Labels.FRANCE
    ),

    Event(
        "World Philosophy Day",
        PHILOSOPHY,
        """
        Celebrates philosophical reflection and open dialogue, proclaimed by UNESCO on the third Thursday of November.
        Bring thought-provoking question to share, be open-minded.
        Greet others with "Happy World Philosophy Day," listen curiously, and debate kindly and respectfully!
        """,
        5_000_000,
        Labels.POP
    ),

    Event(
        "Children's Day",
        date(2026, NOVEMBER, 20),
        """
        Celebrates children’s rights, joy, and well-being on World Children’s Day.
        Wear bright, playful clothes, bring games, books, or treats to share,
        and greet families with "Happy Children's Day!" Be kind, inclusive, and make children feel cherished.
        """,
        2_000_000_000,
        Labels.FAMILY
    ),

    Event(
        "Thanksgiving",
        THANKSGIVING,
        """
        The 1621 harvest feast and gratitude. Traditional attire is cozy and casual.
        Bring a side dish or bottle of wine, and come hungry for turkey, stuffing, and pie!
        Say "Happy Thanksgiving," remember to compliment the cook, and enjoy a warm, joyful feast with loved ones.
        """,
        us_population,
        Labels.USA
    ),

    Event(
        "Black Friday",
        BLACK_FRIDAY,
        """
        Marks the kick-off of the holiday shopping season with major retail deals.
        Wear comfortable walking shoes and casual layers, and bring your shopping list and patience.
        Greet fellow shoppers politely, practice good line etiquette, and score some wonderful gifts!
        """,
        200_000_000,
        Labels.USA
    ),

    Event(
        "Cyber Monday",
        CYBER_MONDAY,
        """
        Celebrates online shopping with digital discounts and tech deals from home.
        Wear comfy loungewear, have your payment details ready, and keep a wish list handy.
        Share great find links with friends cheerfully, stay secure online, and enjoy stress-free holiday browsing.
        """,
        100_000_000,
    ),

    Event(
        "Hanukkah",
        HANUKKAH,
        """
        Celebrates the Festival of Lights and the miracle of the oil flask.
        Wear festive attire, light the menorah each evening, enjoy latkes and sufganiyot,
        and greet friends with "Happy Hanukkah."
        """,
        12_000_000,
        Labels.ISRAEL
    ),

    Event(
        "Sant'Ambrogio",
        SANT_AMBROGIO,
        """
        Honors Milan's patron Sant'Ambrogio with festive celebrations and the opening of the La Scala opera season.
        Wear elegant evening attire, enjoy local panettone, and greet guests warmly with Italian festive cheer.
        """,
        1_400_000,
        Labels.ITALY
    ),

    Event(
        "Immacolata Concezione",
        IMMACOLATA_CONCEZIONE,
        """
        Celebrates the solemn belief regarding the Virgin Mary's conception.
        Wear smart casual attire, attend church services or local light displays,
        and greet others with peaceful holiday blessings.
        """,
        50_000_000,
        Labels.ITALY
    ),

    Event(
        "Winter Solstice",
        date(2026, DECEMBER, 21),
        """
        Honors the longest night of the year and the return of longer daylight.
        Wear cozy warm sweaters and prepare traditional foods like sweet rice dumplings.
        Greet family with warm wishes for health, gather closely by the hearth,
        and celebrate the peaceful turning of the seasons.
        """,
        1_000_000_000,
    ),

    Event(
        "Christmas",
        CHRISTMAS,
        """
        Join the festive cheer with gift exchanges and joyous carols. Wear a fun festive sweater or smart casual attire.
        Bring beautifully wrapped gifts or a holiday treat like cookies.
        Greet others warmly with "Merry Christmas" and share in the joy.
        """,
        2_400_000_000,
    ),

    Event(
        "Santo Stefano (Boxing Day)",
        SANTO_STEFANO,
        """
        Celebrates Saint Stephen's Day in Italy with family gatherings and festive leftovers.
        Wear cozy winter clothes, relax at home or stroll town lights, and greet loved ones with warm holiday wishes.
        """,
        55_000_000,
        Labels.ITALY
    ),

    Event(
        "New Year's Eve",
        NEW_YEAR,
        """
        Bids farewell to the passing year and welcomes the new one with hope and joy.
        Wear sparkling, celebratory evening attire and bring a toast beverage or party snacks.
        Greet friends with "Happy New Year!", countdown with enthusiasm, and celebrate safely into the night.
        """,
        4_000_000_000,
    ),

))
