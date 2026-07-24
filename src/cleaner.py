"""
Очистка wiki-разметки.
"""

import mwparserfromhell


class WikiCleaner:
    """Преобразует wiki-разметку в обычный текст."""

    def clean(self, text: str) -> str:
        """
        Преобразовать Wikitext в обычный текст.

        Parameters
        ----------
        text : str
            Текст статьи с wiki-разметкой.

        Returns
        -------
        str
            Текст без wiki-разметки.
        """

        code = mwparserfromhell.parse(text)

        return code.strip_code()