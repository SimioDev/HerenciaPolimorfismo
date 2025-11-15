# Taller: Herencia y Polimorfismo - Sistema Bancario

## Autor
Nestor Cabrera  
Ingeniería de Software

## Descripción
Implementación de un sistema bancario:
- Herencia: Clases `CuentaAhorro`, `CuentaCorriente` y `CuentaInversion` heredan de `CuentaBancaria`.
- Polimorfismo: Método `procesar_cuentas()` opera sobre diferentes tipos de cuentas.
- Sobrecarga de operadores: `+` para transferencias, `>` para comparar saldos, `__str__` para representación.
- Logging: Registro de todas las transacciones en `transacciones.log`.

## Ejecución

```
python3 test_sistema.py
```