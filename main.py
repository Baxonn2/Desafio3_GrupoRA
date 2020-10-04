from src.grapher import Grapher

def main():
    grapher = Grapher()

    # Agregando entidad infectada
    grapher.add_entity(infected=True)

    for _ in range(100):
        grapher.add_entity()

    grapher.run()
    print("Fin del programa")

if __name__ == "__main__":
    main()