from interfaz import Interfaz

if __name__ == "__main__":
    import sys
    app = Interfaz()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)
