CREATE PROCEDURE listarMovimientos
    @IdEmpleado INT
AS
BEGIN
    SET NOCOUNT ON;

    SELECT ValorDocumentoIdentidad, Nombre, SaldoVacaciones FROM Empleado WHERE Id = @IdEmpleado

    SELECT 
        m.Fecha,
        tm.Nombre AS TipoMovimiento,
        m.Monto,
        m.NuevoSaldo,
        u.Username AS Usuario,
        m.PostInIP,
        m.PostTime
    FROM Movimiento m
    INNER JOIN TipoMovimiento tm ON m.IdTipoMovimiento = tm.Id
    INNER JOIN Usuario u ON m.IdUsuario = u.Id
    WHERE m.IdEmpleado = @IdEmpleado
    ORDER BY m.Fecha DESC

END
GO