import os
from sentence_transformers import SentenceTransformer

# Используем кросс-язычную модель LaBSE, которая поддерживает многие языки (русский, английский, немецкий, польский, итальянский, французский и др.)
model = SentenceTransformer('sentence-transformers/LaBSE')

def get_embedding(text: str):
    """Возвращает векторное представление текста с использованием LaBSE."""
    return model.encode(text, convert_to_numpy=True)
def create_index_text(manga: dict) -> str:
    title = manga.get("title", {}).get("english") or manga.get("title", {}).get("romaji", "")
    genres = " ".join(manga.get("genres", []))
    tags = " ".join([tag["name"] for tag in manga.get("tags", [])])
    description = manga.get("description", "")
    # Можно добавить обработку отзывов, если они есть:
    reviews = ""
    if manga.get("reviews") and manga["reviews"].get("edges"):
        reviews = " ".join([edge["node"].get("summary", "") for edge in manga["reviews"]["edges"]])
    # Также можно добавить персонажей, если требуется:
    characters = ""
    if manga.get("characters") and manga["characters"].get("edges"):
        characters = " ".join([edge["node"].get("name", {}).get("full", "") for edge in manga["characters"]["edges"]])
    return f"{title} {genres} {tags} {description} {reviews} {characters}"


def create_index_file(data_file: str, index_file: str, dimension: int = 768):
    """
    Создает векторный индекс из данных в data_file, сохраняет его в index_file и возвращает объект индекса.
    """
    import json
    from infrastructure.vector_index import VectorIndex, save_index
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"Data file {data_file} not found!")
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} records from {data_file}.")
    index = VectorIndex(dimension)
    for manga in data:
        text_for_embedding = create_index_text(manga)
        emb = get_embedding(text_for_embedding)
        index.add_item(emb, manga)
    index.build_index()
    save_index(index, index_file)
    print(f"Index saved to {index_file}.")
    return index