CREATE PROCEDURE dbo.filtrarEmpleados
@Filtro VARCHAR(50)
AS
BEGIN
	SELECT e.Id,e.ValorDocumentoIdentidad,e.Nombre,e.FechaContratación,e.SaldoVacaciones,e.EsActivo,p.Nombre AS Puesto
	FROM dbo.Empleado e 
	INNER JOIN Puesto p ON e.IdPuesto = p.Id
	WHERE (@Filtro is NULL OR e.Nombre LIKE'%'+@Filtro+'%'
	OR CAST(e.ValorDocumentoIdentidad AS VARCHAR) LIKE'%'+@Filtro+'%')
END