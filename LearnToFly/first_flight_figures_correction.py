from pyparrot.Minidrone import Mambo

# enter here the adress of your  MANBO drone,you can put None for this session because we won't use it.
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
    mambo.safe_takeoff(3)
    
    # 
    # ### square using roll and pitch only
    # for i in range(0,4):
    #     mambo.smart_sleep(1)
    #     
    #     if i==0:
    #         print("Flying direct: roll")
    #         mambo.fly_direct(roll=20, pitch=0, yaw=0, vertical_movement=0, duration=1)
    #         
    #     if i==1:
    #         print("Flying direct: pitch")
    #         mambo.fly_direct(roll=0, pitch=20, yaw=0, vertical_movement=0, duration=1)
    #     if i==2:
    #         print("Flying direct: roll")
    #         mambo.fly_direct(roll=-20, pitch=0, yaw=0, vertical_movement=0, duration=1)
    #         
    #     if i==3:
    #         print("Flying direct: pitch")
    #         mambo.fly_direct(roll=0, pitch=-20, yaw=0, vertical_movement=0, duration=1)            
    #                     
    # 
    # 
    # ###square using turn_degrees and roll only
    # 
    # for i in range(0,4):
    #     mambo.smart_sleep(1)
    #     print("Flying direct: roll")
    #     mambo.fly_direct(roll=20, pitch=0, yaw=0, vertical_movement=0, duration=1)
    #     print("Showing turning (in place) using turn_degrees") 
    #     mambo.turn_degrees(90)  
    
    
    
    
    # ###square using turn_degrees and pitch only 
    # 
    # for i in range(0,4):
    #     mambo.smart_sleep(1)
    #     print("Flying direct: pitch")
    #     mambo.fly_direct(roll=0, pitch=20, yaw=0, vertical_movement=0, duration=1)
    #     print("Showing turning (in place) using turn_degrees")
    #     mambo.turn_degrees(90)   
                
    
   
    
    
    ###circle using fly_direct function (all parameters allowed)
    
    print("Circle")
    print("Flying direct: going around in a circle")
    mambo.fly_direct(roll=20, pitch=0, yaw=80, vertical_movement=0, duration=4)
    
    
    ###triangle using turn_degrees and fly_direct functions
    
    for i in range(3):
        mambo.smart_sleep(1)
        print("Flying direct: pitch")
        mambo.fly_direct(roll=0, pitch=20, yaw=0, vertical_movement=0, duration=1)
        print("Showing turning (in place) using turn_degrees")
        mambo.turn_degrees(90)  
    
    
    

    print("landing")
    mambo.safe_land(5)
    print("landed")
    mambo.smart_sleep(5)

    print("disconnect")
    mambo.disconnect()
    
    
    
#your turn : draw the figures above with your drone using the commands and functions you saw on the previous files. Tips : you will use some loops.
