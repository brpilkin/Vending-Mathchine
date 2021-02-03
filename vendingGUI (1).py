
import tkinter as tk 
from tkinter import messagebox
   
  
LARGEFONT =("Verdana", 35) 
bgColor = "#6699cc"   
class tkinterApp(tk.Tk): 
      
    # __init__ function for class tkinterApp  
    def __init__(self, systemController, player, gameController, adminController):  
          
        # __init__ function for class Tk 
        tk.Tk.__init__(self)

        self.geometry("1024x600")  
        self.resizable(0, 0)
        self.container = tk.Frame(self)
        self.container.pack_propagate(0)
        self.container.pack(fill = tk.BOTH, expand = 1)
        self.container.pack()
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1) 
        self.gameController = gameController
        self.systemController = systemController
        self.player = player
        self.adminController = adminController
        systemController.loadPlayers()
        

        self.frames = {}   
        # create the Frames
        for F in (MainMenuGUI, LoginScreenGUI, AdminMenuGUI, PlayerMenuGUI, AddPlayerGUI, RemovePlayerGUI, EditPlayerGUI, EditSpecificPlayerGUI, DisplayLevelGUI, UpdateQuantityGUI, GameScreenGUI, CongratulatePlayerGUI, SelectRewardGUI): 
            frame = F(self.container, self) 
            frame.configure(bg=bgColor)
            self.frames[F] = frame  
            frame.grid(row = 0, column = 0, sticky ="nsew") 
   
        self.show_frame(MainMenuGUI) 
   
    # to display the current frame 
    def show_frame(self, cont): 
        frame = self.frames[cont] 
        frame.update()
        frame.tkraise() 

    # Update frame if information has changed on the same screen        
    def update_frame(self, cont):
        frame = cont(self.container, self) 
        frame.configure(bg=bgColor)
        self.frames[cont] = frame  
        frame.grid(row = 0, column = 0, sticky ="nsew")
        
    def goalMetorRepeat(self):
        correct = self.gameController.checkAnswer()
        if not correct:
            self.popupWindowIncorrect()
            
            
        if self.gameController.getCurrentCorrect() == self.gameController.getGoal():
            self.systemController.levelUp()
            self.show_frame(CongratulatePlayerGUI)
            
        else:
            self.gameController.createMathProblem(self.systemController.getCurrentPlayerLevel())
            self.update_frame(GameScreenGUI)
            
    def popupWindowIncorrect(self):
        tk.messagebox.showinfo("", "Incorrect")
        
        
         
        
        
        
 
    
 
    
 
# Main Menu GUI 
class MainMenuGUI(tk.Frame): 
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent) 

        AdminLoginButton = tk.Button(self, text ="Admin Login",font = ("Helveteica 0 bold"),height=10, width=40, command = lambda : [controller.show_frame(LoginScreenGUI), controller.systemController.setAdminOrPlayer(0)]) 
        AdminLoginButton.place(x=30,y=200) 
   
        playerLoginButton = tk.Button(self, text ="Player Login",font = ("Helveteica 0 bold"),height=10, width=40, command = lambda : [controller.show_frame(LoginScreenGUI), controller.systemController.setAdminOrPlayer(1)]) 
        playerLoginButton.place(x=550, y=200) 
   
           
   
   
