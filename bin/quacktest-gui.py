#!/usr/bin/python

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import logging

from QuackTest import core

# The valid file types used for saving and loading files from the file dialog
VALID_FILETYPES = [("Duck", ".duck"), ("Text", ".txt"), ("All", ".*")]


class Application(tk.Frame):
    '''
    Main application class
    '''

    def __init__(self, master=None):
        '''
        Initialize primary frame

        :param master:
        The main frame to be used. Should be none for the main frame
        '''
        # Initialize QuackTester and Associated log handler
        self.logging_handler = GuiHandler(self)
        self.quack_tester = core.QuackTester(log_handler=self.logging_handler)

        # Set frame dimensions and make visible
        super().__init__(master=master, height=300, width=400)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        '''
        Create all widgets within the application
        '''

        # Label listing the currently loaded ducky script (or empty if none loaded yet)
        self.ducky_script_text_label = None
        self.load_ducky_label()

        # Text box listing the contents of the current Ducky Script
        self.ducky_script_text_box = tk.Text(self, height=15, cursor="xterm", wrap=tk.NONE)
        self.ducky_script_text_box.grid(row=1, column=0, columnspan=3, sticky=tk.N + tk.E + tk.W, padx=10, pady=0)
        # Tags for different Ducky Script keywords
        self.valid_tags = ["REM", "STRING", "DELAY", "SPECIAL"]
        self.ducky_script_text_box.tag_configure("REM", foreground="gray", font=("Times", "10", "italic"))
        self.ducky_script_text_box.tag_configure("STRING", foreground="green")
        self.ducky_script_text_box.tag_configure("DELAY", foreground="orange")
        self.ducky_script_text_box.tag_configure("SPECIAL", foreground="blue")
        # Bind key event collector for altering keyword colors
        self.ducky_script_text_box.bind("<KeyRelease>", self.color_text)

        self.ducky_script_text_box_scroll_bar = tk.Scrollbar(self, orient=tk.VERTICAL,
                                                             command=self.ducky_script_text_box.yview)
        self.ducky_script_text_box.configure(yscrollcommand=self.ducky_script_text_box_scroll_bar.set)
        self.ducky_script_text_box_scroll_bar.grid(row=1, column=4, sticky=tk.N + tk.S + tk.W)

        # Contains the absolute path of the currently loaded Ducky Script. Used for both load and save scripts
        self.current_ducky_script = None

        # Button for loading Ducky Script into the editor
        self.load_script_button = tk.Button(self, width=20, command=self.load_script, text="Load Script")
        self.load_script_button.grid(row=2, column=0, padx=10, pady=5, sticky=tk.N)

        # Button for saving Ducky Script from the editor
        self.save_script_button = tk.Button(self, width=20, command=self.save_script, text="Save Script")
        self.save_script_button.grid(row=2, column=1, padx=0, pady=5, sticky=tk.N)

        # Button to execute Ducky script in editor
        self.execute_script_button = tk.Button(self, width=20, command=self.execute_script, text="Execute Script")
        self.execute_script_button.grid(row=2, column=2, padx=10, pady=5, sticky=tk.N)

        # Text to list debug logs
        self.log_text_box = tk.Text(self, height=15, background="gray", state=tk.DISABLED, cursor="arrow")
        self.log_text_box.grid(row=3, column=0, columnspan=3, sticky=tk.N + tk.E + tk.W, padx=5, pady=20)

        self.log_text_box_scroll_bar = tk.Scrollbar(self, orient=tk.VERTICAL,
                                                    command=self.log_text_box.yview)
        self.log_text_box.configure(yscrollcommand=self.log_text_box_scroll_bar.set)
        self.log_text_box_scroll_bar.grid(row=3, column=4, sticky=tk.N + tk.S + tk.W)

        # Checkbox to select log verbosity
        self.verbosity_checkbox_int = tk.IntVar()
        self.verbosity_checkbox = tk.Checkbutton(self, text="Verbose Logs", anchor=tk.NW,
                                                 variable=self.verbosity_checkbox_int)
        self.verbosity_checkbox.grid(row=4, column=0, pady=0)
        self.verbosity_checkbox.select()

    def load_ducky_label(self, text=""):
        '''
        Loads a new text label with the name of the current Ducky Script

        :param text:
        The text to set the label to (i.e. the name of the script being loaded)
        '''
        if self.ducky_script_text_label:
            self.ducky_script_text_label.destroy()

        self.ducky_script_text_label = tk.Label(self, text=text, justify=tk.LEFT)
        self.ducky_script_text_label.grid(row=0, column=0, columnspan=3, pady=5, sticky=tk.N + tk.W)

    def load_script(self):
        '''
        Loads a script from the file dialog into the file editor
        '''
        file = filedialog.askopenfile(title="Select Ducky Script",
                                      filetypes=VALID_FILETYPES)
        # Verify that the "Cancel" button wasn't pressed
        if file:
            self.current_ducky_script = file.name
            self.load_ducky_label(os.path.basename(self.current_ducky_script))
            self.ducky_script_text_box.delete("0.0", tk.END)
            for line in file.readlines():
                self.ducky_script_text_box.insert(chars=line, index=tk.CURRENT)
            file.close()
            # Update the text color in the editor
            self.color_text(None)
            self.ducky_script_text_box.edit_modified(False)

    def save_script(self):
        '''
        Callback for saving the current script in the editor
        '''
        # Determine if a script has already been loaded. If not, use default name and save location
        if not self.current_ducky_script:
            file = filedialog.asksaveasfile(defaultextension=".duck",
                                            title="Save Ducky Script",
                                            initialfile="ducky",
                                            filetypes=VALID_FILETYPES)
        else:
            # Start the file dialog using the same directory and name as the loaded ducky script
            file = filedialog.asksaveasfile(title="Save Ducky Script",
                                            initialfile=os.path.basename(self.current_ducky_script),
                                            initialdir=os.path.dirname(self.current_ducky_script),
                                            defaultextension=".duck",
                                            filetypes=VALID_FILETYPES)
        # Verify that the "Cancel" button wasn't pressed
        if file:
            # Read lines and write out to the selected file
            ducky_lines = self.ducky_script_text_box.get("1.0", tk.END)
            file.write(ducky_lines)
            file.close()
            self.load_ducky_label(os.path.basename(file.name))
            self.ducky_script_text_box.edit_modified(False)

    def execute_script(self):
        '''
        Executes the script currently within the text editor
        '''
        # Clear log box
        self.log_text_box.configure(state=tk.NORMAL)
        self.log_text_box.delete("1.0", tk.END)
        self.log_text_box.configure(state=tk.DISABLED)

        # Get all lines from editor box
        lines = self.ducky_script_text_box.get("1.0", tk.END)
        lines_list = [line for line in lines.split("\n")]

        # Determine the level of logging verbosity
        if self.verbosity_checkbox_int.get() == 1:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        # Run the script using the QuackTest library
        self.quack_tester.run(lines_list, log_level=log_level)

    def color_text(self, event):
        '''
        Callback called for every key entry in the text box. Used to do coloring on certain text keywords in the editor

        :param event:
        The keyboard event being executed. The actual content of this is unneeded
        '''

        # Remove all current tags from the text box to refresh
        for tag in self.valid_tags:
            self.ducky_script_text_box.tag_remove(tag, "1.0", tk.END)

        # Color each field according to the keywords present
        # REM coloring
        self.color_section(tag_name="REM", keywords=["REM"])

        # DELAY coloring
        self.color_section(tag_name="DELAY", keywords=["DELAY", "DEFAULTDELAY", "DEFAULT_DELAY"])

        # STRING coloring
        self.color_section(tag_name="STRING", keywords=["STRING"])

        # BUTTON coloring
        keys = list(core.special_key_dict.keys())
        keys.append("REPLAY")
        self.color_section(tag_name="SPECIAL", keywords=keys)

    def color_section(self, tag_name, keywords: list):
        '''
        Color a certain section using the given tag name when the specified keywords start a line

        :param tag_name:
        The tag used to style a line
        :param keywords:
        The keywords to search for when searching for lines to stylize
        '''

        for word in keywords:
            current_index = "1.0"
            while True:
                current_index = self.ducky_script_text_box.search(word, index=current_index, stopindex=tk.END, nocase=1)
                if current_index:
                    line_start = current_index + " linestart"
                    line_end = current_index + " lineend"
                    char_number = current_index.split(".")[1]
                    if char_number == "0":
                        self.ducky_script_text_box.tag_add(tag_name, line_start, line_end)
                    current_index = current_index + " + 1 lines"
                else:
                    break

    def write_log_entry(self, record):
        # print("Writing entry: " + message)
        self.log_text_box.tag_configure("ERROR_MESSAGE", foreground="red")

        self.log_text_box.configure(state=tk.NORMAL)
        self.log_text_box.insert(tk.END, chars=record.msg)
        if record.levelno != logging.DEBUG:
            print("Got error message")
            self.log_text_box.tag_add("ERROR_MESSAGE", "current linestart", "current lineend")
        self.log_text_box.insert(tk.END, chars="\n")
        self.log_text_box.configure(state=tk.DISABLED)

    def kill_self(self):
        if self.master:
            self.master.destroy()
        else:
            self.destroy()

    def exit_callback(self):
        if self.ducky_script_text_box.edit_modified():
            if messagebox.askokcancel(title="Warning",
                                      message="You have made edits since your last save. "
                                              "Are you sure you want to quit?"):
                self.kill_self()
        else:
            self.kill_self()


class GuiHandler(logging.Handler):
    def __init__(self, app, level=logging.DEBUG):
        super().__init__(level)
        self.app = app

    def emit(self, record):
        app.write_log_entry(record)


if __name__ == "__main__":
    top_level = tk.Tk()
    app = Application(master=top_level)
    app.master.title("QuackTest")
    top_level.protocol(name="WM_DELETE_WINDOW", func=app.exit_callback)
    top_level.resizable(width=False, height=False)
    app.mainloop()
