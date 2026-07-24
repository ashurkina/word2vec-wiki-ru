"""
Токенизация текста.
"""

from collections.abc import Iterator


class Tokenizer:
    """Простейший токенизатор русского текста."""

    def tokenize(self, text: str) -> list[str]:
        """
        Разбить текст на список слов.
        """

        return list(self.tokenize_text(text))

    def tokenize_text(self, text: str) -> Iterator[str]:
        """
        Потоковая токенизация текста.

        Возвращает слова по одному.
        """

        word = []

        for char in text.lower():

            if char.isalpha():

                word.append(char)

            else:

                if word:
                    yield "".join(word)
                    word.clear()

        if word:
            yield "".join(word)

    def tokenize_stream(self, stream) -> Iterator[str]:
        """
        Токенизировать текстовый поток.

        Parameters
        ----------
        stream
            Открытый текстовый файл.
        """

        for line in stream:
            yield from self.tokenize_text(line)