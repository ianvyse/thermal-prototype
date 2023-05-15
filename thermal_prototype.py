#IMPORTS
import matplotlib.pyplot as plt

#CONSTANTS
#######################################################################################################################################
#MATERIAL = [density [kg/m^3], thermal conductivity [W/m*k], heat capacity [J/kg*K]]
WHITE_PINE = [500, 0.12, 2.3] #https://material-properties.org/pine-wood-density-strength-melting-point-thermal-conductivity/
BEESWAX = [960, 0.2, 2.2] #https://material-properties.org/wax-density-strength-melting-point-thermal-conductivity/
AIR = [1.23, 0.025, 1.006]

#DIMENSION = [length [m], width [m], height [m]. thickness [m]]
TEN_FRAME_DEEP_BODY = [0.24, 0.47, 0.37, 0.01]

VARROA_TEMPERATURE = 44.5 #42-47 range
EXTERNAL_TEMPERATURE = 13.4
BROOD_TEMPERATURE = 35
TREATMENT_TIME = 2

#FUNCTIONS
#######################################################################################################################################
def calculate_energy_to_heat(standard_dimensions, critical_temperature, starting_temperature, material):
    '''
    Return the energy required to heat a Langstroth Hive of standard_dimensions and material to critical_temperature from starting_temperature.
    
    standard_dimensions -> list of ints of length 3
    critical_temperature -> int
    starting_temperature -> int
    material -> list of ints of length 3

    Using Q = m*c*dT
    Q -> energy required to heat hive [J]
    m -> mass of hive
    c -> heat capacity
    dT -> change in temperature
    '''
    mass_structure = (calculate_volume_external(standard_dimensions) - calculate_volume_internal(standard_dimensions)) * material[0]
    mass_wax = 0.5*calculate_volume_internal(standard_dimensions) * BEESWAX[1]
    mass_air = 0.5*calculate_volume_internal(standard_dimensions) * AIR[1]
    delta_temperature = critical_temperature - starting_temperature
    return (mass_structure * material[2] * delta_temperature) + (mass_wax * BEESWAX[1] * delta_temperature) + (mass_air * AIR[1] * delta_temperature)

def calculate_energy_lost(standard_dimensions, critical_temperature, external_temperature, material):
    '''
    Return the heat lost to the air of temperature external_temperature of a Langstroth Hive of temperature critical_temperature
    Assume heat is lost through material, i.e. the wood frame of the hive

    Using Q = (k*A*dT)/t
    Q -> heat lost per second [J/s or W]
    k -> thermal conductivity [W/m*K]
    A -> surface area [m^2]
    dT -> change in temperature from inside to outside [K]
    t -> thickness of hive wall / insulation [m]
    '''
    delta_temperature = critical_temperature - external_temperature
    surface_area = calculate_surface_area(standard_dimensions)
    return (surface_area * delta_temperature * material[1]) / standard_dimensions[3]

def calculate_energy_lost_with_insulation(insulation, standard_dimensions, critical_temperature, external_temperature, material):
    '''
    Return the heat lost to the air of temperature external_temperature of a Langstroth Hive of temperature critical_temperature
    Assume heat is lost through material, i.e. the wood frame of the hive

    Using Q = (k*A*dT)/t
    Q -> heat lost per second [J/s or W]
    k -> thermal conductivity [W/m*K]
    A -> surface area [m^2]
    dT -> change in temperature from inside to outside [K]
    t -> thickness of hive wall / insulation [m]

    insulation -> [thermal_coefficient, thickness]
    '''
    delta_temperature = critical_temperature - external_temperature
    surface_area = calculate_surface_area(standard_dimensions)
    return (surface_area * delta_temperature * insulation[0]) / insulation[1]

def calcualte_temperature_over_time(insulation, initial_temperature = VARROA_TEMPERATURE, standard_dimensions = TEN_FRAME_DEEP_BODY, external_temperature = EXTERNAL_TEMPERATURE, treatment_time = TREATMENT_TIME, material = WHITE_PINE):
  '''
  Return a list containing temperature values over time for a given starting temperature and a given insulation.

  Q = m*c*(T-T0) -> T = (Q/(m*c)) + T0

  insulation -> [thermal_coefficient, thickness]
  
  '''
  mass_structure = (calculate_volume_external(standard_dimensions) - calculate_volume_internal(standard_dimensions)) * material[0]
  mass_wax = 0.5*calculate_volume_internal(standard_dimensions) * BEESWAX[1]
  mass_air = 0.5*calculate_volume_internal(standard_dimensions) * AIR[1]
  count = 1
  temperature_array = []
  temperature_array.append(initial_temperature)
  energy = calculate_energy_to_heat(standard_dimensions, temperature_array[0], external_temperature, material)
  energy_lost = calculate_energy_lost_with_insulation(insulation, standard_dimensions, temperature_array[0], external_temperature, material)
  while (count < (3600*treatment_time)):
    energy -= energy_lost
    temperature_array.append((energy / (mass_structure*WHITE_PINE[2] + mass_wax*BEESWAX[2] + mass_air*AIR[2])) + external_temperature)
    energy = calculate_energy_to_heat(standard_dimensions, temperature_array[count], external_temperature, material)
    energy_lost = calculate_energy_lost_with_insulation(insulation, standard_dimensions, temperature_array[count], external_temperature, material)
    count+=1
  return temperature_array

def calculate_volume_external(standard_dimensions):
    '''
    Return the volume of the Langstroth Hive of standard_dimensions
    standard_dimensions -> list of ints of length 3
    '''
    return standard_dimensions[0] * standard_dimensions[1] * standard_dimensions[2]

def calculate_volume_internal(standard_dimensions):
    '''
    Return the internal volume of the Langstroth Hive of standard_dimensions
    standard_dimensions -> list of ints of length 3
    '''
    thickness = standard_dimensions[2]*2
    return (standard_dimensions[0]-thickness) * (standard_dimensions[1]-thickness) * (standard_dimensions[2]-thickness)

def calculate_surface_area(standard_dimensions):
    '''
    Return the surface area of the Langstroth Hive of standard_dimensions
    standard_dimensions -> list of ints of length 3
    '''
    return 2 * (standard_dimensions[0]*standard_dimensions[1] + standard_dimensions[1]*standard_dimensions[2] + standard_dimensions[2]*standard_dimensions[0])

#MAIN FUNCTION
#######################################################################################################################################
if __name__ == "__main__":
    insulation = [0.033, 0.1]
    temperature = calcualte_temperature_over_time(insulation)
    time = []
    for i in range(0, (3600*2)):
        time.append(i)
    
    plt.plot(time, temperature)
    plt.axhline(40)
    plt.show()

    print(calculate_energy_lost(TEN_FRAME_DEEP_BODY, VARROA_TEMPERATURE, EXTERNAL_TEMPERATURE, WHITE_PINE))
    print(calculate_energy_lost_with_insulation(insulation, TEN_FRAME_DEEP_BODY, VARROA_TEMPERATURE, EXTERNAL_TEMPERATURE, WHITE_PINE))

    print("Completed successfully.")