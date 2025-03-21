# application/services.py
from langdetect import detect
from infrastructure.translator import translate_text
from infrastructure.vector_index import VectorIndex
from infrastructure.embedding import get_embedding

def build_index_from_data(mangas: list) -> VectorIndex:
    """
    Строит векторный индекс на основе списка данных о мангах.
    Для каждой манги используется:
      - Название (title.romaji или title.synonyms)
      - Жанры и теги
    """
    index = VectorIndex(dimension=384)
    for manga in mangas:
        try:
            title = manga["title"].get("romaji") or manga["title"].get("synonyms", "")
            genres = " ".join(manga.get("genres", []))
            tags = " ".join([tag["name"] for tag in manga.get("tags", [])])
            text_for_embedding = f"{title} {genres} {tags}"
            embedding = get_embedding(text_for_embedding)
            index.add_item(embedding, manga)
        except Exception as e:
            print(f"Ошибка при обработке манги с ID {manga.get('id')}: {e}")
    if not index.embeddings:
        raise ValueError("Нет эмбеддингов для построения индекса.")
    index.build_index()
    return index

def process_query(query: str) -> str:
    """
    Определяет язык запроса и, если он не на английском, переводит его.
    """
    try:
        return translate_text(query, dest_lang="en")
    except Exception:
        return query

def search_manga(query: str, index: VectorIndex, k: int = 5):
    """
    Обрабатывает запрос: переводит (если нужно), генерирует эмбеддинг и ищет в индексе.
    """
    processed_query = process_query(query)
    query_embedding = get_embedding(processed_query)
    return index.search(query_embedding, k)

