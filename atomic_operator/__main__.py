import fire
from atomic_operator import AtomicOperator

def main():
    fire.Fire({
        'run': AtomicOperator().run,
        'get_atomics': AtomicOperator().get_atomics
    })

if __name__ == "__main__":
    main()
