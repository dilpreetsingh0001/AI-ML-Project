import imdb
import csv
import os
from http.client import IncompleteRead
from time import sleep

ia = imdb.IMDb()

def search_movie(title, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            movies = ia.search_movie(title.strip())
            if movies:
                movie_id = movies[0].movieID
                movie = ia.get_movie(movie_id)
                return movie
            else:
                print(f"No movies found with the title: {title}")
                return None
        except IncompleteRead as e:
            print(f"IncompleteRead error encountered while searching for '{title}': {e}. Retrying...")
            sleep(2)  # Wait a couple of seconds before retrying
            retries += 1
        except Exception as e:
            print(f"An error occurred while fetching data for '{title}': {e}. No retries left.")
            return None
    print("Failed to fetch data after several retries.")
    return None

def print_temp(movie):
    if movie:
        temp = {
            'ID': movie.movieID,
            'Title': movie['title'] if 'title' in movie else 'N/A',
            'Year': movie['year'] if 'year' in movie else 'N/A',
            'Rating': movie['rating'] if 'rating' in movie else 'N/A',
            'Directors': ', '.join(director['name'] for director in movie.get('directors', [])),
            'Actors': ', '.join(actor['name'] for actor in movie.get('cast', [])[:5]),
            'Type': movie['kind'] if 'kind' in movie else 'N/A',
            'Genres': ', '.join(movie['genres'] if 'genres' in movie else []),
            'Countries': ', '.join(movie['countries'] if 'countries' in movie else []),
            'Duration': movie['runtime'][0] if 'runtime' in movie and movie['runtime'] else 'N/A',
            'Description': movie['plot outline'] if 'plot outline' in movie else 'N/A'
        }

        with open('movie_details.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(temp.values())
        return True
    return False

if __name__ == "__main__":
    if not os.path.isfile('movie_details.csv'):
        with open('movie_details.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            headers = ['ID', 'Title', 'Year', 'Rating', 'Directors', 'Actors', 'Type', 'Genres', 'Countries', 'Duration', 'Description']
            writer.writerow(headers)

    with open('hindi.txt', 'r', encoding='utf-8') as file:
        titles = file.readlines()

    unprocessed_titles = []
    for title in titles:
        title = title.strip()  # Remove any extra spaces or newline characters
        if title:  # Only process non-empty titles
            movie = search_movie(title)
            if not print_temp(movie):  # If printing to CSV fails, add to unprocessed
                unprocessed_titles.append(title + '\n')

    # Rewrite the hindi.txt file with only unprocessed titles
    with open('hindi.txt', 'w', encoding='utf-8') as file:
        file.writelines(unprocessed_titles)