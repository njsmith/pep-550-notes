# A sketch for how we expect people to implement context managers to fake
# dynamic scoping on top of PEP 550 v2
_store = ContextItem()

@contextmanager
def set_value(new_value):
    old_value = _store.get()
    _store.set(new_value)
    try:
        yield
    finally:
        _store.set(old_value)

def get_value():
    return _store.get()


# Tricky usage scenario:
def generator():
    # ExecutionContext stack on entry: [{_store: 0}, {}]
    # So this prints 0, as expected:
    print(get_value())
    with set_value(1):
        # ExecutionContext stack here: [{_store: 0}, {_store: 1}]
        # So this prints 1, as expected:
        print(get_value())
    # ExecutionContext stack here: [{_store: 0}, {_store: 0}]
    # So this prints 0, as expected:
    print(get_value())
    yield
    # ExecutionContext stack here: [{_store: 2}, {_store: 0}]
    # So this prints 0, even though we expected 2!
    print(get_value())

g = generator()
with set_value(0):
    next(generator())
with set_value(2):
    next(generator())
