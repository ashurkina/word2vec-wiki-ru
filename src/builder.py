"""
Построение текстового корпуса.
"""

import time
from pathlib import Path

from tqdm import tqdm

from .cleaner import WikiCleaner
from .parser import WikipediaParser


class CorpusBuilder:
    """Строит текстовый корпус из дампа Википедии."""

    def __init__(
        self,
        parser: WikipediaParser,
        cleaner: WikiCleaner,
    ):
        self.parser = parser
        self.cleaner = cleaner

    def build(
        self,
        output_path: Path,
        limit: int | None = None,
    ) -> None:
        """
        Построить текстовый корпус.

        Parameters
        ----------
        output_path : Path
            Путь для сохранения корпуса.

        limit : int | None
            Максимальное количество статей.
            Если None, будет обработан весь дамп.
        """

        output_path.parent.mkdir(parents=True, exist_ok=True)

        processed = 0
        saved = 0

        start_time = time.perf_counter()

        progress = tqdm(
            desc="Построение корпуса",
            unit=" статей",
        )

        with output_path.open("w", encoding="utf-8") as output:

            for article in self.parser.articles():

                processed += 1

                text = self.cleaner.clean(article.text).strip()

                if text:

                    output.write(text)
                    output.write("\n\n")

                    saved += 1

                progress.update(1)

                if limit is not None and processed >= limit:
                    break

        progress.close()

        elapsed = time.perf_counter() - start_time

        print("\nПостроение корпуса завершено.")
        print(f"Прочитано статей : {processed:,}")
        print(f"Сохранено статей : {saved:,}")
        print(f"Время выполнения : {elapsed:.1f} сек ({elapsed / 60:.1f} мин)")
        print(f"Корпус сохранен в: {output_path}")