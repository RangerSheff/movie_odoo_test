import logging

from odoo import models, fields, api

from odoo.addons.movie_module.services.movie_service import MovieService

_logger = logging.getLogger(__name__)


class Movie(models.Model):
    _name = "movie.movie"
    _description = "Movie"

    title = fields.Char("Título", required=True, index=True)
    ranking = fields.Float("Ranking", digits=(3, 1))

    @api.model
    def fetch_movie_from_api_cron(self):
        """Method invoked by the cron to import movies."""
        _logger.info("Executing movie import cron job...")
        try:
            movie = MovieService.fetch_new_movie(self.env)
            db_movie = self.create({"title": movie["title"], "ranking": movie["ranking"]})
            _logger.info(f"Movie import cron job: {db_movie.title} created.")
        except Exception as e:
            _logger.error(f"Movie import cron job: error during import - {str(e)}")
