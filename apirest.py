"""Práctica REST: los cambios viven únicamente en la memoria del proceso."""
from threading import RLock
from api_comun import crear_api


class MemoryStore:
    def __init__(self):
        self.books = {
            1: dict(id=1, title="La hojarasca", description="Good one", author="Gabo"),
            2: dict(id=2, title="El coronel no tiene quien le escriba", description="Interesting", author="Gabo"),
        }
        self.next_id = 3
        self.lock = RLock()

    def all(self):
        with self.lock:
            return [dict(book) for book in self.books.values()]

    def get(self, book_id):
        with self.lock:
            book = self.books.get(book_id)
            return dict(book) if book else None

    def create(self, fields):
        with self.lock:
            book = dict(fields, id=self.next_id)
            self.books[self.next_id] = book
            self.next_id += 1
            return dict(book)

    def update(self, book_id, fields):
        with self.lock:
            if book_id not in self.books:
                return None
            self.books[book_id].update(fields)
            return dict(self.books[book_id])

    def delete(self, book_id):
        with self.lock:
            return self.books.pop(book_id, None) is not None


app = crear_api(MemoryStore())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
