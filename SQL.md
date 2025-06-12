# DatabaseGeneratorAi

## Entidades
- productos
- clientes
- empleados
- ventas
- proveedores
- muebles

## Relaciones
- suministros
  -< proveedores
- muebles
  >-< suministros
  >-< empleados
  
- ventas
  >- muebles
  >- clientes
  >- empleados

## Tablas
-- Suministros
CREATE TABLE suministros (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    tipo VARCHAR(50),
    descripcion TEXT
);

CREATE TABLE proveedores (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT
);

CREATE TABLE clientes (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    cedula VARCHAR(20)
);

CREATE TABLE empleados (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    cedula VARCHAR(20),
    tipo VARCHAR(50),
    salario DECIMAL(10, 2)
);

CREATE TABLE muebles (
    id INT PRIMARY KEY,
    tipo VARCHAR(50),
    descripcion TEXT
);

CREATE TABLE muebles_suministros (
    id INT PRIMARY KEY,
    idSuministro INT,
    idMueble INT,
    cantidadSuministro INT,
    FOREIGN KEY (idSuministro) REFERENCES suministros(id),
    FOREIGN KEY (idMueble) REFERENCES muebles(id)
);

CREATE TABLE muebles_empleados (
    id INT PRIMARY KEY,
    idMueble INT,
    idEmpleado INT,
    FOREIGN KEY (idMueble) REFERENCES muebles(id),
    FOREIGN KEY (idEmpleado) REFERENCES empleados(id)
);

CREATE TABLE compra (
    id INT PRIMARY KEY,
    idSuministro INT,
    idProveedor INT,
    cantidad INT,
    precio DECIMAL(10, 2),
    fechaCompra DATE,
    FOREIGN KEY (idSuministro) REFERENCES suministros(id),
    FOREIGN KEY (idProveedor) REFERENCES proveedores(id)
);

CREATE TABLE ventas (
    id INT PRIMARY KEY,
    idMueble INT,
    idEmpleado INT,
    idCliente INT,
    precio DECIMAL(10, 2),
    fechaVenta DATE,
    FOREIGN KEY (idMueble) REFERENCES muebles(id),
    FOREIGN KEY (idEmpleado) REFERENCES empleados(id),
    FOREIGN KEY (idCliente) REFERENCES clientes(id)
);


