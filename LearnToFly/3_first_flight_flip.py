from pyparrot.Minidrone import Mambo

#enter the adress of your Mambo here,you can put None for this session because we won't use it.
mamboAddr = None

# creating a MAMBO object
#We will use Wifi for this session, modify use_wifi to make it possible to use Wifi
mambo = Mambo(mamboAddr, use_wifi=True)

print("trying to connect")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)

if (success):
    # get the state information
    print("sleeping")
    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)

    #taking of
    print("taking off!")
    mambo.safe_takeoff(5)

    if (mambo.sensors.flying_state != "emergency"):

        #flip
        print("flip left")
        print("flying state is %s" % mambo.sensors.flying_state)
        success = mambo.flip(direction="left")
        print("mambo flip result %s" % success)
        mambo.smart_sleep(5)

        #landing
        print("landing")
        print("flying state is %s" % mambo.sensors.flying_state)
        mambo.safe_land(5)
        mambo.smart_sleep(5)


    print("disconnect")
    mambo.disconnect()



#your turn : -modify the code to do a flip in the front direction
#            -modify the code to do a flip in the right direction and then a flip in the back direction : BE CAREFULL always put the line "manbo.smart_sleep(5)" ; it will allow your drone to rest between two flips. Otherwise it will crash.
