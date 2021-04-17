def uuid(n=8):
    return ''.join([str(i) for i in np.random.choice(range(10),n)])

def build_homeSystem(data):

    # form.cleanedplanet_name=Earth&num_planets=6&num_moons=24&home_has_moons=on&starting_pop=7&population_conformity=0.3&population_literacy=0.7&population_aggression=0.5&population_constitution=0.5
    return data