# Login Screen GUI 
class LoginScreenGUI(tk.Frame): 
      
    def __init__(self, parent, controller): 
        
        self.usernameString = tk.StringVar()
        self.usernameString.set('')
        self.passwordString = tk.StringVar()
        self.passwordString.set('')
        
        qwertyKeys = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','0','1','2','3','4','5','6','7','8','9','<=']
        keyboardButtons = []
          
        tk.Frame.__init__(self, parent) 
        usernameLabel = tk.Label(self, text ="Username:",bg=bgColor, font = LARGEFONT) 
        usernameLabel.place(x=140,y=10) 
   
        # username entry variable
        usernameEntry = tk.Entry(self, font=("Ariel 14"), textvariable=self.usernameString) 
        # place the username entry box on the screen
        usernameEntry.place(x=400, y=20, height=50, width=300) 
        #usernameEntry.insert(0,controller.systemController.getUsernameStr())
        
        #Create password label + text box and place on screen
        passwordLabel = tk.Label(self, text ="Password:",bg=bgColor, font = LARGEFONT) 
        passwordLabel.place(x=150,y=75)
        passwordEntry = tk.Entry(self, font=("Ariel 14"), textvariable=self.passwordString)
        passwordEntry.place(x=400, y=85, height=50, width=300)
        passwordEntry.insert(0,controller.systemController.displaySecurePassword())
        
        # Create Submit button and place on screen
        loginSubmitButton = tk.Button(self, text ="Submit",height=3, width=30, command = lambda :  loginSuccess())  
        loginSubmitButton.place(x=400, y=475) 
        
        for letter in qwertyKeys:
            qwertyButton = tk.Button(self, text=letter, height=4, width=8, command = lambda letter = letter: focusFunctionForUserPass(letter))
            keyboardButtons.append(qwertyButton)
        
        xLocation = 150
        yLocation = 225
        for item in range(10):
           keyboardButtons[item].place(x=xLocation, y=yLocation)
           xLocation += 75
           
           
        xLocation = 175
        yLocation = 300
        for item in range(10,19):
           keyboardButtons[item].place(x=xLocation, y=yLocation)
           xLocation += 75 
           
        xLocation = 275
        yLocation = 375   
        for item in range(19,26):
            keyboardButtons[item].place(x=xLocation, y=yLocation)
            xLocation += 75 
            
        xLocation = 125
        yLocation = 150
        for item in range(26,37):
            keyboardButtons[item].place(x=xLocation, y=yLocation)
            xLocation += 75 
            
            
           
        def focusFunctionForUserPass(letter):
            if str(LoginScreenGUI.focus_get(self))=='.!frame.!loginscreengui.!entry': 
                controller.systemController.setUsernameInput(letter)
                x = controller.systemController.getUsernameStr()
                self.usernameString.set(x)
            else:
                controller.systemController.setPasswordInput(letter)
                y = controller.systemController.displaySecurePassword()
                self.passwordString.set(y)
                
        def loginSuccess():
            if controller.systemController.getAdminOrPlayer() == 0 and controller.systemController.checkLogin(controller.systemController.getUsernameStr(),controller.systemController.getPassword()) == True:
                controller.show_frame(AdminMenuGUI)
                self.usernameString.set('')
                self.passwordString.set('')
                controller.systemController.clearUserPassLevel()
            elif controller.systemController.getAdminOrPlayer() == 1 and controller.systemController.checkLogin(controller.systemController.getUsernameStr(),controller.systemController.getPassword()) == True:
                controller.systemController.setCurrentPlayer(controller.systemController.getUsernameStr())
                controller.show_frame(PlayerMenuGUI)
                self.usernameString.set('')
                self.passwordString.set('')
                controller.systemController.clearUserPassLevel()
            else:
                self.usernameString.set('')
                self.passwordString.set('')
                controller.systemController.clearUserPassLevel()
                controller.show_frame(MainMenuGUI)
                
   
   
