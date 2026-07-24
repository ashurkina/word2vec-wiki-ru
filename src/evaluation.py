from dataclasses import dataclass

import pandas as pd


SEMANTIC_CATEGORIES = {
    "capital-common-countries",
    "capital-world",
    "city-in-state",
    "currency",
    "family",
}


@dataclass
class EvaluationReport:
    """Отчет об оценке модели."""

    overall_accuracy: float
    by_category: pd.DataFrame
    by_type: pd.DataFrame


class Evaluation:
    """Оценка качества модели Word2Vec."""

    def __init__(self, model, dataset_path: str):
        self.model = model
        self.dataset_path = dataset_path

    def evaluate(self) -> EvaluationReport:
        # оцениваем модель
        overall_accuracy, sections = self.model.wv.evaluate_word_analogies(
            self.dataset_path
        )

        # собираем результаты по категориям
        category_rows = []

        for section in sections:
            category = section["section"].lstrip(": ")

            if category == "Total accuracy":
                continue

            correct = len(section["correct"])
            incorrect = len(section["incorrect"])
            total = correct + incorrect

            category_rows.append(
                {
                    "Тип": (
                        "Semantic"
                        if category in SEMANTIC_CATEGORIES
                        else "Syntactic"
                    ),
                    "Категория": category,
                    "Всего": total,
                    "Правильно": correct,
                    "Неправильно": incorrect,
                    "Accuracy": correct / total if total else 0.0,
                }
            )

        by_category = pd.DataFrame(category_rows)

        # собираем результаты по типам
        type_rows = []

        for analogy_type in ["Semantic", "Syntactic"]:
            subset = by_category[by_category["Тип"] == analogy_type]

            correct = subset["Правильно"].sum()
            incorrect = subset["Неправильно"].sum()
            total = correct + incorrect

            type_rows.append(
                {
                    "Тип": analogy_type,
                    "Всего": total,
                    "Правильно": correct,
                    "Неправильно": incorrect,
                    "Accuracy": correct / total if total else 0.0,
                }
            )

        by_type = pd.DataFrame(type_rows)

        return EvaluationReport(
            overall_accuracy=overall_accuracy,
            by_category=by_category,
            by_type=by_type,
        )