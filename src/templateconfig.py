import customtkinter
from tkinter import messagebox
import tkinter as tk
import os
import template_generator as tg
from pathvalidate import is_valid_filename, sanitize_filename

class config(customtkinter.CTk):

    """
    config is a class that allows users to choose the target path for their obsidian vault template,
    or obsidian vault path.

    Attributes
    ────────────────────────────────────────────────────────────

    filePath : str
        This decides the target path for the obsidian vault. 

    config : str
        This decides whether a default obsidian vault will be generated or a custom obsidian
        vault will be generated.

    config_path : str
        This represents the target path to the custom obsidian vault template file. 

    ticketNumber : str
        This represents the number of the ticket. 

    ticketName : str
        This represents the name of the ticket. 

    Methods
    ────────────────────────────────────────────────────────────
    
    initializeWidget()
        Just like any other classes in this program, it is used to initialize all the widgets in that page.
        It will call grid_configurate() to set up the grid, create three CTkLabel and one CTkButton. When the
        submitButton is clicked, the submitTemplate() method will be called.

    grid_configurate()
        Just like any other classes in this program, it will configurate the grid system for this page.

    submitTemplate()
        This method will first check whether the target directory already exists, if it does exist, a message box
        will be displayed showing the error. Else, it will use the templateGenerator() method to create the obsidian
        vault in the targetted path.

    validateInput()
        This method will check whether the ticketnum is a valid input.

    """
    def initializeWidget(self):
        self.grid_configurate()
        self.geometry("1000x500")
        self.title("Template Configuration")
        self.resizable(False,False)
        title = customtkinter.CTkLabel(self, text = "Template Configuration", font = ("American Typewriter",25))
        title.grid(row = 0, column = 0, columnspan = 2, sticky = "nsew")
        submitButton = customtkinter.CTkButton(self, text = "Submit", command = self.submitTemplate, height = 50)
        submitButton.grid(row = 3, column = 0, columnspan = 2, sticky = "nsew")
        ticketNameLabel = customtkinter.CTkLabel(self, text = "Name of the ticket", font = ("American Typewriter",25))
        ticketNameLabel.grid(row = 1, column = 0, pady = (0,0))
        self.ticketName.grid(row = 1, column = 1, pady = (0,0))
        ticketNumberLabel = customtkinter.CTkLabel(self, text = "Number of the ticket", font = ("American Typewriter",25))
        ticketNumberLabel.grid(row = 2, column = 0)
        self.ticketNumber.grid(row = 2, column = 1)

    def __init__(self, filePath, config, config_path):
        super().__init__()
        self.filePath = filePath
        self.config = config
        self.config_path = config_path
        self.ticketNumber = customtkinter.CTkTextbox(master = self, height = 40, width = 450, border_width = 3, border_color = "black")
        self.ticketName = customtkinter.CTkTextbox(master = self, height = 40, width = 450, border_width = 3, border_color = "black")
        self.initializeWidget()

    def submitTemplate(self):
        ticketName = self.ticketName.get("1.0","end-1c")
        if self.validateInput():
            if not is_valid_filename(ticketName):
                ticketName = sanitize_filename(ticketName)
                messagebox.showinfo(title = "Illegal ticket name", message = "Notice: The ticket name you provided is not a legal file name. Your ticket name has been changed to: " + ticketName)
            filePath = self.filePath + "/" + ticketName
            filePath = filePath.strip()
            if not self.directory_exists(filePath):
                os.makedirs(filePath) 
                tg.templateGenerator(self.config_path,filePath, self.ticketNumber.get("1.0","end-1c"), ticketName, self.config)
                messagebox.showinfo(title = "Vault Generated", message = "Success: The Obsidian Vault: " + ticketName + " has been generated.")
                self.destroy()
            else:
                messagebox.showerror(title = "Directory already exists", message = "Error: Directory already exists.")
        else:
           messagebox.showerror(title = "Inputs not found", message = "Error: One or more inputs not found.")

    def validateInput(self):
        ticketnum = int(self.ticketNumber.get("0.0","end"))  
        if ticketnum != 0:
            if self.ticketName.get("0.0","end").strip():
                return True
        return False

    def grid_configurate(self):
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)
        self.grid_rowconfigure(2, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
    
    def directory_exists(self, filePath):
        return os.path.exists(filePath)


