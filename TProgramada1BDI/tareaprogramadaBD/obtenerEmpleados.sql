CREATE PROCEDURE dbo.consultarEmpleados
AS
BEGIN
	SELECT Id,IdPuesto,ValorDocumentoIdentidad,Nombre,FechaContratación,SaldoVacaciones,EsActivo
	FROM dbo.Empleado
END