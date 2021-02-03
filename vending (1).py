#! /usr/bin/env python3
import vendingGUI as gui
import random
import RPi.GPIO as GPIO
import time
# System Controller Class
class SystemController(object):
    def __init__(self):
        self.listPlayers = []
        self.rewardDict = {'item1':1, 'item2':1, 'item3':1, 'item4':1}
        self.adminOrPlayer = -1
        self.username = []
        self.password = []
        self.reward1 = []
        self.reward2 = []
        self.reward3 = []
        self.reward4 = []
        self.currentPlayer = ''
        
# load information from files when program is started        
    def loadPlayers(self):
        playerListFile = open("/home/pi/Downloads/vendingPlayerList.txt", "r")
        for line in playerListFile:
           playerAttributeList = list(line.split())
           if len(playerAttributeList) != 0:
               self.listPlayers.append(Player(playerAttributeList[0], playerAttributeList[1], playerAttributeList[2]))
        playerListFile.close()
           
# remove player from player list           
    def removePlayerFromList(self, i):
        if len(self.listPlayers) > 0 and i != 99:
            self.listPlayers.remove(self.listPlayers[i])
        
     # Add new created player to list of players in the system   
    def newPlayer(self, username, password, level):
        self.listPlayers.append(Player(username, level))
        userPassFile =  open('/home/pi/Downloads/vendingUserPass.txt', 'a')
        userPassFile.write('\n' + username + ' ' + password)
        userPassFile.close()
        playerListFile = open("/home/pi/Downloads/vendingPlayerList.txt", "a")
        playerListFile.write('\n' + username + ' ' + level + ' ' + '0')
        playerListFile.close()
            
        
    

  
    # Check user entered username and password against the username password file
    def checkLogin(self, username, password):
        userPassFile = open('/home/pi/Downloads/vendingUserPass.txt', 'r')
        for line in userPassFile:
            line = line.strip()

            if username in line.lower() and password in line.lower() and username != '' and password != '':
               userPassFile.close()
               return True
        userPassFile.close()
        return False
    

    
    
    # set if admin or player is logging in
    def setAdminOrPlayer(self, num):
        self.adminOrPlayer = num
    
        
    
    
    # get the result of admin or player logging in
    def getAdminOrPlayer(self):
        return self.adminOrPlayer
  
    
  
    
    # create the username from input 
    def setUsernameInput(self, letter):
        if letter == '<=':
            if len(self.username) > 0:
                self.username.pop()    
        else:
            self.username.append(letter)
    
            
    
    # create the password from input        
    def setPasswordInput(self, letter):
        if letter == '<=':
            if len(self.password) > 0:
                self.password.pop()    
        else:
            self.password.append(letter)
  
    
  
    
    # displays * instead of the text password
    def displaySecurePassword(self):
        passwordHide = ''
        if len(self.password) > 0:
            for item in self.password:
                passwordHide += "*"
            return passwordHide
        else:
            return ''
  
    
  
    
    # convert the created username into a string
    def getUsernameStr(self):
        usernameStr = ''
        if len(self.username) > 0:
            for item in self.username:
                usernameStr += item
            return usernameStr
        else:
            return ''
    
    
    
    
    # turn the password list into string
    def getPassword(self):
        passStr = ''
        if len(self.password) > 0:
            for item in self.password:
                passStr += item
            return passStr
        else:
            return ''
    
    
    
    
    # clear the username and password information after a successful or unsuccessful attempt at logging in
    def clearUserPassLevel(self):
        self.username = []
        self.password = []
  
    
     
    # update the quantity of items in system
    def updateQuantity(self, item1, item2, item3, item4):
        if item1 != '':
            self.rewardDict['item1'] = int(item1)
        if item2 != '':
            self.rewardDict['item2'] = int(item2)
        if item3 != '':
            self.rewardDict['item3'] = int(item3)
        if item4 != '':
            self.rewardDict['item4'] = int(item4)
            
        for key, value in self.rewardDict.items():
            print(key,':',value)
            
            
            
    # decrement the reward quantity when a reward is dispensed     
    def rewardDispensed(self, item):
        if item == 1:
            self.rewardDict['item1'] = self.rewardDict['item1'] - 1
        if item == 2:
            self.rewardDict['item2'] = self.rewardDict['item2'] - 1
        if item == 3:
            self.rewardDict['item3'] = self.rewardDict['item3'] - 1
        if item == 4:
            self.rewardDict['item4'] = self.rewardDict['item4'] - 1
            
            
    # get the quantity of items in the system        
    def getRewardQuantity(self, item):
        if item == 1:
            return self.rewardDict['item1']
        elif item == 2:
            return self.rewardDict['item2']
        elif item == 3:
            return self.rewardDict['item3']
        elif item == 4:
            return self.rewardDict['item4']
        
        
    # create the list for the quantity    
    def setRewardQuantity(self, item, num):
        if item == 1:
            if num == '<=':
                if len(self.reward1) > 0:
                    self.reward1.pop()    
            else:
                self.reward1.append(num)
                
        if item == 2:
            if num == '<=':
                if len(self.reward2) > 0:
                    self.reward2.pop()    
            else:
                self.reward2.append(num)
                
        if item == 3:
            if num == '<=':
                if len(self.reward3) > 0:
                    self.reward3.pop()    
            else:
                self.reward3.append(num)
                
        if item == 4:
            if num == '<=':
                if len(self.reward4) > 0:
                    self.reward4.pop()    
            else:
                self.reward4.append(num)
     
                
     
    # create reward strings    
    def getRewardInt(self,item):
        rewardStr1 = ''
        rewardStr2 = ''
        rewardStr3 = ''
        rewardStr4 = ''
        
        if item == 1:
            for x in self.reward1:
                rewardStr1 = rewardStr1 + x
            return rewardStr1
                
        elif item == 2:
            for x in self.reward2:
                rewardStr2 = rewardStr2 + x
            return rewardStr2
        
        elif item == 3:
            for x in self.reward3:
                rewardStr3 = rewardStr3 + x
            return rewardStr3
        
        elif item == 4:
            for x in self.reward4:
                rewardStr4 = rewardStr4 + x
            return rewardStr4
        
        
        
    # clears quantity     
    def clearQuantity(self):
        self.reward1 = []
        self.reward2 = []
        self.reward3 = []
        self.reward4 = []
        
        
    # get list of players in system    
    def getListOfPlayers(self):
        return list(self.listPlayers) 
        
        
        
    # get current players name    
    def getCurrentPlayerName(self):
        if self.currentPlayer != "":
            return self.currentPlayer.name
        else:
            return ''
        
        
    # get current players level
    def getCurrentPlayerLevel(self):
        if self.currentPlayer != "":
            return self.currentPlayer.level
        else:
            return ''
    
    # get current players number of iterations
    def getCurrentPlayeriterations(self):
        if self.currentPlayer != "":
            return self.currentPlayer.iterations
        else:
            return ''
    
    

    # sets the current player in system
    def setCurrentPlayer(self, player):
        for item in self.listPlayers:
            if item.name == player:
                self.currentPlayer = item




    # handles if user is to be leveled up
    def levelUp(self):
        if self.currentPlayer.iterations == "10" and self.currentPlayer.level < "5":
            self.currentPlayer.level = str(int(self.currentPlayer.level) + 1)
            self.currentPlayer.iterations = "0"
        elif self.currentPlayer.iterations == "10" and self.currentPlayer.level == "5":
            self.currentPlayer.iterations = "0"
        else:
            self.currentPlayer.iterations = str(int(self.currentPlayer.iterations) + 1)
            
    
    # saves the state of the system        
    def saveState(self):
        player = self.currentPlayer
        listPlayers = []
        correctLine2 = 0
         
        userlistFile =  open('/home/pi/Downloads/vendingPlayerList.txt', 'r')
        for line in userlistFile:
            listPlayers.append(line)
        userlistFile.close()
        
        x = 0
        for line in listPlayers:
            newLine = line.split()
            if newLine[0] == player.name:
                correctLine2 = x
            x += 1


        listPlayers[correctLine2] = "{} {} {}\n".format(player.name, player.level, player.iterations)

        
        playerListFile = open("/home/pi/Downloads/vendingPlayerList.txt", "w")
        for line in listPlayers:
            playerListFile.write(line)
        playerListFile.close()
    
    
    
    
    # dispenses reward using GPIO from raspberry pi
    def dispenseReward(self, num):
        GPIO.setmode(GPIO.BOARD)

        # Set pin 11 as an output, and set servo1 as pin 11 as PWM
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(12,GPIO.OUT)
        GPIO.setup(13,GPIO.OUT)
        GPIO.setup(15,GPIO.OUT)
        servo1 = GPIO.PWM(11,50) # Note 11 is pin, 50 = 50Hz pulse
        servo3 = GPIO.PWM(12,50)
        servo4 = GPIO.PWM(13,50)
        servo2 = GPIO.PWM(15,50)
        #start PWM running, but with value of 0 (pulse off)
        servo1.start(0)
        servo2.start(0)
        servo3.start(0)
        servo4.start(0)

        if num == 1:
            servo1.ChangeDutyCycle(9)
            time.sleep(1)
            servo1.stop()
        
        elif num == 2:
            servo2.ChangeDutyCycle(6)
            time.sleep(1)
            servo2.stop()    

        elif num == 3:
            servo3.ChangeDutyCycle(9)
            time.sleep(1)
            servo3.stop()
            
        elif num == 4:
            servo4.ChangeDutyCycle(6)
            time.sleep(1)
            servo4.stop()    
            
        GPIO.cleanup()
    
    


