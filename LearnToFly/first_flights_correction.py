from pyparrot.Minidrone import Mambo

# enter here the adress of your  MANBO drone,you can put None for this session because we won't use it.
mamboAddr = None

# creating a MAMBO object
#We will use Wifi for this session, modify use_wifi to make it possible to use Wifi
mambo = Mambo(mamboAddr, use_wifi=True) #check that use_wifi=True


number_sequences=input("How many take off/landing sequences do you want to do ?")
number_sequences=int(number_sequences)

#Connection with the drone
print("trying to connect")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)

#if the connection can't be established; check the battery : connection could not be done with a low battery level. Sometimes also it does not work at first try. Try to change the battery or simply to restart the drone.


#if the drone is well connected
if (success):
###if you just want to do twice the take off/lading sequence (could be done with a for or a while loop also) uncomment the following lines

     #get the state information
    #print("sleeping")
    #mambo.smart_sleep(2)
    #mambo.ask_for_state_update()
    #mambo.smart_sleep(2)

    #print("taking off!")
    #mambo.safe_takeoff(5)

    #if (mambo.sensors.flying_state != "emergency"):

        #print("landing")
        #print("flying state is %s" % mambo.sensors.flying_state)
        #mambo.safe_land(5)
        #mambo.smart_sleep(5)

    #print("taking off!")
    #mambo.safe_takeoff(5)

    #if (mambo.sensors.flying_state != "emergency"):

        #print("landing")
        #print("flying state is %s" % mambo.sensors.flying_state)
        #mambo.safe_land(5)
        #mambo.smart_sleep(5)

###if you choose to ask to the user how many times he wants to do the take off/landing sequence (could also be done with a for loop).

    while number_sequences !=0:
        mambo.smart_sleep(2)
        print("taking off!")
        mambo.safe_takeoff(5)
        if (mambo.sensors.flying_state != "emergency"):
            print("landing")
            print("flying state is %s" % mambo.sensors.flying_state)
            mambo.safe_land(2)
            mambo.smart_sleep(2)
        print(number_sequences)
        number_sequences=number_sequences-1


    print("disconnect")
    mambo.disconnect()


#your turn : add lines to the code in order to have one more take off/landing sequence after first landing. You could also ask to the user how many take off/landing sequences he wants.

#It might be possible that the drone take off proprely but then do not land or do not respond to any command. Indeed, it is possible that the connexion between the drone and the labtop is gone even is the wifi seems turn on. To avoid this, check that the camera of your drone is well install and that it's not moving where your drone is flying.