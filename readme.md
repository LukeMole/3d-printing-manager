    # 3D PRINT MANAGER
    #### Video Demo:  https://youtu.be/xcqsBl0PNIo
    ### Description:
    the program will be a 3D printing management software that utilises a GUI using the tkinter libraries in python. it will include functionality such as a counter for profit, income and expenses, it will be able to create new orders that need to be fulfilled and new expenses for things that need to be bought for the business. you will also be able to view past completed orders and expenses.

    the program will be flexible so you will be able to add or remove filament types, print types and colors. it will auto fill information such as order place date and order complete date. you will also be able to edit pending orders in case there was a mistake but you will not be able to edit completed orders or expenses as those are important and should not be edited.

    the program utilises multiple files to organise data and store everything effectively. the colors.txt file contains all information of the colors available for prints, the filaments.txt contains all information for available filaments that you can choose, income_expenses.csv contains all information on completed orders and expenses, inoutprofit.txt just tracks the income and expense amount, pending_orders.csv saves all current pending orders and prints.csv contains the name of available prints and their price.

    I couldve used databases or consolidated colors.txt, filaments.txt and prints.csv but i believe that is above the scope of the project and wouldve taken far too long.

    while the program couldve been a command line program i wanted to challenge myself and make something with a GUI, as command line programs are not very common in todays world.