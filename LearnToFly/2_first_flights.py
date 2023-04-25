from pyparrot.Minidrone import Mambo
from pyparrot import DroneVision

# enter here the adress of your  MANBO drone,you can put None for this session because we won't use it.
mamboAddr = " "

# creating a MAMBO object
#We will use Wifi for this session, modify use_wifi to make it possible to use Wifi
mambo = Mambo(mamboAddr, use_wifi=True)




#Connection with the drone
print("trying to connect")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)


#if the drone is well connected
if (success):
    # get the state information
    print("sleeping")
    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)

    print("taking off!")
    mambo.safe_takeoff(5)



    if (mambo.sensors.flying_state != "emergency"):

        print("landing")
        print("flying state is %s" % mambo.sensors.flying_state)
        mambo.safe_land(5)
        mambo.smart_sleep(5)

    print("disconnect")
    mambo.disconnect()


#your turn : add lines to the code in order to have one more take off/landing sequence after first landing. You could also ask to the user how many take off/landing sequences he wants.


#use in case of an emergency