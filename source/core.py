from pathlib import Path
from Map import Map
from Seeker import Seeker
from Hider import Hider
import os


pathToMap = Path(__file__).parents[1] / "maps"

def playLevel1(mapFileName, pingResetInterval=5):
    mapGame = Map(fileName=pathToMap / mapFileName)
    seeker_pos, hider_pos_list, numOfHider = mapGame.getSeekerAndHidersInfo()

    seeker = Seeker(pos=seeker_pos, vissionRange=3)
    mapGame.addSeeker(seeker)
    hiderList = []
    for index, hider_pos in enumerate(hider_pos_list):
        hider = Hider(index ,seeker=seeker, pos=hider_pos, pingResetInterval=pingResetInterval, visionRange=3, map=mapGame)
        hiderList.append(hider)
        break

    numberOfSteps = 1

    while (seeker.get_catched() != len(hiderList)):
        os.system('cls' if os.name == 'nt' else 'clear')

        mapGame.setNumberOfSteps(numberOfSteps)
        for hider in hiderList:
            hider.setNumberOfSteps(numberOfSteps)
        seeker.setNumberOfSteps(numberOfSteps)
        
        seeker.move(mapGame)
        mapGame.display_map()
        numberOfSteps += 1
        print(f"Number of steps: {numberOfSteps}")

        wait = input("Press Enter to continue...")

def playLevel2(mapFileName, pingResetInterval=5):
    mapGame = Map(fileName=pathToMap / mapFileName)
    seeker_pos, hider_pos_list, numOfHider = mapGame.getSeekerAndHidersInfo()

    seeker = Seeker(pos=seeker_pos, vissionRange=3)
    mapGame.addSeeker(seeker)
    hiderList = []

    for index, hider_pos in enumerate(hider_pos_list):
        hider = Hider(index ,seeker=seeker, pos=hider_pos, pingResetInterval=pingResetInterval, visionRange=3, map=mapGame)
        hiderList.append(hider)

    while len(hiderList) < 3:
        hider = Hider(len(hiderList) ,seeker=seeker, pos=mapGame.getRandomPos(), pingResetInterval=pingResetInterval, visionRange=3, map=mapGame)
        hiderList.append(hider)

    numberOfSteps = 1

    while (seeker.get_catched() != len(hiderList)):
        os.system('cls' if os.name == 'nt' else 'clear')

        mapGame.setNumberOfSteps(numberOfSteps)
        for hider in hiderList:
            hider.setNumberOfSteps(numberOfSteps)
        seeker.setNumberOfSteps(numberOfSteps)
      
        seeker.move(mapGame)
        mapGame.display_map()
        numberOfSteps += 1
        print(f"Number of steps: {numberOfSteps}")

        wait = input("Press Enter to continue...")

def playLevel3(mapFileName, pingResetInterval=5):
    mapGame = Map(fileName=pathToMap / mapFileName)
    seeker_pos, hider_pos_list, numOfHider = mapGame.getSeekerAndHidersInfo()

    seeker = Seeker(pos=seeker_pos, vissionRange=3)
    mapGame.addSeeker(seeker)
    hiderList = []

    for index, hider_pos in enumerate(hider_pos_list):
        hider = Hider(index ,seeker=seeker, pos=hider_pos, pingResetInterval=pingResetInterval, visionRange=3, map=mapGame)
        hiderList.append(hider)

    while len(hiderList) < 3:
        hider = Hider(len(hiderList) ,seeker=seeker, pos=mapGame.getRandomPos(), pingResetInterval=pingResetInterval, visionRange=3, map=mapGame)
        hiderList.append(hider)

    numberOfSteps = 1

    while (seeker.get_catched() != len(hiderList)):
        os.system('cls' if os.name == 'nt' else 'clear')

        mapGame.setNumberOfSteps(numberOfSteps)
        for hider in hiderList:
            hider.setNumberOfSteps(numberOfSteps)
        seeker.setNumberOfSteps(numberOfSteps)

        
        for hider in hiderList:
            hider.move(mapGame)
        seeker.move(mapGame)
        mapGame.display_map()
        numberOfSteps += 1
        print(f"Number of steps: {numberOfSteps}")

        wait = input("Press Enter to continue...")


        
def playGame(mapFileName, pingResetInterval=5, level=1):
    mapGame = Map(fileName=pathToMap / mapFileName)
    seeker_pos, hider_pos_list, numOfHider = mapGame.getSeekerAndHidersInfo()

    seeker = Seeker(pos=seeker_pos, vissionRange=3)
    mapGame.addSeeker(seeker)
    hiderList = []

    for index, hider_pos in enumerate(hider_pos_list):
        hider = Hider(index ,seeker=seeker, pos=hider_pos, pingResetInterval=pingResetInterval, visionRange=3, map=mapGame)
        hiderList.append(hider)
        if level == 1:
            break
    
    while len(hiderList) < 3 and (level == 2 or level == 3):
        hider = Hider(len(hiderList) ,seeker=seeker, pos=mapGame.getRandomPos(), pingResetInterval=pingResetInterval, visionRange=3, map=mapGame)
        hiderList.append(hider)

    numberOfSteps = 1

    while (seeker.get_catched() != len(hiderList)):
        os.system('cls' if os.name == 'nt' else 'clear')

        mapGame.setNumberOfSteps(numberOfSteps)
        for hider in hiderList:
            hider.setNumberOfSteps(numberOfSteps)
        seeker.setNumberOfSteps(numberOfSteps)

        if level == 3:
            for hider in hiderList:
                hider.move(mapGame)
        seeker.move(mapGame)
        mapGame.display_map()
        numberOfSteps += 1
        print(f"Number of steps: {numberOfSteps}")

        wait = input("Press Enter to continue...")


