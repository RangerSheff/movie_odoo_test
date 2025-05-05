from odoo import models, fields


class MovieConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    external_api_url = fields.Char(
        "URL del API de Películas", config_parameter="movie_module.external_api_url"
    )
    external_api_key = fields.Char(
        "API Key de Películas", config_parameter="movie_module.external_api_key"
    )
