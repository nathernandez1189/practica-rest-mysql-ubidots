"""Práctica REST + MySQL. Configuración mediante variables de entorno."""
import os
import pymysql
from flask import jsonify
from api_comun import crear_api


class MySQLStore:
    def connect(self):
        return pymysql.connect(
            host=os.environ.get("MYSQL_HOST", "127.0.0.1"),
            port=int(os.environ.get("MYSQL_PORT", "3306")),
            user=os.environ.get("MYSQL_USER", "rest_equipo"),
            password=os.environ["MYSQL_PASSWORD"],
            database=os.environ.get("MYSQL_DB", "rest_equipo"),
            charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5, read_timeout=10, write_timeout=10,
        )

    def all(self):
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute("SELECT id, title, description, author FROM books ORDER BY id")
            return cur.fetchall()

    def get(self, book_id):
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM books WHERE id=%s", (book_id,))
            return cur.fetchone()

    def create(self, fields):
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute("INSERT INTO books (title, description, author) VALUES (%s,%s,%s)",
                        (fields["title"], fields["description"], fields["author"]))
            book_id = cur.lastrowid
            conn.commit()
            return dict(fields, id=book_id)

    def update(self, book_id, fields):
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM books WHERE id=%s FOR UPDATE", (book_id,))
            book = cur.fetchone()
            if book is None:
                return None
            book.update(fields)
            cur.execute("UPDATE books SET title=%s, description=%s, author=%s WHERE id=%s",
                        (book["title"], book["description"], book["author"], book_id))
            conn.commit()
            return book

    def delete(self, book_id):
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM books WHERE id=%s", (book_id,))
            deleted = cur.rowcount > 0
            conn.commit()
            return deleted


app = crear_api(MySQLStore())


@app.errorhandler(pymysql.MySQLError)
def database_error(error):
    app.logger.error("Error MySQL de tipo %s", type(error).__name__)
    return jsonify(error="Base de datos no disponible"), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