# Admin Class    
class Admin(object):
    def __init__(self):
        self.newPlayerUser = []
        self.newPlayerPass = []
        self.newPlayerLevel = []
        self.currentPlayer = ''
        self.currentEditPlayer = ''
        self.listOfPlayers = []
    
        
    # sets new players username
    def setNewPlayerUsername(self, letter):
        if letter == '<=':
            if len(self.newPlayerUser) > 0:
                self.newPlayerUser.pop()    
        else:
            self.newPlayerUser.append(letter)
    
        # gets the string reprensentation of new player username
    def getNewPlayerUsername(self):
        newStr = ''
        for item in self.newPlayerUser:
            newStr += item
        return newStr
    
    
    # sets new player password
    def setNewPlayerPassword(self, letter):
        if letter == '<=':
            if len(self.newPlayerPass) > 0:
                self.newPlayerPass.pop()    
        else:
            self.newPlayerPass.append(letter)
     
        
    # gets string representation of new players password 
    def getNewPlayerPassword(self):
        newStr = ''
        for item in self.newPlayerPass:
            newStr += item
        return newStr
    
    
    # sets new players level
    def setNewPlayerLevel(self, level):
        if level == '<=':
            if len(self.newPlayerLevel) > 0:
                self.newPlayerLevel.pop()    
        else:
            self.newPlayerLevel.append(level)
     
        
     # gets string representation of new players password 
    def getNewPlayerLevel(self):
        newStr = ''
        for item in self.newPlayerLevel:
            newStr += item
        if newStr != '':
            return int(newStr)
        else:
            return newStr
        
    # clears the new players variables
    def clearUserPassLevel(self):
        self.newPlayerPass = []
        self.newPlayerUser = []
        self.newPlayerLevel = []
  
    
      # displays * instead of password on screen
    def displaySecurePassword(self):
        passwordHide = ''
        if len(self.newPlayerPass) > 0:
            for item in self.newPlayerPass:
                passwordHide += "*"
            return passwordHide
        else:
            return ''


    # edit player function
    def editPlayer(self, username, password, level):
        player = self.currentEditPlayer
        listUserPass = []
        listPlayers = []
        correctLine = 0
        correctLine2 = 0
        currentPass = ''    
        userPassFile =  open('/home/pi/Downloads/vendingUserPass.txt', 'r')
        for line in userPassFile:
            listUserPass.append(line)
        userPassFile.close()
            
        userlistFile =  open('/home/pi/Downloads/vendingPlayerList.txt', 'r')
        for line in userlistFile:
            listPlayers.append(line)
        userlistFile.close()
        
        x = 0
        for line in listUserPass:
            newLine = line.split()
            if newLine[0] == player.name:
                currentPass = newLine[1]
                correctLine = x
            x += 1
            
        x = 0
        for line in listPlayers:
            newLine = line.split()
            if newLine[0] == player.name:
                correctLine2 = x
            x += 1
        
        if username != "":
            player.name = username
        if password != "":
            currentPass = password
        if level != "":
            player.level = level
  
        listUserPass[correctLine] = "{} {}\n".format(player.name, currentPass)
        listPlayers[correctLine2] = "{} {} {}\n".format(player.name, player.level, player.iterations)
        
        userPassFile =  open('/home/pi/Downloads/vendingUserPass.txt', 'w')
        for line in listUserPass:
            userPassFile.write(line)
        userPassFile.close()
        
        playerListFile = open("/home/pi/Downloads/vendingPlayerList.txt", "w")
        for line in listPlayers:
            playerListFile.write(line)
        playerListFile.close()
    
    # gets which player the user is currently editing
    def getCurrentEditPlayer(self):
        return self.currentEditPlayer
    

    # sets the currently editing player
    def setCurrentEditPlayer(self, i, players):
        if len(players) > 0:
            self.currentEditPlayer = players[i]

    # sets the list of players in system
    def setListOfPlayers(self, players):
        self.listOfPlayers = list(players)
        
        
     # function to remove player   
    def removePlayer(self, i, listOfPlayers):
        listUserPass = []
        listPlayers = []
        
        if i == 99:
            return
        userPassFile =  open('/home/pi/Downloads/vendingUserPass.txt', 'r')
        for line in userPassFile:
            listUserPass.append(line)
        userPassFile.close()
            
        userlistFile =  open('/home/pi/Downloads/vendingPlayerList.txt', 'r')
        for line in userlistFile:
            listPlayers.append(line)
        userlistFile.close()
        

        for line in listPlayers:
            newLine = line.split()
            if newLine[0] == listOfPlayers[i].name:
                listPlayers.remove(line)
                
        for line in listUserPass:
            newLine = line.split()
            if newLine[0] == listOfPlayers[i].name:
                listUserPass.remove(line)
                
                
        listOfPlayers.remove(listOfPlayers[i])
                
        userPassFile =  open('/home/pi/Downloads/vendingUserPass.txt', 'w')
        for line in listUserPass:
            userPassFile.write(line)
        userPassFile.close()
        
        playerListFile = open("/home/pi/Downloads/vendingPlayerList.txt", "w")
        for line in listPlayers:
            playerListFile.write(line)
        playerListFile.close()

    
        
