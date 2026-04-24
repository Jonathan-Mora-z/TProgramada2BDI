CREATE PROCEDURE dbo.consultarPuestos
AS
BEGIN
	SET NOCOUNT ON;
	SELECT Id,Nombre,SalarioxHora
	FROM Puesto
END

		