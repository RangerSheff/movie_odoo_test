import json

from odoo import http
from odoo.http import Response

from odoo.addons.movie_module.services.movie_service import MovieService


class MovieController(http.Controller):
    @http.route(
        "/api/top_movies",
        auth="public",
        type="http",
        methods=["GET"],
        csrf=False,
    )
    def get_top_movies(self, **kwargs):
        result = MovieService.top_movies()
        return Response(
            json.dumps(result),
            headers={"Content-Type": "application/json"},
        )
