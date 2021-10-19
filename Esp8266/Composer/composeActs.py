import time
from controlMotor import ControlMotor
from controlLed import ControlLed

class ComposeActs():
    """
        This class is a representation of a interpretation
        of a moviment group registered to the robot.
    """
    
    
    def __init__(self, presentation):
        self.__controlMotor = ControlMotor()
        self.__controlLed = ControlLed()
        self.__presentation = presentation
    
    
    def interpreter(self, moviment, body):
        """
            Based on moviment name, this method will
            do the correct job with the motors.
        """
        speed = body["speed"] if "speed" in body else ""
        leds = body["leds"] if "leds" in body else ""
        duration = body["time"]
        
        
        if moviment == "frente":
            self.__controlMotor.controlAll(speed[0], speed[1])
        elif moviment == "tras":
            self.__controlMotor.controlAll(-speed[0], -speed[1])
        elif moviment == "direita":
            self.__controlMotor.controlAll(speed[0], -speed[1])
        elif moviment == "esquerda":
            self.__controlMotor.controlAll(-speed[0], speed[1])
        elif moviment == "led on":
            self.__controlLed.on()
        elif moviment == "led off":
            self.__controlLed.off()
        elif moviment == "piscar":
            self.__controlLed.blink(leds, duration, body["repeat"])
        else:
            print("Uhh... Sorry, but this moviment is not register yet.")
            
        if not leds:
            time.sleep(duration)
            self.__controlMotor.controlAll(0, 0)
        
    
    def read_moviments(self, key):
        """
            This method will read all moviments
            and will send the command to be executed.
        """
        if "moviment" in self.__presentation[key]:
            self.execute_moviment(self.__presentation[key]["moviment"], self.__presentation[key])
        
        elif "moviments" in self.__presentation[key]:
            moviments = self.__presentation[key]["moviments"]
            
            if "repeat" in self.__presentation[key]:
                for time in range(0, self.__presentation[key]["repeat"]):
                    for position in range(0, len(moviments)):
                        self.execute_moviment(moviments[position], self.__presentation[key]["details"][position])
            else:
                for position in range(0, len(moviments)):
                    self.execute_moviment(moviments[position], self.__presentation[key]["details"][position])
                    
        else:
            print("Error: {" + "\n\tAct: " + str(i) + "\n\tMessage: It's impossible to find a moviment! \n}" )
            
        
    def execute_moviment(self, moviment, body):
        """
            This method will call the interpreter
            method to each moviment informed.
        """
        if "repeat" in body:
            for time in range(0, body["repeat"]):
                self.interpreter(moviment.lower(), body)
                
        else:
            self.interpreter(moviment.lower(), body)
            
        
