from dataclasses import dataclass, fields
from typing import Any, Iterator, Sequence

import annotated_types
from sentinel import sentinel

ANNOTATED_TYPE_NAMES = {name.casefold() for name in annotated_types.__all__}

Missing: Any = sentinel("Missing")


@dataclass(frozen=True)
class Field(annotated_types.GroupedMetadata):
    """Mimic Pydantic Field to be used as Annotated metadata.

    >>> Annotated[int, Field(ge=0, description='Positive integer')]
    """
    default: Any = Missing
    # alias: str | Missing = Missing
    # alias_priority: int | Missing = Missing
    # validation_alias: str | AliasPath | AliasChoices | Missing = Missing
    # serialization_alias: str | Missing = Missing
    # title: str | Missing = Missing
    # field_title_generator: Callable[[str, FieldInfo], str] | Missing = Missing
    description: str = Missing
    examples: Sequence[Any] = Missing
    # exclude: bool | Missing = Missing
    # exclude_if: Callable[[Any], bool] | Missing = Missing
    # discriminator: str | types.Discriminator | Missing = Missing
    # deprecated: Deprecated | str | bool | Missing = Missing
    # json_schema_extra: JsonDict | Callable[[JsonDict], None] | Missing = Missing
    # frozen: bool | Missing = Missing
    # validate_default: bool | Missing = Missing
    # repr: bool = None
    # init: bool | Missing = Missing
    # init_var: bool | Missing = Missing
    # kw_only: bool | Missing = Missing
    # pattern: str | re.Pattern[str] | Missing = Missing
    # strict: bool | Missing = Missing
    # coerce_numbers_to_str: bool | Missing = Missing
    gt: annotated_types.SupportsGt = Missing
    ge: annotated_types.SupportsGe = Missing
    lt: annotated_types.SupportsLt = Missing
    le: annotated_types.SupportsLe = Missing
    # multiple_of: float | Missing = Missing
    # allow_inf_nan: bool | Missing = Missing
    # max_digits: int | Missing = Missing
    # decimal_places: int | Missing = Missing
    min_length: int = Missing
    max_length: int = Missing

    # union_mode: Literal['smart', 'left_to_right'] | Missing = Missing
    # fail_fast: bool | Missing = Missing
    # extra: dict

    def __post_init__(self):
        if self.examples is not Missing and not isinstance(self.examples, tuple):
            object.__setattr__(self, "examples", tuple(self.examples))

    def __iter__(self) -> Iterator[object]:
        # Iterating over a GroupedMetadata object should yield annotated-types
        # constraint metadata objects which describe it as fully as possible,
        # and may include other unknown objects too.
        if self.description is not Missing:
            yield annotated_types.doc(self.description)

        for field in fields(self):
            if field.name.casefold() in ANNOTATED_TYPE_NAMES:
                value = getattr(self, field.name)
                if value is not Missing:
                    yield getattr(self, field.name)(value)
