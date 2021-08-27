def build_species(data):
    # More rules here to follow depending on the attribute, however this is a placeholder
    species = {}
    for attr in ['population_conformity', 'population_literacy', 'population_aggression', 'population_constitution']:
        species[attr] = data[attr]
    return species


def build_homeSystem(data):
    pass

