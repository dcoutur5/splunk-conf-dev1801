import json
from functools import wraps

from flask import Response, jsonify, request

from jsonschema import Draft7Validator


class MissingAllOps(Exception):
    def __init__(self, missing):
        self.missing = missing


class required(object):
    """
    This class can be used as a decorator on a Flask route.

    Its expects a schema in the format described by JSON Schema Draft 7
    https://json-schema.org/understanding-json-schema/index.html
    """

    def __init__(self, schema):
        Draft7Validator.check_schema(schema)
        self.validator = Draft7Validator(schema=schema)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.content_type != "application/json":
                return (
                    jsonify("This endpoint only accepts 'application/json' bodies"),
                    400,
                )
            body = request.get_json()
            if self.validator.is_valid(body):
                try:
                    return func(*args, body=body, **kwargs)
                except MissingAllOps as err:
                    missing = (f"`{field}`" for field in err.missing)
                    return jsonify({
                        "status": "err",
                        "msg": "Invalid request body",
                        "errors": [f"One of {' or '.join(missing)} is required"],
                        "expected": {
                            "input": self.validator.schema,
                            "format": "Defined by JSON Schema 7 | https://json-schema.org/understanding-json-schema/index.html"
                        },
                    }), 400
            error_messages = [
                error.message for error in self.validator.iter_errors(body)]
            return jsonify({
                "status": "err",
                "msg": "Invalid request body",
                "errors": error_messages,
                "expected": {
                    "input": self.validator.schema,
                    "format": "Defined by JSON Schema 7 | https://json-schema.org/understanding-json-schema/index.html"
                },
            }), 400
        return wrapper
