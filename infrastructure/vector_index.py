import faiss
import numpy as np

class VectorIndex:
    def __init__(self, dimension: int):
        self.dimension = dimension
        # Используем IndexFlatIP для внутреннего произведения (при нормализации – cosine similarity)
        self.index = faiss.IndexFlatIP(dimension)
        self.embeddings = []  # список эмбеддингов
        self.metadata = []    # список метаданных (данные манги)

    def add_item(self, embedding: np.ndarray, metadata: dict):
        norm = np.linalg.norm(embedding)
        if norm != 0:
            embedding = embedding / norm
        self.embeddings.append(embedding)
        self.metadata.append(metadata)

    def build_index(self):
        if self.embeddings:
            embeddings_np = np.vstack(self.embeddings).astype('float32')
            self.index.add(embeddings_np)
        else:
            raise ValueError("Нет эмбеддингов для построения индекса.")

    def search(self, query_embedding: np.ndarray, k: int = 5):
        query_embedding = query_embedding.astype('float32')
        norm = np.linalg.norm(query_embedding)
        if norm != 0:
            query_embedding = query_embedding / norm
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        scores, indices = self.index.search(query_embedding, k)
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.metadata):
                results.append((self.metadata[idx], float(score)))
        return results

def save_index(vector_index: VectorIndex, filepath: str):
    """Сохраняет FAISS индекс из VectorIndex в файл."""
    faiss.write_index(vector_index.index, filepath)

def load_index(filepath: str, dimension: int = 768) -> VectorIndex:
    """Загружает FAISS индекс из файла и возвращает новый VectorIndex.
       Заметим, что FAISS сохраняет только индекс, а не связанные метаданные.
       Для полноты данных метаданные нужно хранить отдельно (например, в all_manga.json)."""
    vi = VectorIndex(dimension)
    vi.index = faiss.read_index(filepath)
    print(f"Index loaded from {filepath}.")
    return vi


