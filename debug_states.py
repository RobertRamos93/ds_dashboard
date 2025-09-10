# debug_states.py
import pandas as pd

# Datos de ejemplo basados en tu log
sample_data = pd.DataFrame({
    'estado': ['CDMX', 'CHIHUAHUA', 'COLIMA', 'MICHOAC\xa0N', 'TAMAULIPAS', 'TIJUANA', 'VERACRUZ'],
    'importe': [990217.51, 150000, 80000, 120000, 200000, 300000, 180000]
})

def main():
    # Importar la función de debug
    try:
        from geo_map import debug_state_names
        debug_state_names(sample_data)
    except ImportError:
        print("❌ No se pudo importar geo_map. Asegúrate de tener el archivo actualizado.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()