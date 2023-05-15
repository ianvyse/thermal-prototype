'''
Email Sanjeev Chandra: chandra@mie.utoronto.ca
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

def Q_given_dT(dT):
    '''
    Q = (m1c1 + m2c2) * dT
    '''
    mass_air = 0.2 * INTERNAL_VOLUME * AIR[0]
    mass_beeswax = 0.8 * INTERNAL_VOLUME * BEESWAX[0]
    return mass_air * AIR[1] * dT + mass_beeswax * BEESWAX[1] * dT

def dT_given_Q(Q):
    '''
    dT = Q / (m1c1 + m2c2)
    '''
    mass_air = 0.2 * INTERNAL_VOLUME * AIR[0]
    mass_beeswax = 0.8 * INTERNAL_VOLUME * BEESWAX[0]
    return Q / (mass_air * AIR[1] + mass_beeswax * BEESWAX[1])

def dQdt_given_thermal_coefficient(insulation, internal_temperature):
    '''
    dQ/dt = h/t * A * dT
    '''
    thermal_coefficient = insulation[0] / insulation[1]
    return thermal_coefficient * INTERNAL_SURFACE_AREA * (internal_temperature - EXTERNAL_TEMPERATURE)

def temperature_over_time(insulation):
    temperature = []
    temperature.append(CRITICAL_TEMPERATURE)
    change_in_temperature = dQdt_given_thermal_coefficient(insulation, temperature[0])
    for i in range(1, TREATMENT_TIME * 3600):
        temperature.append(temperature[i-1] - dT_given_Q(change_in_temperature))
        change_in_temperature = dQdt_given_thermal_coefficient(insulation, temperature[i])
    return temperature

if __name__ == "__main__":

    temperature_styrofoam = temperature_over_time(STYROFOAM)
    #temperature_aerogel = temperature_over_time(AEROGEL)

    time = []
    for i in range(0, TREATMENT_TIME * 3600):
        time.append(i)
    
    plt.plot(time, temperature_styrofoam)
    #plt.plot(time, temperature_aerogel)
    plt.show()

    i = 0
    while temperature_styrofoam[i] >= (CRITICAL_TEMPERATURE - CRITICAL_RANGE):
        i+=1
        print(i, temperature_styrofoam[i])
    
    print(dQdt_given_thermal_coefficient(STYROFOAM, CRITICAL_TEMPERATURE));

    print("Completed successfully!")