# Admin Menu GUI 
class AdminMenuGUI(tk.Frame):  
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent) 
        addPlayerButton = tk.Button(self, text ="Add Player",font = ("Helveteica 0 bold"),height=7, width=35, command = lambda : [controller.show_frame(AddPlayerGUI),controller.systemController.clearUserPassLevel()]) 
        addPlayerButton.place(x=50,y=40) 
   
        removePlayerButton = tk.Button(self, text ="Remove Player",font = ("Helveteica 0 bold"),height=7, width=35, command = lambda : [controller.show_frame(RemovePlayerGUI),controller.update_frame(RemovePlayerGUI)]) 
        removePlayerButton.place(x=600, y=40) 
        
        updateQuantityButton = tk.Button(self, text ="Update Quantity",font = ("Helveteica 0 bold"),height=7, width=35, command = lambda : [controller.show_frame(UpdateQuantityGUI),controller.systemController.clearQuantity()] ) 
        updateQuantityButton.place(x=50,y=300) 
   
        editPlayerButton = tk.Button(self, text ="Edit Player",font = ("Helveteica 0 bold"),height=7, width=35, command = lambda : [controller.show_frame(EditPlayerGUI), controller.adminController.setListOfPlayers(controller.systemController.getListOfPlayers()), controller.update_frame(EditPlayerGUI)]) 
        editPlayerButton.place(x=600, y=300) 
        
        logOutButton = tk.Button(self, text ="Log Out",font = ("Helveteica 0 bold"),height=2, width=15, command = lambda : controller.show_frame(MainMenuGUI)) 
        logOutButton.place(x=425,y=500) 

    

# Player Menu GUI
class PlayerMenuGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        playGameButton = tk.Button(self, text="Play Game",font = ("Helveteica 0 bold"),height=7, width=35, command = lambda : [controller.show_frame(GameScreenGUI), controller.gameController.createMathProblem(controller.systemController.getCurrentPlayerLevel()), controller.update_frame(GameScreenGUI)])
        playGameButton.place(x=50, y=200)
        
        checkLevelButton = tk.Button(self, text="Check Level",font = ("Helveteica 0 bold"),height=7, width=35, command = lambda : [controller.show_frame(DisplayLevelGUI), controller.update_frame(DisplayLevelGUI)])
        checkLevelButton.place(x=600, y=200)
        
        logOutButton = tk.Button(self, text="Log Out",font = ("Helveteica 0 bold"),height=2, width=15, command = lambda : [controller.show_frame(MainMenuGUI),controller.gameController.clearCurrent(), controller.systemController.saveState()])
        logOutButton.place(x=425, y=400)
 
        
 
    
