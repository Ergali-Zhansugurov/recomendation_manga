import requests

ANI_API_URL = 'https://graphql.anilist.co'

def fetch_manga_by_id(manga_id: int) -> dict:
    query = '''
    query ($id: Int) {
      Media(id: $id, type: MANGA) {
        id
        format
        status
        startDate {
          year
          month
          day
        }
        averageScore
        meanScore
        popularity
        favourites
        source
        genres
        title {
          romaji
          english
          native
        }
        synonyms
        tags {
          name
          rank
        }
        coverImage {
          extraLarge
        }
        characters(sort: ROLE, perPage: 5) {
          edges {
            node {
              id
              name {
                full
              }
              image {
                large
              }
            }
          }
        }
        reviews(perPage: 5) {
          pageInfo {
            total
          }
          edges {
            node {
              id
              summary
              rating
              user {
                name
              }
            }
          }
        }
      }
    }
    '''
    variables = {"id": manga_id}
    response = requests.post(ANI_API_URL, json={'query': query, 'variables': variables})
    result = response.json()
    if 'errors' in result:
        raise Exception(f"AniList API Error: {result['errors']}")
    return result['data']['Media']
def fetch_manga_details(manga_id: int, review_count: int = 10) -> dict:
    """
    Запрашивает подробные данные о манге по ID, включая описание и отзывы.
    :param manga_id: ID манги
    :param review_count: Количество отзывов для запроса
    :return: Словарь с данными манги (description и reviews)
    """
    query = '''
    query ($id: Int) {
      Media(id: $id, type: MANGA) {
        id
        description
        reviews(perPage: %d) {
          pageInfo {
            total
          }
          edges {
            node {
              id
              summary
              rating
              user {
                name
              }
            }
          }
        }
      }
    }
    ''' % review_count
    variables = {"id": manga_id}
    response = requests.post(ANI_API_URL, json={'query': query, 'variables': variables})
    result = response.json()
    if 'errors' in result:
        raise Exception(f"AniList API Error: {result['errors']}")
    return result['data']['Media']
if __name__ == "__main__":
    try:
        manga = fetch_manga_by_id(15125)
        print("Manga data:", manga)
    except Exception as e:
        print("Ошибка:", e)