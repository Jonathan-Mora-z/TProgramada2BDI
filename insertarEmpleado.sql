CREATE PROCEDURE insertarEmpleado
@IdPuesto INT,
@ValorDocumentoIdentidad INT,
@Nombre VARCHAR(64),
@FechaContratacion DATE,
@SaldoVacaciones MONEY,
@EsActivo BIT
AS 
BEGIN 

IF EXISTS(SELECT 1 FROM dbo.Empleado WHERE  Nombre = @Nombre)
BEGIN
SELECT -1 AS Resultado, 'Nombre de empleado existente' AS Mensaje; -- mensaje en caso de que exista la persona
RETURN;
END
IF EXISTS(SELECT 1 FROM dbo.Empleado WHERE ValorDocumentoIdentidad = @ValorDocumentoIdentidad)
BEGIN
SELECT -1 AS Resultado, 'Valor de documento de indentidad existente' AS Mensaje;
RETURN;
END

INSERT INTO dbo.Empleado (IdPuesto,ValorDocumentoIdentidad,Nombre,FechaContratación,SaldoVacaciones,EsActivo) 
VALUES (@IdPuesto,@ValorDocumentoIdentidad,@Nombre,@FechaContratacion,@SaldoVacaciones,@EsActivo); 
SELECT 1 AS Resultado, 'Exito al insertar al empleado' AS Mensaje; -- Mensaje en caso de exito
END