'''
Method
1. Heat brood slides to critical temperature -> need to know about of energy required
2. Determine how soon brood cools down to below critical range -> need to know how fast box loses heat
3. Determine amount of energy required to heat back up to critical range -> need to know about energy required

Need to Know
1. Size of frames being used
2. Composition of frames (material, density, specific heat capacity)
3. Insulation

Frame size: 480 * 285 * 35
Assume 10 frames per brood box

480*285*350 -> 0.48*0.285*0.350
'''

#IMPORTS
import matplotlib.pyplot as plt

#DIMENSIONS
INTERNAL_DIMENSIONS = [0.480, 0.285, 0.350]
INTERNAL_SURFACE_AREA = 0.809099
INTERNAL_VOLUME = 0.047879

#TEMPERATURES
CRITICAL_TEMPERATURE = 44.5
CRITICAL_RANGE = 2.5
EXTERNAL_TEMPERATURE = 13.5
BROOD_TEMPERATURE = 35

#MATERIAL PROPERTIES
BEESWAX = [960, 2.2]
AIR = [1.23, 1.006]

#INSULATORS
STYROFOAM = [0.033, 0.1]
AEROGEL = [0.013, 0.1]

#TIME
TREATMENT_TIME = 2

def energy_to_heat(initial_temperature):
    '''
    Return amount of energy [J] needed to raise the temperature of the frames from initial_temperature to the critical temperature.

    Q = m * c * dT
    '''

    difference_in_temperature = CRITICAL_TEMPERATURE - initial_temperature
    mass_of_beeswax = BEESWAX[0] * 0.5 * INTERNAL_VOLUME
    mass_of_air = AIR[0] * 0.5 * INTERNAL_VOLUME
    return mass_of_air * AIR[1] * difference_in_temperature + mass_of_beeswax * BEESWAX[1] * difference_in_temperature

def temperature_given_energy(energy, initial_temperature):
    '''
    Return temperature given external temperature and energy

    Q = m * c * (T - EXTERNAL_TEMPERATURE) -> T = (Q / (m * c)) + EXTERNAL_TEMPERATURE
    '''

    mass_of_beeswax = BEESWAX[0] * 0.5 * INTERNAL_VOLUME
    mass_of_air = AIR[0] * 0.5 * INTERNAL_VOLUME
    return -(energy / (mass_of_air * AIR[1] + mass_of_beeswax * BEESWAX[1])) + initial_temperature

def energy_given_temperature(temperature):
    '''
    Return energy given external temperature and internal temperature

    Q = m * c * dT
    '''
    difference_in_temperature = temperature - EXTERNAL_TEMPERATURE
    mass_of_beeswax = BEESWAX[0] * 0.5 * INTERNAL_VOLUME
    mass_of_air = AIR[0] * 0.5 * INTERNAL_VOLUME
    return mass_of_air * AIR[1] * difference_in_temperature + mass_of_beeswax * BEESWAX[1] * difference_in_temperature

def energy_lost_by_convection(insulation, internal_temperature):
    '''
    Return amount of energy lost per second [W] for box with insulation at internal_temperature

    Q = (h / t) * A * dT
    '''

    difference_in_temperature = internal_temperature - EXTERNAL_TEMPERATURE
    insulation_factor = insulation[0] / insulation[1]
    return insulation_factor * INTERNAL_SURFACE_AREA * difference_in_temperature

def temperature_over_treatment(insulation):
    '''
    Return simulated temperature over treatment span with given insulation
    '''

    temperature = []
    temperature[0] = CRITICAL_TEMPERATURE
    change_in_energy = energy_lost_by_convection(insulation, temperature[0])
    for i in range(0, TREATMENT_TIME * 3600):
        new_temperature = 
        temperature.append(new_temperature)

def time_to_exit_critical_range(insulation):
    '''
    Return time elapsed in seconds after commencing treatment before interior below beyond critical range
    '''
    i = 0
    temperature = temperature_over_treatment(insulation)
    while temperature[i] >= CRITICAL_TEMPERATURE - CRITICAL_RANGE:
        i+=1
    return i

def surface_area(dimensions):
    '''
    Return the surface area of the rectangular prism specified by dimensions.
    '''
    return 2 * (dimensions[0] * dimensions[1] + dimensions[1] * dimensions[2] + dimensions[2] * dimensions[0])

def volume(dimensions):
    '''
    Return the volume of the rectangular prism specified by dimensions.
    '''
    return dimensions[0]*dimensions[1]*dimensions[2]

if __name__ == "__main__":
    temperature = temperature_over_treatment(STYROFOAM)
    time = []
    for i in range(0, TREATMENT_TIME * 3600):
        time.append(i)


    plt.plot(time, temperature)
    plt.axhline(CRITICAL_TEMPERATURE - CRITICAL_RANGE, ls = "--")
    plt.axhline(CRITICAL_TEMPERATURE + CRITICAL_RANGE, ls = "--")
    plt.show()

    print(time_to_exit_critical_range(STYROFOAM))
    
    '''
    for i in range(0, time_to_exit_critical_range(STYROFOAM)):
        print(temperature[i])
    '''

    print(temperature_given_energy(energy_given_temperature(44.5), 44.5))

    print("Executed successfully!")