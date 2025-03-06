import nbtlib
import sys

# Ruta del archivo .dat del jugador (modifica con la ruta correcta)
uuid_file = "nuevo/a6abd3d4-b25e-3ce3-9ed2-c183362a62d8.dat"

try:
    # Cargar archivo NBT
    player_data = nbtlib.load(uuid_file)

    # Mostrar toda la información en formato estructurado
    print("Información completa del jugador:")
    print(player_data)

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en {uuid_file}")
    print("Verifica que la ruta sea correcta y que el UUID sea el correcto.")
except Exception as e:
    print(f"Ocurrió un error: {e}")