# Add Player GUI
class AddPlayerGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.usernameString = tk.StringVar()
        self.usernameString.set('')
        self.passwordString = tk.StringVar()
        self.passwordString.set('')
        self.levelNum = tk.StringVar()
        self.levelNum.set('')
        qwertyKeys = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','0','1','2','3','4','5','6','7','8','9','<=']
        keyboardButtons = []
        
        usernameLabel = tk.Label(self, text ="Username:",bg=bgColor, font = LARGEFONT) 
        usernameLabel.place(x=140,y=10) 
   
        # username entry variable
        usernameEntry = tk.Entry(self, font=("Ariel 14"), textvariable=self.usernameString) 
        # place the username entry box on the screen
        usernameEntry.place(x=400, y=20, height=50, width=300) 
        #usernameEntry.insert(0,controller.systemController.getUsernameStr())
        
        #Create password label + text box and place on screen
        passwordLabel = tk.Label(self, text ="Password:",bg=bgColor, font = LARGEFONT) 
        passwordLabel.place(x=150,y=75)
        passwordEntry = tk.Entry(self, font=("Ariel 14"), textvariable=self.passwordString)
        passwordEntry.place(x=400, y=85, height=50, width=300)
        passwordEntry.insert(0,controller.systemController.displaySecurePassword())
        
        enterLevelLabel = tk.Label(self, text="Level:", bg=bgColor, font = LARGEFONT)
        enterLevelLabel.place(x=245, y=145)
        levelEntry = tk.Entry(self, font=("Ariel 14"), textvariable=self.levelNum)
        levelEntry.place(x=400, y=155, height=50, width=50)
        

        addPlayerButton = tk.Button(self, text ="Add Player",height=3, width=20, command = lambda : [controller.show_frame(AdminMenuGUI), controller.systemController.newPlayer(usernameEntry.get(), controller.adminController.getNewPlayerPassword(),levelEntry.get()), clearInput(), controller.update_frame()]) 
        addPlayerButton.place(x=450, y=550) 
        
        backButton = tk.Button(self, text ="Back",height=3, width=20, command = lambda : controller.show_frame(AdminMenuGUI)) 
        backButton.place(x=870, y=540)
        
        for letter in qwertyKeys:
            qwertyButton = tk.Button(self, text=letter, height=4, width=8, command = lambda letter = letter: focusFunctionForUserPass(letter))
            keyboardButtons.append(qwertyButton)
        
        xLocation = 150
        yLocation = 300
        for item in range(10):
           keyboardButtons[item].place(x=xLocation, y=yLocation)
           xLocation += 75
           
           
        xLocation = 175
        yLocation = 375
        for item in range(10,19):
           keyboardButtons[item].place(x=xLocation, y=yLocation)
           xLocation += 75 
           
        xLocation = 275
        yLocation = 450 
        for item in range(19,26):
            keyboardButtons[item].place(x=xLocation, y=yLocation)
            xLocation += 75 
            
        xLocation = 125
        yLocation = 225
        for item in range(26,37):
            keyboardButtons[item].place(x=xLocation, y=yLocation)
            xLocation += 75 
            
            
           
        def focusFunctionForUserPass(letter):
            if str(AddPlayerGUI.focus_get(self))=='.!frame.!addplayergui.!entry': 
                controller.adminController.setNewPlayerUsername(letter)
                x = controller.adminController.getNewPlayerUsername()
                self.usernameString.set(x)
                
                
            elif str(AddPlayerGUI.focus_get(self))=='.!frame.!addplayergui.!entry2': 
                controller.adminController.setNewPlayerPassword(letter)
                y = controller.adminController.displaySecurePassword()
                self.passwordString.set(y)
                
            else:
                if letter in qwertyKeys[26:36] or letter == "<=":
                    controller.adminController.setNewPlayerLevel(letter)
                    z = controller.adminController.getNewPlayerLevel()
                    self.levelNum.set(z)
                    
                    
        def clearInput():
            self.usernameString.set('')
            self.passwordString.set('')
            self.levelNum.set('')
            controller.adminController.clearUserPassLevel()
            
            
            



# Remove Player GUI
class RemovePlayerGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        players = controller.systemController.getListOfPlayers()
        self.removeUser = tk.IntVar()
        self.removeUser.set(99)
        x=1
        i=0
        offset = 75
        for player in players:
            playerRadioButton = tk.Radiobutton(self, bg=bgColor, variable = self.removeUser, text=player.name, value=i, font=("Ariel 30 bold"))
            playerRadioButton.place(x=400, y=offset*x)
            x += 1
            i += 1 
        
        removePlayerButton = tk.Button(self, text="Remove Player", height=3, width=20, command = lambda : [controller.show_frame(AdminMenuGUI), controller.adminController.removePlayer(self.removeUser.get(), controller.systemController.getListOfPlayers()), controller.systemController.removePlayerFromList(self.removeUser.get())])
        removePlayerButton.place(x=400, y=offset * x + offset)
        
        backButton = tk.Button(self, text ="Back",height=3, width=20, command = lambda : controller.show_frame(AdminMenuGUI)) 
        backButton.place(x=870, y=540)
        
        def getPlayersChecked():
            pass

