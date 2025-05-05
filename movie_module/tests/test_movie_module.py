import requests
from odoo.tests.common import TransactionCase

from odoo.addons.movie_module.services.movie_service import MovieService


class DummyResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data


class TestMovie(TransactionCase):
    def test_movie_creation(self):
        movie = self.env["movie.movie"].create(
            {"title": "Nueva Película", "ranking": 9.5}
        )
        self.assertTrue(movie.id, "La película no fue creada correctamente (sin ID).")
        self.assertEqual(
            movie.title, "Nueva Película", "El título de la película no coincide."
        )
        self.assertEqual(movie.ranking, 9.5, "El ranking de la película no coincide.")

    def test_fetch_movie_from_api(self):
        dummy_data = {
            "movie_title": "Dummy Movie",
            "ranking_movie": 8.5,
        }
        original_get = requests.get
        requests.get = lambda url, params=None, **kwargs: DummyResponse(dummy_data)

        try:
            movie = MovieService.fetch_new_movie(self.env)
            self.assertIn("title", movie)
            self.assertIn("ranking", movie)
        finally:
            requests.get = original_get

    def test_top_movies_endpoint(self):
        for i in range(1, 16):
            self.env["movie.movie"].create({"title": f"Pelicula {i}", "ranking": i})
        top_movies = self.env["movie.movie"].search([], order="ranking desc", limit=10)
        result = [
            {"id": movie.id, "title": movie.title, "ranking": movie.ranking}
            for movie in top_movies
        ]
        for movie_data in result:
            self.assertIn(
                "id", movie_data, "Falta 'id' en un elemento de la respuesta."
            )
            self.assertIn(
                "title", movie_data, "Falta 'title' en un elemento de la respuesta."
            )
            self.assertIn(
                "ranking", movie_data, "Falta 'ranking' en un elemento de la respuesta."
            )
