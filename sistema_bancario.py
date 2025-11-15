from abc import ABC, abstractmethod
from datetime import datetime
import logging
from typing import List

logging.basicConfig(
    filename='transacciones.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class CuentaBancaria(ABC):
    """Clase abstracta base para todas las cuentas bancarias."""
    
    def __init__(self, numero_cuenta: str, titular: str, saldo: float = 0.0):
        self._numero_cuenta = numero_cuenta
        self._titular = titular
        self._saldo = saldo
        self._historial = []

    @property
    def numero_cuenta(self) -> str:
        return self._numero_cuenta

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, monto: float) -> None:
        """Deposita dinero en la cuenta."""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self._saldo += monto
        self._registrar(f"Depósito: +${monto:,.0f}")

    def retirar(self, monto: float) -> None:
        """Retira dinero (sin sobregiro en clase base)."""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > self._saldo:
            raise ValueError("Fondos insuficientes")
        self._saldo -= monto
        self._registrar(f"Retiro: -${monto:,.0f}")

    def _registrar(self, accion: str):
        """Registra acción en log y historial."""
        mensaje = f"Cuenta {self._numero_cuenta} ({self._titular}) - {accion} → Saldo: ${self._saldo:,.0f}"
        self._historial.append(f"[{datetime.now().strftime('%H:%M:%S')}] {accion}")
        logging.info(mensaje)

    @abstractmethod
    def calcular_interes(self) -> float:
        """Calcula interés/rendimiento mensual."""
        pass

    @abstractmethod
    def aplicar_comision(self) -> None:
        """Aplica comisión mensual."""
        pass

    # Sobrecarga de operadores
    def __add__(self, other):
        """Transferencia: cuenta1 + cuenta2 transfiere de 1 a 2"""
        if not isinstance(other, CuentaBancaria):
            raise TypeError("Solo se pueden sumar cuentas")
        try:
            monto = float(input(f"¿Cuánto transferir de {self._numero_cuenta} a {other._numero_cuenta}? $"))
            if monto <= 0:
                print("Monto inválido. Operación cancelada.")
                return self
            self.retirar(monto)
            other.depositar(monto)
            logging.info(f"Transferencia: ${monto:,.0f} de {self._numero_cuenta} → {other._numero_cuenta}")
            print(f"Transferencia de ${monto:,.0f} exitosa.")
        except ValueError as e:
            print(f"Error: {e}")
        return self

    def __gt__(self, other) -> bool:
        """Compara saldos"""
        if not isinstance(other, CuentaBancaria):
            return NotImplemented
        return self._saldo > other._saldo

    def __str__(self) -> str:
        return f"{self.__class__.__name__}-{self._numero_cuenta}: Saldo: ${self._saldo:,.0f}"

class CuentaAhorro(CuentaBancaria):
    """Cuenta de ahorros con 2% interés anual."""
    TASA_INTERES_ANUAL = 0.02

    def calcular_interes(self) -> float:
        interes = self._saldo * self.TASA_INTERES_ANUAL / 12
        if interes > 0:
            self._saldo += interes
            self._registrar(f"Interés ganado: +${interes:,.0f}")
        return interes

    def aplicar_comision(self) -> None:
        pass  # Sin comisión

    def __str__(self) -> str:
        return super().__str__() + f" (Interés: 2%)"

class CuentaCorriente(CuentaBancaria):
    """Cuenta corriente con sobregiro y comisión."""
    
    def __init__(self, numero_cuenta: str, titular: str, saldo: float = 0.0,
                 limite_sobregiro: float = 200000.0, comision: float = 8000.0):
        super().__init__(numero_cuenta, titular, saldo)
        self._limite_sobregiro = limite_sobregiro
        self._comision = comision

    def retirar(self, monto: float) -> None:
        if monto <= 0:
            raise ValueError("Monto inválido")
        if monto > (self._saldo + self._limite_sobregiro):
            raise ValueError(f"Sobregiro excedido. Límite: ${self._limite_sobregiro:,.0f}")
        self._saldo -= monto
        self._registrar(f"Retiro (sobregiro permitido): -${monto:,.0f}")

    def calcular_interes(self) -> float:
        """Cuenta corriente no genera interés."""
        return 0.0

    def aplicar_comision(self) -> None:
        if self._saldo > 0:
            self._saldo -= self._comision
            self._registrar(f"Comisión mantenimiento: -${self._comision:,.0f}")

    def __str__(self) -> str:
        sobregiro = max(0, -self._saldo)
        return super().__str__() + f" (Sobregiro usado: ${sobregiro:,.0f})"

class CuentaInversion(CuentaBancaria):
    """Cuenta de inversión con rendimiento variable."""
    
    def __init__(self, numero_cuenta: str, titular: str, saldo: float = 0.0,
                 rendimiento_anual: float = 0.085):
        super().__init__(numero_cuenta, titular, saldo)
        self._rendimiento_anual = rendimiento_anual

    def calcular_interes(self) -> float:
        rendimiento = self._saldo * self._rendimiento_anual / 12
        if rendimiento > 0:
            self._saldo += rendimiento
            self._registrar(f"Rendimiento inversión: +${rendimiento:,.0f}")
        return rendimiento

    def aplicar_comision(self) -> None:
        pass

    def __str__(self) -> str:
        return super().__str__() + f" (Rendimiento: {self._rendimiento_anual*100:.1f}%)"

def procesar_cuentas(cuentas: List[CuentaBancaria]):
    """Aplica operaciones mensuales a todas las cuentas (polimorfismo)."""
    print("\n" + "="*60)
    print("PROCESANDO CUENTAS MENSUALES".center(60))
    print("="*60)
    for cuenta in cuentas:
        cuenta.aplicar_comision()
        cuenta.calcular_interes()
        print("  →", cuenta)
    print("="*60 + "\n")