# Edit Player GUI
class EditPlayerGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        players = controller.systemController.getListOfPlayers()
        self.editUser = tk.IntVar()
        #radioButtons = []
        x=1
        i=0
        offset = 75
        for player in players:
            playerRadioButton = tk.Radiobutton(self, bg=bgColor, variable = self.editUser, text=player.name, value=i, font=("Ariel 30 bold"))
            #radioButtons.append(playerRadioButton)
            playerRadioButton.place(x=400, y=offset*x)
            x += 1
            i += 1 
        
        editPlayerButton = tk.Button(self, text="Edit Player", height=3, width=20, command = lambda : [controller.show_frame(EditSpecificPlayerGUI), controller.adminController.setCurrentEditPlayer(self.editUser.get(), controller.systemController.getListOfPlayers()),controller.systemController.clearUserPassLevel()])
        editPlayerButton.place(x=400, y=offset * x + offset)
        
        backButton = tk.Button(self, text ="Back",height=3, width=20, command = lambda : controller.show_frame(AdminMenuGUI)) 
        backButton.place(x=870, y=540)
        

# Edit Specific Player GUI        
class EditSpecificPlayerGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.usernameString = tk.StringVar()
        self.usernameString.set('')
        self.passwordString = tk.StringVar()
        self.passwordString.set('')
        self.levelNum = tk.StringVar()
        self.levelNum.set('')
        qwertyKeys = ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','0','1','2','3','4','5','6','7','8','9','<=']
        keyboardButtons = []
        
        usernameLabel = tk.Label(self, text ="Username:",bg=bgColor, font = LARGEFONT) 
        usernameLabel.place(x=140,y=10) 
        usernameEntry = tk.Entry(self, font=("Ariel 14"), textvariable=self.usernameString) 
        usernameEntry.place(x=400, y=20, height=50, width=300) 

        
        #Create password label + text box and place on screen
        passwordLabel = tk.Label(self, text ="Password:",bg=bgColor, font = LARGEFONT) 
        passwordLabel.place(x=150,y=75)
        passwordEntry = tk.Entry(self, font=("Ariel 14"), textvariable=self.passwordString)
        passwordEntry.place(x=400, y=85, height=50, width=300)
        passwordEntry.insert(0,controller.systemController.displaySecurePassword())
        
        enterLevelLabel = tk.Label(self, text="Level:", bg=bgColor, font = LARGEFONT)
        enterLevelLabel.place(x=245, y=145)
        levelEntry = tk.Entry(self, font=("Ariel 14"), textvariable=self.levelNum)
        levelEntry.place(x=400, y=155, height=50, width=50)
        

        editPlayerButton = tk.Button(self, text ="Edit Player",height=3, width=20, command = lambda : [controller.show_frame(AdminMenuGUI),controller.adminController.editPlayer(usernameEntry.get(), controller.adminController.getNewPlayerPassword(),levelEntry.get()), clearInput()]) 
        editPlayerButton.place(x=450, y=550) 
        
        backButton = tk.Button(self, text ="Back",height=3, width=20, command = lambda : controller.show_frame(AdminMenuGUI)) 
        backButton.place(x=870, y=540)
        
        for letter in qwertyKeys:
            qwertyButton = tk.Button(self, text=letter, height=4, width=8, command = lambda letter = letter: focusFunctionForUserPass(letter))
            keyboardButtons.append(qwertyButton)
        
        xLocation = 150
        yLocation = 300
        for item in range(10):
           keyboardButtons[item].place(x=xLocation, y=yLocation)
           xLocation += 75
           
           
        xLocation = 175
        yLocation = 375
        for item in range(10,19):
           keyboardButtons[item].place(x=xLocation, y=yLocation)
           xLocation += 75 
           
        xLocation = 275
        yLocation = 450 
        for item in range(19,26):
            keyboardButtons[item].place(x=xLocation, y=yLocation)
            xLocation += 75 
            
        xLocation = 125
        yLocation = 225
        for item in range(26,37):
            keyboardButtons[item].place(x=xLocation, y=yLocation)
            xLocation += 75 
            
            
           
        def focusFunctionForUserPass(letter):
            if str(EditSpecificPlayerGUI.focus_get(self))=='.!frame.!editspecificplayergui.!entry': 
                controller.adminController.setNewPlayerUsername(letter)
                x = controller.adminController.getNewPlayerUsername()
                self.usernameString.set(x)
            elif str(EditSpecificPlayerGUI.focus_get(self))=='.!frame.!editspecificplayergui.!entry2': 
                controller.adminController.setNewPlayerPassword(letter)
                y = controller.adminController.displaySecurePassword()
                self.passwordString.set(y)
                
            else:
                if letter in qwertyKeys[26:36] or letter == "<=":
                    controller.adminController.setNewPlayerLevel(letter)
                    z = controller.adminController.getNewPlayerLevel()
                    self.levelNum.set(z)
                    
                    
        def clearInput():
            self.usernameString.set('')
            self.passwordString.set('')
            self.levelNum.set('')
            controller.adminController.clearUserPassLevel()
            
        
