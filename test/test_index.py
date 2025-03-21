# tests/test_index.py
import json
from infrastructure.embedding import get_embedding
from infrastructure.vector_index import VectorIndex

def load_test_data(file_path="test/test_data.json"):
    import json
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_test_index(data):
    index = VectorIndex(dimension=768)  # Размерность LaBSE
    for manga in data:
        # Формируем текст для эмбеддинга
        title = manga.get("title", {}).get("english") or manga.get("title", {}).get("romaji", "")
        genres = " ".join(manga.get("genres", []))
        tags = " ".join([tag["name"] for tag in manga.get("tags", [])])
        text_for_embedding = f"{title} {genres} {tags}"
        emb = get_embedding(text_for_embedding)
        index.add_item(emb, manga)
    index.build_index()
    return index

def test_search(index: VectorIndex, query: str):
    emb = get_embedding(query)
    results = index.search(emb, k=5)
    print(f"Результаты для запроса '{query}':")
    for manga, score in results:
        title = manga.get("title", {}).get("english") or manga.get("title", {}).get("romaji", "Без названия")
        print(f" - {title} (Score: {score:.2f})")

if __name__ == "__main__":
    data = load_test_data()
    print(f"Загружено тестовых записей: {len(data)}")
    index = build_test_index(data)
    test_search(index, "love")
    test_search(index, "приключения")
