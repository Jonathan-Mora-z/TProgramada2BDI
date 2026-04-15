CREATE PROCEDURE InsertarEmpleado
@Nombre VARCHAR(64),
@Salario MONEY
AS 
BEGIN 

IF EXISTS(SELECT 1 FROM dbo.Empleado WHERE  Nombre = @Nombre)
BEGIN
SELECT -1 AS Resultado, 'Nombre de empleado existente' AS Mensaje; -- mensaje en caso de que exista la persona
RETURN;
END

INSERT INTO dbo.Empleado (Nombre, Salario) VALUES (@Nombre, @Salario); 
SELECT 1 AS Resultado, 'Exito al insertar al empleado' AS Mensaje; -- Mensaje en caso de exito
END