# Display Level GUI 
class DisplayLevelGUI(tk.Frame):
      def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        playerLevelMessage = tk.Label(self, text=controller.systemController.getCurrentPlayerName() + " current level is " + str(controller.systemController.getCurrentPlayerLevel()), font=LARGEFONT, bg=bgColor)
        playerLevelMessage.place(x=200, y=250)
        
        backButton = tk.Button(self, text ="Back",height=3, width=20, command = lambda : controller.show_frame(PlayerMenuGUI)) 
        backButton.place(x=870, y=540)
        
        
# Update Quantity GUI        
class UpdateQuantityGUI(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.item1Quan = tk.StringVar()
        self.item1Quan.set('')
        self.item2Quan = tk.StringVar()
        self.item2Quan.set('')
        self.item3Quan = tk.StringVar()
        self.item3Quan.set('')
        self.item4Quan = tk.StringVar()
        self.item4Quan.set('')
        
        numpad = ['9','8','7','<=','6','5','4','3','2','1']
        numpadButtons = []
          
        item1Label = tk.Label(self, text ="Item 1:",bg=bgColor, font=("Ariel 18 bold")) 
        item1Label.place(x=385,y=50) 
        item1Entry = tk.Entry(self, font=("Ariel 14"), textvariable=self.item1Quan) 
        # place the username entry box on the screen
        item1Entry.place(x=470, y=50, height=40, width=100) 
        
        item2Label = tk.Label(self, text ="Item 2:",bg=bgColor, font=("Ariel 18 bold")) 
        item2Label.place(x=385,y=100) 
        item2Entry = tk.Entry(self, font=("Ariel 14"), textvariable=self.item2Quan) 
        # place the username entry box on the screen
        item2Entry.place(x=470, y=100, height=40, width=100) 
        
        item3Label = tk.Label(self, text ="Item 3:",bg=bgColor, font=("Ariel 18 bold")) 
        item3Label.place(x=385,y=150) 
        item3Entry = tk.Entry(self, font=("Ariel 14"), textvariable=self.item3Quan) 
        # place the username entry box on the screen
        item3Entry.place(x=470, y=150, height=40, width=100) 
        
        item4Label = tk.Label(self, text ="Item 4:",bg=bgColor, font=("Ariel 18 bold")) 
        item4Label.place(x=385,y=200) 
        item4Entry = tk.Entry(self, font=("Ariel 14"), textvariable=self.item4Quan) 
        # place the username entry box on the screen
        item4Entry.place(x=470, y=200, height=40, width=100) 
        
        
        for num in numpad:
            numButton = tk.Button(self, text=num, height=4, width=8, command = lambda num = num: focusFunctionForQuantity(num))
            numpadButtons.append(numButton)
        
        xLocation = 400
        yLocation = 250
        for j in range(4):
            numpadButtons[j].place(x=xLocation, y=yLocation)
            xLocation += 75
            
            
            
        xLocation = 400
        yLocation = 325
        for j in range(4,7):
            numpadButtons[j].place(x=xLocation, y=yLocation)
            xLocation += 75
            
        xLocation = 400
        yLocation = 400
        for j in range(7,10):
            numpadButtons[j].place(x=xLocation, y=yLocation)
            xLocation += 75
        
        
        
        updateQuantityButton = tk.Button(self, text ="Update Quantity",height=3, width=20, command = lambda : [controller.show_frame(AdminMenuGUI), controller.systemController.updateQuantity(controller.systemController.getRewardInt(1), controller.systemController.getRewardInt(2),controller.systemController.getRewardInt(3),controller.systemController.getRewardInt(4)), clearInput()]) 
        updateQuantityButton.place(x=425, y=525) 
        
        backButton = tk.Button(self, text ="Back",height=3, width=20, command = lambda : controller.show_frame(AdminMenuGUI)) 
        backButton.place(x=870, y=540)
        
        def focusFunctionForQuantity(num):
            if str(UpdateQuantityGUI.focus_get(self))=='.!frame.!updatequantitygui.!entry': 
                controller.systemController.setRewardQuantity(1, num)
                x = controller.systemController.getRewardInt(1)
                self.item1Quan.set(x)
            elif str(UpdateQuantityGUI.focus_get(self))=='.!frame.!updatequantitygui.!entry2': 
                controller.systemController.setRewardQuantity(2, num)
                x = controller.systemController.getRewardInt(2)
                self.item2Quan.set(x)
            elif str(UpdateQuantityGUI.focus_get(self))=='.!frame.!updatequantitygui.!entry3': 
                controller.systemController.setRewardQuantity(3, num)
                x = controller.systemController.getRewardInt(3)
                self.item3Quan.set(x)
            elif str(UpdateQuantityGUI.focus_get(self))=='.!frame.!updatequantitygui.!entry4': 
                controller.systemController.setRewardQuantity(4, num)
                x = controller.systemController.getRewardInt(4)
                self.item4Quan.set(x)
                
        def clearInput():
            self.item1Quan.set('')
            self.item2Quan.set('')
            self.item3Quan.set('')
            self.item4Quan.set('')
        
        
# Game Screen GUI        
class GameScreenGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)



        playerLabel = tk.Label(self, text="Player: {}".format(controller.systemController.getCurrentPlayerName()), font=("Ariel 25"), bg=bgColor)
        playerLabel.place(x=0, y=0) 
        
        goalLabel = tk.Label(self, text="Goal: {} / {}".format(controller.gameController.getCurrentCorrect(), controller.gameController.getGoal()), font=("Ariel 25"), bg=bgColor)
        goalLabel.place(x=850, y=0)
        
        levelLabel = tk.Label(self, text="Level: {}".format(controller.systemController.getCurrentPlayerLevel()), font=("Ariel 25"), bg=bgColor)
        levelLabel.place(x=0, y=540)
        
        quitButton = tk.Button(self, text ="Quit",height=3, width=20, command = lambda : [controller.show_frame(PlayerMenuGUI), controller.gameController.clearCurrent()]) 
        quitButton.place(x=870, y=540)
        
        mathProblemLabel = tk.Label(self, text=controller.gameController.getMathProblem(), font=LARGEFONT, bg=bgColor)
        mathProblemLabel.place(x=400, y=50)
        
        answerEntry = tk.Entry(self, font=("Ariel 20"), width=15)
        answerEntry.place(x=375, y=125)
        answerEntry.insert(0, controller.gameController.getAnswerInputStr())
        
        enterButton = tk.Button(self, text="Enter", font=("Ariel 14"),width=8, command = lambda : controller.goalMetorRepeat())
        enterButton.place(x=610, y=125)
        
        button7 = tk.Button(self, text="7", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput(7), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        button7.place(x=375, y=175)
        
        button8 = tk.Button(self, text="8", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput(8), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        button8.place(x=450, y=175)
        
        button9 = tk.Button(self, text="9", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput(9), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        button9.place(x=525, y=175)
        
        button4 = tk.Button(self, text="4", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput(4), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        button4.place(x=375, y=250)
        
        button5 = tk.Button(self, text="5", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput(5), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        button5.place(x=450, y=250)
        
        button6 = tk.Button(self, text="6", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput(6), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        button6.place(x=525, y=250)
        
        button1 = tk.Button(self, text="1", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput(1), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        button1.place(x=375, y=325)
        
        button2 = tk.Button(self, text="2", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput(2), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        button2.place(x=450, y=325)
        
        button3 = tk.Button(self, text="3", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput(3), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        button3.place(x=525, y=325)
        
        button0 = tk.Button(self, text="0", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput(0), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        button0.place(x=450, y=400)
        
        buttonNegative = tk.Button(self, text = "-", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput("-"), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        buttonNegative.place(x=375, y=400)
        buttonBackspace = tk.Button(self, text="<=", height=4, width=8, command = lambda : [controller.gameController.setAnswerInput(-1), controller.update_frame(GameScreenGUI), controller.show_frame(GameScreenGUI)])
        buttonBackspace.place(x=610, y=175)
 
        
# Congratulations GUI
class CongratulatePlayerGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        congratulationsLabel = tk.Label(self, bg=bgColor, font = LARGEFONT, text="Congratulations {}!!!".format(controller.player.getPlayerName()))
        congratulationsLabel.place(x=200, y=200)
        
        selectRewardButton = tk.Button(self, text="Select Reward", height=4, width=20, command = lambda : [controller.update_frame(SelectRewardGUI),controller.show_frame(SelectRewardGUI),controller.gameController.clearCurrent()])
        selectRewardButton.place(x=415, y=375)
        

# Select Reward GUI        
class SelectRewardGUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.stateButton1 = 'normal'
        self.stateButton2 = 'normal'
        self.stateButton3 = 'normal'
        self.stateButton4 = 'normal'
        
        
        if controller.systemController.getRewardQuantity(1) == 0:
            self.stateButton1 = 'disabled'
        if controller.systemController.getRewardQuantity(2) == 0:
            self.stateButton2 = 'disabled'
        if controller.systemController.getRewardQuantity(3) == 0:
            self.stateButton3 = 'disabled'
        if controller.systemController.getRewardQuantity(4) == 0:
            self.stateButton4 = 'disabled'
        
        selectRewardLabel = tk.Label(self, text="Select Reward", font = LARGEFONT, bg=bgColor)
        selectRewardLabel.place(x=325, y=25)
        
        item1Button = tk.Button(self, text="Item 1", font=("Ariel 14"), height=9, width=30,state=self.stateButton1, disabledforeground = '#696969', command= lambda : [controller.show_frame(PlayerMenuGUI), controller.systemController.rewardDispensed(1),controller.systemController.dispenseReward(1), controller.gameController.clearGame()])
        item1Button.place(x=50, y=100)
        
        item2Button = tk.Button(self, text="Item 2", font=("Ariel 14"), height=9, width=30,state=self.stateButton2,disabledforeground = '#696969',command= lambda : [controller.show_frame(PlayerMenuGUI), controller.systemController.rewardDispensed(2), controller.systemController.dispenseReward(2),controller.gameController.clearGame()])
        item2Button.place(x=600, y=100)
        
        item3Button = tk.Button(self, text="Item 3", font=("Ariel 14"), height=9, width=30,state=self.stateButton3,disabledforeground = '#696969',command= lambda : [controller.show_frame(PlayerMenuGUI), controller.systemController.rewardDispensed(3),controller.systemController.dispenseReward(3), controller.gameController.clearGame()])
        item3Button.place(x=50, y=350)
        
        item4Button = tk.Button(self, text="Item 4", font=("Ariel 14"), height=9, width=30,state=self.stateButton4,disabledforeground = '#696969',command= lambda : [controller.show_frame(PlayerMenuGUI), controller.systemController.rewardDispensed(4),controller.systemController.dispenseReward(4), controller.gameController.clearGame()])
        item4Button.place(x=600, y=350)
        
        