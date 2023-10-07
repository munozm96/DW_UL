import sys
sys.path.append('C:/Users/man27/Desktop/AI_test/UL_DW/Scrappers')  # Añade la ruta al directorio donde se encuentra Jumbo_DW.py
import Jumbo_DW  # Importa el script Jumbo_DW.py
import Lider_DW
import Unimarc_DW
import SISA_DW
import Tottus_DW

def main():
    Jumbo_DW.run()
    Lider_DW.run() 
    Unimarc_DW.run()
    SISA_DW.run()
    Tottus_DW.run()

if __name__ == "__main__":
    main()  # Llama a la función main() si este script es el principal
