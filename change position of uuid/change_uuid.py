import nbtlib
import os

# Ruta original del archivo .dat del jugador
ruta_original = "C:/Users/kiridepapel/Desktop/New folder/playerdata/14c379e2-ffee-359e-a49b-842d422169f9.dat"

# Nueva carpeta donde guardarás el archivo modificado
nueva_carpeta = "C:/Users/kiridepapel/Desktop/New folder/nuevo/"

# Asegurar que la carpeta existe, si no, crearla
os.makedirs(nueva_carpeta, exist_ok=True)

# Nueva ruta del archivo modificado
ruta_nueva = os.path.join(nueva_carpeta, "14c379e2-ffee-359e-a49b-842d422169f9.dat")

# Nueva posición que deseas establecer (X=100, Y=100, Z=0)
nueva_pos = [100.0, 100.0, 0.0]  # En formato float

try:
    # Cargar el archivo NBT
    player_data = nbtlib.load(ruta_original)

    # Modificar la posición del jugador
    player_data["Pos"] = nbtlib.List[nbtlib.Double](nueva_pos)

    # Guardar el archivo en la nueva carpeta
    player_data.save(ruta_nueva)

    print("La posición del jugador ha sido cambiada exitosamente.")
    print(f"Nueva posición: X={nueva_pos[0]}, Y={nueva_pos[1]}, Z={nueva_pos[2]}")
    print(f"Archivo guardado en: {ruta_nueva}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo en {ruta_original}")
except Exception as e:
    print(f"Ocurrió un error: {e}")
