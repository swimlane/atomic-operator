import fire
from atomic_operator import AtomicOperator

def main():
    fire.Fire({
        'run': AtomicOperator().run
    })

if __name__ == "__main__":
    main()