# Player Class        
class Player(object):
    def __init__(self, name="User1", level=2, iterations=0):
        self.name = name
        self.level = level
        self.iterations = iterations
        
    # get methods for player name and level    
    def getPlayerName(self):
        return self.name
    
    def getPlayerLevel(self):
        return self.level

    def getPlayerIterations(self):
        return self.iterations
    
    def setPlayerIterations(self):
        self.iterations += 1







# Game Controller Class        
class Game(object):
    def __init__(self):
        self.goal = 2
        self.operators = ["+", "-", "*"]
        self.answerInput = []
        self.mathProblem = ""
        self.computedAnswer = 0
        self.currentCorrect = 0
    
    # get method for Goal    
    def getGoal(self):
        return self.goal
    
    def setGoal(self, goal):
        self.goal = goal
    

    # current function to create a math problem to be displayed     
    def createMathProblem(self, level):
        randomOperatorHigherLevel = random.randint(1,3)
        if level == "1":
            self.mathProblem =  "{} {} {}".format(random.randint(0,10), random.choice(self.operators[:2]), random.randint(0,10))
            
            
        elif level == "2":
            self.mathProblem = "{} {} {}".format(random.randint(0,50), random.choice(self.operators[:2]), random.randint(0,50))
            
            
        elif level == "3":
            if randomOperatorHigherLevel == 1:
                self.mathProblem = "{} {} {}".format(random.randint(-100,100), random.choice(self.operators[:2]), random.randint(-100,100))
            else:
                 self.mathProblem = "{} {} {}".format(random.randint(0,10), self.operators[2], random.randint(0,10))
        
        elif level == "4":
            if randomOperatorHigherLevel == 1:
                 self.mathProblem = "{} {} {}".format(random.randint(-1000,1000), random.choice(self.operators[:2]), random.randint(-1000,1000))
            else:
                self.mathProblem = "{} {} {}".format(random.randint(0,20), self.operators[2], random.randint(0,20))
                
                
        elif level == "5":
            if randomOperatorHigherLevel == 1:
                self.mathProblem = "{} {} {}".format(random.randint(-10000,10000), random.choice(self.operators[:2]), random.randint(-10000,10000))
            else: 
                self.mathProblem = "{} {} {}".format(random.randint(0,50), self.operators[2], random.randint(0,50))
            
                
        if self.mathProblem != "":        
            self.computedAnswer = eval(self.mathProblem)                 
                
    # function to check the answer entered by user to the computed answer            
    def checkAnswer(self):
        if self.computedAnswer == self.getAnswerInputInt():
            self.setCurrentCorrect()
            self.answerInput = []
            return True
        else:
            self.answerInput = []
            return False
    
    # returns the current correctly answered problems                    
    def getCurrentCorrect(self):
        return self.currentCorrect
    
    
    # sets the current correct number of problems answered
    def setCurrentCorrect(self):
        self.currentCorrect += 1
    
    # clears the current correct variable    
    def clearCurrent(self):
        self.currentCorrect = 0
    
    # returns a math problem         
    def getMathProblem(self):
        return self.mathProblem
    
    # functions im working with to fill the entry box with what user selects    
    def setAnswerInput(self, num):
        if num == -1:
            if len(self.answerInput) > 0:
                self.answerInput.pop()
        elif  num == "-":
            if len(self.answerInput) > 0:
               if self.answerInput[0] == "-":
                    self.answerInput.remove("-")
               else:
                   self.answerInput.insert(0, "-")
            else:
                self.answerInput.append("-")
        else:
            self.answerInput.append(num)

    # get input representation of users entered input
    def getAnswerInputInt(self):
        if self.getAnswerInputStr() != "":
            return int(self.getAnswerInputStr())

     # get string representation of users entered answer       
    def getAnswerInputStr(self):
        newString = ''
        for item in self.answerInput:
            newString += str(item)
        if newString != '':
            return newString
        else:
            return ''
        
    # clears game
    def clearGame(self):
        self.currentCorrect = 0
        
  
    
  
    
  
    
newGame = SystemController()
newPlayer = Player()
gameController = Game()
adminController = Admin()
root = gui.tkinterApp(newGame, newPlayer, gameController, adminController) 
root.mainloop()          