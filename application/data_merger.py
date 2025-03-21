# application/data_merger.py
import json


def load_data(filename: str):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def merge_manga_data(existing: dict, new: dict) -> dict:
    """Объединяет два словаря с данными манги, заменяя значения непустыми из new."""
    merged = existing.copy()
    for key, value in new.items():
        if value not in (None, "", []):
            merged[key] = value
    return merged


def merge_files(initial_file: str, updated_file: str, additional_file: str, output_file: str):
    data_initial = load_data(initial_file)
    data_updated = load_data(updated_file)
    data_additional = load_data(additional_file)

    merged_dict = {}

    def process_data(data_list):
        for manga in data_list:
            manga_id = str(manga.get("id"))
            if not manga_id:
                continue
            if manga_id in merged_dict:
                merged_dict[manga_id] = merge_manga_data(merged_dict[manga_id], manga)
            else:
                merged_dict[manga_id] = manga

    # Приоритет: сначала базовые данные, затем обновленные, затем дополнительные
    process_data(data_initial)
    process_data(data_updated)
    process_data(data_additional)

    print(f"Всего уникальных манг после объединения: {len(merged_dict)}")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(list(merged_dict.values()), f, ensure_ascii=False, indent=2)
    print(f"Объединённые данные сохранены в файл {output_file}")


if __name__ == "__main__":
    merge_files("initial_data.json", "updated_data.json", "additional_data.json", "merged_data.json")