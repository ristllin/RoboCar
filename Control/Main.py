from Control.Communication import ComAgent
from Control.ControlAgent import ControlAgent


def main():
    com_agent = ComAgent()
    com_agent.awaitConnection() #blocking stage
    cntrl_agent = ControlAgent(com_agent)
    cntrl_agent.run()


if __name__ == "__main__":
    main()