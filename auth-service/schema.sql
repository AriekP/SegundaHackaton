
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    correo VARCHAR(100) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    cliente_id INT
);

CREATE TABLE roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE usuarios_roles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    rol_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (rol_id) REFERENCES roles(id)
);
