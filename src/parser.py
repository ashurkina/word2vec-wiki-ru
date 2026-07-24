"""
Потоковый парсер дампа Википедии.
Отвечает только за чтение XML и извлечение статей.
"""

import bz2
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

# Пространство имен XML, используемое в дампе Википедии
NS = "{http://www.mediawiki.org/xml/export-0.11/}"


@dataclass
class Article:
    """Статья Википедии."""

    title: str
    text: str


class WikipediaParser:
    """Потоковый парсер XML-дампа Википедии."""

    def __init__(self, dump_path: Path):
        self.dump_path = dump_path

    def articles(self) -> Generator[Article, None, None]:
        """
        Последовательно возвращает статьи из дампа.

        Yields:
            Article
        """

        with bz2.open(self.dump_path, "rb") as file:

            for _, element in ET.iterparse(file, events=("end",)):

                if element.tag != f"{NS}page":
                    continue

                # Пропускаем страницы-перенаправления
                if element.find(f"{NS}redirect") is not None:
                    element.clear()
                    continue

                title = element.findtext(f"{NS}title") or ""

                revision = element.find(f"{NS}revision")

                text = ""

                if revision is not None:
                    text = revision.findtext(f"{NS}text") or ""

                yield Article(
                    title=title,
                    text=text,
                )

                # Освобождаем память
                element.clear()