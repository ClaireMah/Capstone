from pyparrot.Minidrone import Mambo

# enter here the adress of your  MANBO drone, you can put None for this session because we won't use it.
mamboAddr = None

# creating a MAMBO object
#We will use Wifi for this session, modify use_wifi to make it possible to use Wifi
mambo = Mambo(mamboAddr, use_wifi=True)



 
#Connection with the drone
print("trying to connect")
success = mambo.connect(num_retries=3)
print("connected: %s" % success)

if (success):
    # get the state information
    print("sleeping")
    mambo.smart_sleep(2)
    mambo.ask_for_state_update()
    mambo.smart_sleep(2)

    print("taking off!")
    mambo.safe_takeoff(5)


    print("Flying direct: pitch")
    mambo.fly_direct(roll=0, pitch=50, yaw=0, vertical_movement=0, duration=0.5)
    
    print("Flying direct: going backwards (negative pitch)")
    mambo.fly_direct(roll=0, pitch=-50, yaw=0, vertical_movement=0, duration=0.5)

    
    print("Showing turning (in place) using turn_degrees") #turns right 
    mambo.turn_degrees(90)
    mambo.smart_sleep(2)
    mambo.turn_degrees(-90)
    mambo.smart_sleep(2)
    
    print("Flying direct: roll")
    mambo.fly_direct(roll=50, pitch=0, yaw=0, vertical_movement=0, duration=1)
    
    print("Flying direct: yaw")
    mambo.fly_direct(roll=0, pitch=0, yaw=50, vertical_movement=0, duration=1)



    print("Flying direct: going up")
    mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=50, duration=1)

    print("Flying direct: going around in a circle (yes you can mix roll, pitch, yaw in one command!)")
    mambo.fly_direct(roll=25, pitch=0, yaw=50, vertical_movement=0, duration=3)
    
    
    print("landing")
    mambo.safe_land(5)
    print("landed")
    mambo.smart_sleep(5)

    print("disconnect")
    mambo.disconnect()
    
    
    
#your turn : uncomment each paragraph one by one and see the effect to answer to the following questions :

# I want to go up with my drone, which parameter do I have to use on the fly_direct function ? to go up use vertical_movement with a positive value only for example : SEE PARAGRAPH SIX

#I want to go on the right with my drone, which parameter do I have to use on the fly_direct function ? use roll SEE PARAGRAPH FOUR

#I want to move forward with my drone, which parameter do I have to use on the fly_direct function ? use pitch SEE PARAGRAPH ONE

#Now I want to go backward, which value do I have to enter for the previous parameter ? use pitch with a negative value SEE PARAGRAPH TWO

#I want my drone to do a 90° turn on the right, which function do I have to use ? use the turn_degrees function SEE PARAGRAPH THREE

#I want my drone to spin, which parameter do I have to use on the fly_direct function ? use yaw SEE PARAGRAPH FIVE
