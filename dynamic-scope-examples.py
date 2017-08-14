import sys

print("no exceptions in progress:", sys.exc_info())
try:
    raise ValueError
except:
    # exc_info contains the ValueError
    print("inside except: block:", sys.exc_info())
# exc_info is (None, None, None)
print("outside except: block:", sys.exc_info())


def print_exc_info():
    print("in subroutine:", sys.exc_info())

try:
    raise ValueError
except:
    print_exc_info()


try:
    raise ValueError
except:
    # exc_info contains the ValueError
    print("single-nested:", sys.exc_info())
    try:
        raise KeyError
    except:
        # exc_info contains the KeyError
        print("double-nested:", sys.exc_info())
    # exc_info contains the ValueError again
    print("single-nested again:", sys.exc_info())


print("\n--- Example: entering a generator from an except: block ---\n")

def gen():
    while True:
        print("inside gen:", sys.exc_info())
        yield

g = gen()
try:
    raise ValueError
except:
    next(g)

next(g)

try:
    raise KeyError
except:
    next(g)

################################################################

print("\n--- Example: entering a generator's except: block ---\n")

def gen():
    try:
        raise RuntimeError("raise inside gen")
    except:
        while True:
            print("inside gen:", sys.exc_info())
            yield
g = gen()

print("outside gen:", sys.exc_info())
next(g)

try:
    raise ValueError
except:
    print("\noutside gen:", sys.exc_info())
    next(g)

################################################################

print("\n---\n")

try:
    raise ValueError
except:
    print("single-nested:", sys.exc_info())
    try:
        raise KeyError
    except:
        print("double-nested:", sys.exc_info())
    print("single-nested again:", sys.exc_info())


# Factor out the last part into a generator
def gen():
    try:
        raise KeyError
    except:
        yield
        print("double-nested:", sys.exc_info())
    print("single-nested again:", sys.exc_info())

g = gen()
next(g)
try:
    raise ValueError
except:
    print("single-nested:", sys.exc_info())
    next(g, None)
