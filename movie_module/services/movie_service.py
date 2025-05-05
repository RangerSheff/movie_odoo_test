# from odoo.tools import safe_eval

from odoo.http import request

from .movie_api_adapter import MovieAPIAdapter


class MovieService:
    @classmethod
    def fetch_new_movie(cls, env):
        """Gets new movies from the external API through the adapter."""
        Param = env["ir.config_parameter"].sudo()
        api_url = Param.get_param("movie_module.external_api_url")
        api_key = Param.get_param("movie_module.external_api_key")
        adapter = MovieAPIAdapter(api_url, api_key)
        movie = adapter.fetch_movie()
        return movie

    @classmethod
    def top_movies(cls):
        """Retrieves the top movies list."""
        movies = (
            request.env["movie.movie"]
            .sudo()
            .search(
                [],
                order="ranking desc",
                limit=10,
            )
        )
        return [{"id": m.id, "title": m.title, "ranking": m.ranking} for m in movies]
