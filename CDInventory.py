#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# AdamH, 2020-Feb-28, Added Functionality
# DKlos, 2020-Mar-05, Passing table to functions, using local instead of global variables.
# AdamH, 2020-Mar-08, Changed data useage to saving and using pickled data. 
# AdamH, 2020-Mar-10, Added exception handling where applicable
#------------------------------------------#
import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- USER INPUT AND OUTPUT -- #
class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def input_album():
        """Function to allow the user to input a new inventory item to be inputted later into our 2D data stucture in memory

        Prompts the user to enter an ID, Album, and Artist as strings.
        
        Args:
            None.

        Returns:
            StrID, strTitle, strArtist: Three outputs, each a string, inputted by the user to be used by other functions. 
        """
        strID = input('Enter ID Number: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, strArtist

# -- DATA PROCESSING -- #
class DataProcessor:
    """Processing the data in memory"""
    
    @staticmethod
    def add_album(lstInput, table):
        """Function to add a user-inputted line item to 2D data structure in memory

        Adds a dict to a 2D data structure (list of dicts) after processing user input.
        
        Args:
            lstInput (list): three item list inputted by the user to but inputted as [0]: ID, [1]: Album, and [2]: Artist.

        Returns:
            blnCDRemoved: True if a line was removed from the table, False if nothing was removed.
        """
        dicRow = {'ID': int(lstInput[0]), 'Title': lstInput[1], 'Artist': lstInput[2]}
        table.append(dicRow)
        
    @staticmethod
    def delete_album(intIDDel, table):
        """Function to remove a specified item from a 2D data structure in memory

        Searches for and removes a dict from the list of dicts stored in memory, with the user inputting which
        item to search for.
        
        Args:
            intIDDel (int): Int inputted by the user, to iterate over the list searching for in the 'ID' value. 

        Returns:
            blnCDRemoved: True if a line was removed from the table, False if nothing was removed.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del table[intRowNr]
                blnCDRemoved = True
                break
        return(blnCDRemoved)

# -- FILE PROCESSING -- #
class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage pickled data ingestion from file to a list of dictionaries

        Reads the pickled data from file identified by file_name into a 2D table, then returns
        that table to be saved into a variable.

        Args:
            file_name (string): name of file used to read the data from

        Returns:
            None.
        """
        try:
            with open(file_name, 'rb') as fileObj:
                data = pickle.load(fileObj)
            return data
        except FileNotFoundError:
            print("The file {} could not be loaded".format(file_name))

    @staticmethod
    def write_file(file_name, table):
        """Function to manage data exporting from the list of tables in memory to a file

        Pickles the data in the 2D table, and saves it to the file specified by the argument file_name.
        
        Args:
            file_name (string): name of file used to write pickled the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        try:
            with open(file_name, 'wb') as fileObj:
                pickle.dump(table, fileObj)
        except FileNotFoundError:
            print("The file {} could not be saved".format(file_name))

# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(strFileName)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    
    # 3.1 process exit first
    if strChoice == 'x':
        break
    
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled.\n')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstTbl = FileProcessor.read_file(strFileName)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # 3.3.2 Add item to the table
        DataProcessor.add_album(IO.input_album(), lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
        
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        # 3.5.2 search thru table and delete CD
        blnCDRemoved = DataProcessor.delete_album(int(input('Which ID would you like to delete? ').strip()), lstTbl)

        if blnCDRemoved:
            print('The CD was removed.')
        else:
            print('Could not find this CD!')
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
        
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')



