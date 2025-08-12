USE tienda_enlinea;

-- 1. Top 3 productos más vendidos por unidades
SELECT p.nombre, SUM(dp.cantidad) AS total_vendido
FROM detalle_pedido dp
JOIN productos p ON dp.producto_id = p.id
GROUP BY p.nombre
ORDER BY total_vendido DESC
LIMIT 3;

-- 2. Ingresos por categoría en el último trimestre
SELECT c.nombre AS categoria, SUM(dp.cantidad * dp.precio_unitario) AS ingresos
FROM detalle_pedido dp
JOIN productos p ON dp.producto_id = p.id
JOIN categorias c ON p.categoria_id = c.id
JOIN pedidos pe ON dp.pedido_id = pe.id
WHERE pe.fecha >= CURDATE() - INTERVAL 3 MONTH
GROUP BY c.nombre;

-- 3. Clientes sin compras en los últimos 60 días
SELECT cl.nombre, cl.email
FROM clientes cl
LEFT JOIN pedidos pe ON cl.id = pe.cliente_id AND pe.fecha >= CURDATE() - INTERVAL 60 DAY
WHERE pe.id IS NULL;

-- 4. Ticket promedio (valor promedio por orden pagada)
SELECT AVG(monto) AS ticket_promedio
FROM pagos;

-- 5. Tasa de cancelación de pedidos
SELECT 
    (SUM(CASE WHEN estado = 'cancelado' THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS tasa_cancelacion
FROM pedidos;

-- 6. Órdenes con inconsistencia en pagos
SELECT pe.id, pe.estado
FROM pedidos pe
LEFT JOIN pagos pa ON pe.id = pa.pedido_id
WHERE pe.estado = 'pendiente' AND pa.id IS NULL;

