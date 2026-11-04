import natural
from events import EVENTS
from main import get_event_image, slugify


def main() -> None:
    events_without_images = (
        event
        for event in EVENTS
        if not get_event_image(event)
    )

    five_most_popular = sorted(
        events_without_images,
        key=lambda event: event.people,
        reverse=True,
    )[:10]

    for event in five_most_popular:
        print(f"{event.title}: {natural.number(event.people)} -> {slugify(event.title)}")


if __name__ == "__main__":
    main()
