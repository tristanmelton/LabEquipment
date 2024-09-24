from labequipment.instruments.lasers.AQ4321A import AQ4321A

import time

with AQ4321A() as laser:
    print(laser.query('*IDN?'))
    laser.unlock()

    print("Starting, Laser is " + laser.is_output_on())
    laser.enable_output()
    print("Laser is now " + laser.is_output_on())
    laser.disable_output()
    print("Laser is now " + laser.is_output_on())
    print("Current Laser Power: "+ str(laser.get_power()))
    laser.set_power(5)
    print("Current Laser Power: "+ str(laser.get_power()))
    laser.set_power(8)
    print("Current Laser Power: "+ str(laser.get_power()))
    print("Current Laser Wavelength: "+ str(laser.get_wavelength()))
    laser.set_wavelength(1560)
    print("Current Laser Wavelength: "+ str(laser.get_wavelength()))
    laser.set_wavelength(1530)
    print("Current Laser Wavelength: "+ str(laser.get_wavelength()))


    print("Sweep Min: " + str(laser.get_sweep_min()))
    laser.set_sweep_min(1480)
    print("Sweep Min: " + str(laser.get_sweep_min()))

    print("Sweep Max: " + str(laser.get_sweep_max()))
    laser.set_sweep_max(1580)
    print("Sweep Max: " + str(laser.get_sweep_max()))

    print("Sweep Time: " + str(laser.get_sweep_time()))
    laser.set_sweep_time(5) #20nm/s
    print("Sweep Time: " + str(laser.get_sweep_time()))

    laser.enable_output()
    time.sleep(2)
    laser.start_sweep()
    time.sleep(5)
    laser.disable_output()
