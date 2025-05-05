import requests


class MovieAPIAdapter:
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def fetch_movie(self):
        """Calls the external API and returns a list of movies (dictionaries)."""
        params = {"api_key": self.api_key}
        resp = requests.get(self.base_url, params=params)
        if resp.status_code != 200:
            raise Exception(f"HTTP {resp.status_code}: Error querying movie API")
        movie = resp.json()
        title = movie.get("movie_title")
        ranking = movie.get("ranking_movie")
        if not (title and ranking):
            raise Exception("No movie data found")
        return {"title": title, "ranking": ranking}
