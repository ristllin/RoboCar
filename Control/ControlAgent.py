from Control.Constants import *
import pygame



class ControlAgent:
    def __init__(self,com_agent):
        self.com_agent = com_agent
        self.status = {
            "speed" : 0,
            "acc" : 0,
            "location" : {"x":0,"y":0},
            "angle" : 0,
        }
        pygame.init()
        pygame.display.set_mode(size=(640,480))
        if DEBUG: print("Control Agent Initiated successfully")

    def __repr__(self):
        return str(self.status)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();  # sys.exit() if sys is imported
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.Generate_Command("front")
                    if event.key == pygame.K_DOWN:
                        self.Generate_Command("back")
                    if event.key == pygame.K_RIGHT:
                        self.Generate_Command("right")
                    if event.key == pygame.K_LEFT:
                        self.Generate_Command("left")
                    if event.key == pygame.K_KP_PLUS:
                        self.Update_Status("higher")
                    if event.key == pygame.K_KP_MINUS:
                        self.Update_Status("lower")
                    if event.key == pygame.K_ESCAPE:
                        self.Exit()

    def Update_Status(self, command):
        if DEBUG: print("Updating status", command)
        if command == "higher": self.status["speed"] += 1
        elif command == "lower" and self.status["speed"] > 0: self.status["speed"] -= 1

    def Generate_Command(self, command):
        if DEBUG: print("Generating Command", command)
        command_msg = {"speed":self.status["speed"], "acc":self.status["acc"], "action":command}
        self.com_agent.send(command_msg)

    def Exit(self):
        self.com_agent.terminate()
        print("Program Terminated")
        exit()