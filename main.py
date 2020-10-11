import random


def main():
    from src.grapher import Grapher
    grapher = Grapher()

    # Agregando entidad infectada
    # Total, enfermos, probabilidad de usar mascarilla
    grapher.add_entities(1000, 5, 0.1, False)

    grapher.run()
    print("Fin del programa")


if __name__ == "__main__":
    random.seed(42)
    main()
