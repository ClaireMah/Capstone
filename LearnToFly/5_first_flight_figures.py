from pyparrot.Minidrone import Mambo

# enter here the adress of your  MANBO drone,you can put None for this session because we won't use it.
mamboAddr = "d0:3a:54:11:e6:23"

# creating a MAMBO object
#We will use Wifi for this session, modify use_wifi to make it possible to use Wifi
mambo = Mambo(mamboAddr, use_wifi=False)



 
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
    
    
    ### square using roll and pitch only
   
   @TO_DO
    
    
    
    ###square using turn_degrees and roll only
   @TO_DO    

    
   
    
    ###square using turn_degrees and pitch only
   @TO_DO 
    
 
    
    
    
    ###circle using fly_direct function (with all the parameter that you want)
    
   @TO_DO
    

    
    
    ###triangle using turn_degrees and fly_direct functions
    
   @TO_DO
  
    
    
    
    

    print("landing")
    mambo.safe_land(5)
    print("landed")
    mambo.smart_sleep(5)

    print("disconnect")
    mambo.disconnect()
    
    
    
#your turn : draw the figures above with your drone using the commands and functions you saw on the previous files. Tips : you will use some loops.
