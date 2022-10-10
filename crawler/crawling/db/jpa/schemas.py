from flask_marshmallow import Marshmallow

from flask import Blueprint

app_schemas = Blueprint("schemas", __name__)
ma = Marshmallow(app_schemas)


class DataSchema(ma.Schema):
    class Meta:

        fields = ["info"]


data_schema = DataSchema()
multiple_data_schema = DataSchema(many=True)


class PaginateSchema(ma.Schema):
    class Meta:
        fields = [
            "items",
            "previous_page",
            "next_page",
            "has_previous",
            "has_next",
            "total",
            "pages",
        ]

    items = ma.Nested(multiple_data_schema)


paginate_schema = PaginateSchema()
multiple_paginate_schema = PaginateSchema(many=True)
