"""Contrato REST común para comparar almacenamiento en memoria y MySQL."""
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

FIELDS = ("title", "description", "author")


def crear_api(store):
    app = Flask(__name__)
    app.json.ensure_ascii = False

    @app.errorhandler(HTTPException)
    def http_error(error):
        return jsonify(error=error.description), error.code

    def datos(require_title=False):
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict) or not payload:
            return None
        if set(payload) - set(FIELDS):
            return None
        if require_title and "title" not in payload:
            return None
        if any(not isinstance(v, str) or len(v) > 255 for v in payload.values()):
            return None
        if "title" in payload and not payload["title"].strip():
            return None
        return payload

    @app.get("/health")
    def health():
        store.all()
        return jsonify(status="ok", storage=type(store).__name__)

    @app.get("/books")
    def get_books():
        return jsonify(books=store.all())

    @app.get("/books/<int:book_id>")
    def get_book(book_id):
        book = store.get(book_id)
        return (jsonify(book=book), 200) if book else (jsonify(error="Libro no encontrado"), 404)

    @app.post("/books")
    def create_book():
        payload = datos(require_title=True)
        if payload is None:
            return jsonify(error="Envía un objeto JSON con title no vacío; los campos deben ser textos de máximo 255 caracteres"), 400
        book = store.create({field: payload.get(field, "") for field in FIELDS})
        return jsonify(book=book), 201, {"Location": f"/books/{book['id']}"}

    @app.put("/books/<int:book_id>")
    def update_book(book_id):
        payload = datos()
        if payload is None:
            return jsonify(error="Envía campos válidos en un objeto JSON"), 400
        book = store.update(book_id, payload)
        return (jsonify(book=book), 200) if book else (jsonify(error="Libro no encontrado"), 404)

    @app.delete("/books/<int:book_id>")
    def delete_book(book_id):
        if not store.delete(book_id):
            return jsonify(error="Libro no encontrado"), 404
        return jsonify(result=True)

    return app
