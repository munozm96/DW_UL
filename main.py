import sys
sys.path.append('C:/Users/man27/Desktop/AI_test/UL_DW')  # Añade la ruta al directorio donde se encuentra Jumbo_DW.py
import Jumbo_DW  # Importa el script Jumbo_DW.py
import Lider_DW

def main():
    Jumbo_DW.run()
    Lider_DW.run()   # Ejecuta la función run() definida en Jumbo_DW.py

if __name__ == "__main__":
    main()  # Llama a la función main() si este script es el principal
