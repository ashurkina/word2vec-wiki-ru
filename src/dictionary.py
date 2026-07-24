"""
Частотный словарь слов.
"""

from collections import Counter
from collections.abc import Iterator
from pathlib import Path
import json


class FrequencyDictionary:
    """Частотный словарь слов."""

    def __init__(self):
        self.word_counts = Counter()

    @property
    def vocabulary_size(self) -> int:
        """
        Количество уникальных слов.
        """
        return len(self.word_counts)

    @property
    def total_words(self) -> int:
        """
        Общее количество слов.
        """
        return sum(self.word_counts.values())

    def fit(self, tokens: Iterator[str]) -> None:
        """
        Построить частотный словарь.

        Parameters
        ----------
        tokens
            Последовательность токенов.
        """

        self.word_counts.update(tokens)

    def most_common(self, n: int = 20) -> list[tuple[str, int]]:
        """
        Вернуть наиболее частые слова.

        Parameters
        ----------
        n
            Количество слов.

        Returns
        -------
        list[tuple[str, int]]
        """

        return self.word_counts.most_common(n)

    def suggest(
        self,
        prefix: str,
        top_k: int = 10,
    ) -> list[tuple[str, int]]:
        """
        Предложить наиболее вероятные слова,
        начинающиеся с указанного префикса.

        Parameters
        ----------
        prefix
            Начало слова.

        top_k
            Максимальное количество предложений.

        Returns
        -------
        list[tuple[str, int]]
        """

        prefix = prefix.lower()

        suggestions = []

        for word, frequency in self.word_counts.items():

            if word.startswith(prefix):
                suggestions.append((word, frequency))

        suggestions.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return suggestions[:top_k]

    def save(self, path: Path) -> None:
        """
        Сохранить словарь в JSON.
        """

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.word_counts,
                file,
                ensure_ascii=False,
            )

    def load(self, path: Path) -> None:
        """
        Загрузить словарь из JSON.
        """

        with path.open(
            encoding="utf-8",
        ) as file:

            self.word_counts = Counter(
                json.load(file)
            )