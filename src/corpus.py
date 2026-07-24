from pathlib import Path

from src.tokenizer import Tokenizer


class Corpus:
    """
    Итератор, возвращающий токенизированные предложения.
    """

    def __init__(
        self,
        path: Path,
        tokenizer: Tokenizer,
    ):
        self.path = path
        self.tokenizer = tokenizer

    def __iter__(self):
        with self.path.open(encoding="utf-8") as file:
            for line in file:
                tokens = self.tokenizer.tokenize(line)

                if tokens:
                    yield tokens