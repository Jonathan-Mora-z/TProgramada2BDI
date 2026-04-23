CREATE PROCEDURE eliminarEmpleado
    @IdEmpleado INT
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1 
        FROM Empleado
        WHERE Id = @IdEmpleado AND EsActivo = 1
    )
    BEGIN
        UPDATE Empleado
        SET EsActivo = 0
        WHERE Id = @IdEmpleado
    END
    ELSE
    BEGIN
        PRINT 'Empleado no existe o ya está inactivo'
    END

END
GO