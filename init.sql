-- Ejecutar sobre la base aislada rest_equipo. No borra registros existentes.
CREATE TABLE IF NOT EXISTS books (
 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 title VARCHAR(255) NOT NULL,
 description VARCHAR(255) NOT NULL DEFAULT '',
 author VARCHAR(255) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
INSERT INTO books (title, description, author)
SELECT 'La hojarasca', 'Good one', 'Gabo'
WHERE NOT EXISTS (SELECT 1 FROM books WHERE title='La hojarasca');
INSERT INTO books (title, description, author)
SELECT 'El coronel no tiene quien le escriba', 'Interesting', 'Gabo'
WHERE NOT EXISTS (SELECT 1 FROM books WHERE title='El coronel no tiene quien le escriba');
