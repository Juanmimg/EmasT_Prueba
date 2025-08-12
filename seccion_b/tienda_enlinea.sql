-- Crear base de datos y usarla
CREATE DATABASE tienda_enlinea;
USE tienda_enlinea;

-- Tabla de clientes
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    fecha_registro DATETIME
);

-- Tabla de categorías
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50)
);

-- Tabla de productos
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    categoria_id INT,
    precio DECIMAL(10,2),
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Tabla de pedidos
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    estado VARCHAR(20),
    fecha DATETIME,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

-- Tabla de detalles del pedido
CREATE TABLE detalle_pedido (
    pedido_id INT,
    producto_id INT,
    cantidad INT,
    precio_unitario DECIMAL(10,2),
    PRIMARY KEY (pedido_id, producto_id),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

-- Tabla de pagos
CREATE TABLE pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT,
    monto DECIMAL(10,2),
    estado VARCHAR(20),
    metodo VARCHAR(20),
    fecha_pago DATETIME,
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
);

-- Categorías
INSERT INTO categorias (nombre) VALUES
('Almacenamiento'),
('Periféricos'),
('Móviles');

-- Clientes
INSERT INTO clientes (nombre, email, fecha_registro) VALUES
('María', 'maria@example.com', '2025-06-01'),
('Juan', 'juan@example.com', '2025-06-15'),
('Pedro', 'pedro@example.com', '2025-07-01'),
('Laura', 'laura@example.com', '2025-08-01');

-- Productos
INSERT INTO productos (nombre, categoria_id, precio) VALUES
('USB 32GB', 1, 25.00),
('Mouse óptico', 2, 15.50),
('Celular A1', 3, 450.00),
('Teclado mecánico', 2, 75.00),
('Disco SSD 512GB', 1, 120.00);

INSERT INTO pedidos (cliente_id, estado, fecha) VALUES
(1, 'pagado', '2025-08-01'),
(2, 'pagado', '2025-07-20'),
(3, 'cancelado', '2025-06-10'),
(4, 'pendiente', '2025-08-05'),
(1, 'pagado', '2025-05-15');

-- Pagos
INSERT INTO pagos (pedido_id, monto, fecha_pago) VALUES
(1, 25.00, '2025-08-01'),
(2, 465.50, '2025-07-20'),
(5, 75.00, '2025-05-15');

INSERT INTO detalle_pedido (pedido_id, producto_id, cantidad, precio_unitario) VALUES
(1, 1, 2, 25.00),
(1, 2, 1, 15.50), 
(2, 3, 1, 450.00), 
(2, 4, 1, 75.00),  
(5, 5, 1, 120.00);  