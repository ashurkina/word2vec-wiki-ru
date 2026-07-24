from itertools import permutations
from pathlib import Path


class AnalogyPairsBuilder:
    """Создает пары для оценки аналогий."""

    def __init__(self, input_path: str | Path, output_path: str | Path):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)

    def build(self) -> None:
        # загружаем категории
        categories = self._load_categories()

        # сохраняем пары
        with self.output_path.open("w", encoding="utf-8") as file:
            for category, pairs in categories.items():
                file.write(category + "\n")

                for (a, b), (c, d) in permutations(pairs, 2):
                    file.write(f"{a} {b} {c} {d}\n")

                file.write("\n")

    def _load_categories(self) -> dict[str, list[tuple[str, str]]]:
        # читаем файл
        with self.input_path.open("r", encoding="utf-8") as file:
            lines = file.readlines()

        categories = {}
        current_category = None

        # разбираем категории
        for line in lines:
            line = line.strip()

            if not line:
                continue

            if line.startswith(":"):
                current_category = line
                categories[current_category] = []
            else:
                word1, word2 = line.split()
                categories[current_category].append((word1, word2))

        return categories