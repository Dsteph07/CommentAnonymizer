from typing import Dict


class PersonMapper:
    FAKE_NAMES = [
        "Alex", "Sam", "Jordan", "Charlie", "Morgan", "Taylor", "Casey",
        "Riley", "Jamie", "Robin", "Avery", "Drew", "Quinn", "Skyler",
        "Emery", "Parker", "Reese", "Rowan", "Sage", "Elliot", "Harper"
    ]

    def __init__(self) -> None:
        self.mapping: Dict[str, str] = {}
        self.fake_name_index = 0

    def pseudonymize(self, value: str) -> str:
        if value is None:
            return ""

        original = str(value).strip()

        if not original:
            return original

        if original not in self.mapping:
            if self.fake_name_index < len(self.FAKE_NAMES):
                fake_name = self.FAKE_NAMES[self.fake_name_index]
            else:
                fake_name = f"User{self.fake_name_index}"
            self.mapping[original] = fake_name
            self.fake_name_index += 1

        return self.mapping[original]

    def export_mapping(self) -> Dict[str, str]:
        return dict(self.mapping)