CREATE PROCEDURE dbo.borrarEmpleado
@Id INT
AS
BEGIN
	UPDATE Empleado
	SET EsActivo=0
	WHERE Id=@Id
END