# tests/test_data_generator.py
import json
import random

def generate_dummy_manga(id_num):
    return {
        "id": id_num,
        "format": random.choice(["MANGA", "NOVEL"]),
        "status": random.choice(["FINISHED", "ONGOING"]),
        "startDate": {"year": random.randint(1980, 2025), "month": random.randint(1, 12), "day": random.randint(1, 28)},
        "averageScore": random.randint(50, 100),
        "meanScore": random.randint(50, 100),
        "popularity": random.randint(1000, 100000),
        "favourites": random.randint(100, 10000),
        "source": random.choice(["Original", "Adaptation"]),
        "genres": random.sample(["Action", "Romance", "Adventure", "Fantasy", "Drama"], k=2),
        "title": {
            "romaji": f"Manga Title {id_num}",
            "english": f"English Title {id_num}",
            "native": f"Native Title {id_num}"
        },
        "synonyms": [f"Synonym {id_num}"],
        "tags": [{"name": random.choice(["Boys' Love", "Girls' Love", "Seinen", "Shounen"]), "rank": random.randint(1, 5)}],
        "coverImage": {"extraLarge": f"https://example.com/cover/{id_num}.jpg"},
        "characters": [],
        "reviews": {"pageInfo": {"total": random.randint(0, 10)}, "edges": []}
    }

def generate_test_data(n=3000, output_file="tests/test_data.json"):
    data = [generate_dummy_manga(i) for i in range(1, n + 1)]
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Сгенерировано {n} записей в файл {output_file}")

if __name__ == "__main__":
    generate_test_data()
