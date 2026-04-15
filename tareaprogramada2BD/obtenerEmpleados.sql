CREATE PROCEDURE dbo.obtenerEmpleados
AS
BEGIN 
	SELECT id,Nombre,Salario
	FROM dbo.Empleado
	ORDER BY Nombre DESC;
END