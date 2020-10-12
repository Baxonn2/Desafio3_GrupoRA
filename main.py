import random
import src.parameters.load_instance_file as load
from src.grapher import Grapher


def main():

    load.load_parameters('data.json')
    grapher = Grapher()

    # Agregando entidad infectada
    # Total, enfermos, probabilidad de usar mascarilla, cuarentena
    grapher.add_entities(1000, 5, 0.1, True)

    grapher.run()
    print("Fin del programa")


if __name__ == "__main__":
    random.seed(42)
    main()
