class ParamPack:
    def __init__(self, population_size, infection_chance, death_chance,
                 sickness_time, reinfection_chance):
        self.population_size = population_size
        self.infection_chance = infection_chance
        self.death_chance = death_chance
        self.sickness_time = sickness_time
        self.reinfection_chance = reinfection_chance

    def pack_data(self):
        return self.population_size, self.infection_chance, self.death_chance, self.sickness_time, self.reinfection_chance
