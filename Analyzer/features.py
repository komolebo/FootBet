class InputLayer:
    def __init__(self, sideness, fitness, derby, rate):
        self.sideness = sideness
        self.fitness = fitness
        self.derby = derby
        self.rate = rate

    def convert_sideness(self):
        return self.sideness + 1

    def convert_fitness(self):
        return self.fitness + 1

    def convert_derby(self):
        return self.derby + 1

    def convert_rate(self):
        return self.rate + 1

    def convert_to_chance_values(self):  # converts values to vector of [0..1]
        return InputLayer(
            self.convert_sideness(),
            self.convert_fitness(),
            self.convert_derby(),
            self.convert_rate()
        )

