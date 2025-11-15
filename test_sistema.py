#!/usr/bin/env python3
from sistema_bancario import (
    CuentaAhorro, CuentaCorriente, CuentaInversion,
    procesar_cuentas
)

def menu():
    print("\n" + "="*60)
    print(" SISTEMA BANCARIO - TALLER HERENCIA Y POLIMORFISMO ".center(60))
    print(" Autor: Néstor Cabrera ".center(60))
    print("="*60)
    
    cuentas = {
        "1": CuentaAhorro("001", "Ana Gómez", 1020000),
        "2": CuentaCorriente("002", "Luis Pérez", -50000, 150000),
        "3": CuentaInversion("003", "Carlos Ruiz", 5450000)
    }

    while True:
        print("\n" + " MENÚ PRINCIPAL ".center(60, "-"))
        print("1. Ver cuentas")
        print("2. Depositar")
        print("3. Retirar")
        print("4. Transferir")
        print("5. Procesar mes (intereses + comisiones)")
        print("6. Comparar saldos")
        print("7. Salir")
        print("-" * 60)
        
        op = input("Seleccione opción (1-7): ").strip()
        
        if op == "1":
            print("\n" + " ESTADO ACTUAL DE CUENTAS ".center(60, "="))
            for c in cuentas.values():
                print(f"  → {c}")
            print("=" * 60)
        
        elif op == "2":
            id_c = input("ID cuenta (1, 2 o 3): ").strip()
            if id_c not in cuentas: 
                print("Cuenta no encontrada.")
                continue
            try:
                monto = float(input("Monto a depositar: $"))
                if monto <= 0: raise ValueError("Monto debe ser positivo")
                cuentas[id_c].depositar(monto)
                print(f"Depósito de ${monto:,.0f} exitoso.")
            except ValueError as e:
                print(f"Error: {e}")
        
        elif op == "3":
            id_c = input("ID cuenta (1, 2 o 3): ").strip()
            if id_c not in cuentas: 
                print("Cuenta no encontrada.")
                continue
            try:
                monto = float(input("Monto a retirar: $"))
                cuentas[id_c].retirar(monto)
                print(f"Retiro de ${monto:,.0f} exitoso.")
            except ValueError as e:
                print(f"Error: {e}")

        elif op == "4":
            origen = input("De (1, 2 o 3): ").strip()
            destino = input("A (1, 2 o 3): ").strip()
            if origen not in cuentas or destino not in cuentas:
                print("Cuenta no válida.")
                continue
            try:
                cuentas[origen] + cuentas[destino]
            except Exception as e:
                print(f"Error: {e}")
        
        elif op == "5":
            print("\n" + " APLICANDO OPERACIONES MENSUALES ".center(60, "*"))
            procesar_cuentas(list(cuentas.values()))
            print("*" * 60)
        
        elif op == "6":
            a = input("Cuenta A (1, 2 o 3): ").strip()
            b = input("Cuenta B (1, 2 o 3): ").strip()
            if a not in cuentas or b not in cuentas:
                print("Cuenta no válida.")
                continue
            print(f"\n¿Cuenta {a} > Cuenta {b}? → {cuentas[a] > cuentas[b]}")
        
        elif op == "7":
            print("\n" + " GRACIAS POR USAR EL SISTEMA ".center(60, "="))
            print(" Transacciones guardadas en: transacciones.log ".center(60))
            print("=" * 60 + "\n")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    menu()
