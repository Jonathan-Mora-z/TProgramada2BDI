CREATE PROCEDURE dbo.actualizarEmpleado
@Id INT,
@Nombre VARCHAR(64),
@ValorDocIden INT,
@IdPuesto INT
AS
BEGIN
	UPDATE Empleado
	SET IdPuesto=@IdPuesto,
	ValorDocumentoIdentidad=@ValorDocIden,
	Nombre=@Nombre
	WHERE Id=@Id
END