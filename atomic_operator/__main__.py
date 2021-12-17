import fire
from atomic_operator import AtomicOperator

def main():
    atomic_operator = AtomicOperator()
    fire.Fire({
        'run': atomic_operator.run,
        'get_atomics': atomic_operator.get_atomics,
        'help': atomic_operator.help
    })

if __name__ == "__main__":
    main()
