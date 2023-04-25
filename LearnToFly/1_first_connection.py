from pyparrot.Minidrone import Mambo

# enter here the adress of your  MANBO drone,you can put None for this session because we won't use it.
mamboAddr = None

# creating a MAMBO object
#We will use Wifi for this session, modify use_wifi to make it possible to use Wifi
mambo = Mambo(mamboAddr, use_wifi=True) #check that use_wifi=True




#Connection with the drone
print("trying to connect")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)

#if the connection can't be established; check the battery : connection could not be done with a low battery level. Sometimes also it does not work at first try. Try to change the battery or simply to restart the drone.

if (success):
    print("sleeping")
    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)
    print("disconnect")
    mambo.disconnect()