class PowerGenerator:
    def __init__(self, a, n):
        self.a = a
        self.n = n
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.n:
            raise StopIteration

        result = self.a ** self.current
        self.current += 1
        return result

gen = PowerGenerator(a=2, n=6)

for value in gen:
    print(value)
