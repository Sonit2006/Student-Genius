import tkinter as tk
from tkinter import ttk
from time import sleep
from PIL import ImageTk, Image
from mysql.connector import connect
from datetime import datetime, timedelta, date as dt
from tkcalendar import DateEntry
import QnA #contains all questions and answers for the help menu
from webbrowser import open as open_file
import configparser

#basic configuration
root = tk.Tk()
screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
root.geometry("{}x{}".format(screenWidth, screenHeight))
win = tk.Frame(root, bg="blue")
win.place(x= 0, y= 0, width=screenWidth, height = screenHeight)
config = configparser.ConfigParser()
config.read("C:/Users/Sonit Maddineni/Documents/config.ini")
mydb = connect(
  host = "localhost" ,
  user = config.get('mysql', 'user'),
  password = config.get('mysql', 'password'),
  database = "nchs"
  )
cur = mydb.cursor(buffered=True)
click_count = 0

#opening images
logo = ImageTk.PhotoImage(Image.open("C://Users/Sonit Maddineni/Documents/ProjectPy/files/logo.png"))
icon = ImageTk.PhotoImage(Image.open("C://Users/Sonit Maddineni/Documents/ProjectPy/files/icon.png").resize((200,50)))
searchGlass = ImageTk.PhotoImage(Image.open("C://Users/Sonit Maddineni/Documents/ProjectPy/files/searchglass.png").resize((40,30)))

#placing the logo on the frame
logo_label = tk.Label(win, image = logo, bg="blue")
logo_label.place(x=(screenWidth/2)-300, y = (screenHeight/2)-350)

name = tk.Label(win, text="Student Genius", font=("Algerian", 30), bg="blue", fg="gold")
name.place(x=(screenWidth/2)-120, y = (screenHeight/2)-70)
root.update()
sleep(1)
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')

#setting up a progressbar
load = ttk.Progressbar(win, style="red.Horizontal.TProgressbar", orient="horizontal",
                length=400, mode="indeterminate", maximum=4, value=1)
load.place(x = (screenWidth/2)-170, y = (screenHeight/2)+50)

#loading the progrssbar
load.start(200)
for i in range(15):
    root.update()
    sleep(0.2)

#navigating to next screen and setting up the widgets
def home():
    for widgets in win.winfo_children():
      ```
        if 'iconBtn' in dir():
            if widgets != iconBtn and widgets != help_btn:
                widgets.destroy()
        else:
            widgets.destroy()
       ```

    win.config(bg = "#11635b")
    
    #opens a help menu
    def help():
        global click_count
        def close():
            global click_count
            window.pack_forget()
            click_count -= 1
        if click_count == 0:
            click_count += 1
            window = tk.Frame(win, width=500, height=750, bg="light gray")
            window.pack(side=tk.RIGHT)
            tk.Button(window, text="close", command= close).place(x = 0, y = 10)
            tk.Label(window, text="Help", font=("Comic sans ms", 20),justify="center").place(x = 200, y = 10)
            quest = [QnA.Qview, QnA.Qedit, QnA.Qhome, QnA.Qwins, QnA.Qreport]
            ans = ['QnA.view', 'QnA.edit', 'QnA.home', 'QnA.wins', 'QnA.report']
            for i in range(5):
                dropdown = ttk.Combobox(window, values=[eval(ans[i]), eval(ans[i]+"2")], state="readonly", width=50)
                dropdown.place(x = 50, y = 100+(50*i))
                dropdown.set(quest[i])
        
        #making a label and a link to the documentation
        tk.Label(window, text= "For more information, see the documentation:", font=("Arial", 12), bg="light gray").place(x=50, y=400)
        docLink = tk.Label(window, text="Student Genius Documentation", fg="blue", font=("Arial", 12, 'underline'), bg="light gray")
        docLink.place(x = 50, y = 420)
        docLink.bind('<Enter>', lambda e: docLink.config(font=("arial", 12)))
        docLink.bind('<Leave>', lambda e: docLink.config(font=("arial", 12, "underline")))
        docLink.bind('<Button-1>', lambda e: open_file("https://sonitmaddineni.slite.com/app/channels/Ty3s3JRz943Bx8"))


    """allows to update the student points"""
    
    def Update():
        for widgets in win.winfo_children():
            if widgets != iconBtn and widgets != help_btn:
                widgets.destroy()

        #updates the database after he enters the Name, date and activitie and clicks the submit button
        def submit():
            if idMenu.get() == "" or idMenu.get() == "Search":
                nameFrame.config(bg = "red")
                nameFrame.update()
                sleep(.2)
                nameFrame.config(bg = "white")
                nameFrame.update()
            elif 1 not in (a.get(),b.get(),c.get(),d.get(),e.get(),f.get(),g.get(),h.get(),i.get(),j.get()):
                activity.config(bg = "red")
                activity.update()
                sleep(.2)
                activity.config(bg = "white")
                activity.update()
            else:
                count = [a.get(), b.get(), c.get(), d.get(), e.get() ,f.get() ,g.get() , h.get() ,i.get() ,j.get()].count(1)
                activitie = {'a':fbla, 'b':math, 'c':mun, 'd':mocktrial, 'e':spanish ,'f':wresting ,'g':swim , 'h':soccer ,'i':football ,'j':track }
                cur.execute("SELECT Points FROM nchs.track WHERE ID = '{}'".format(idMenu.get()))
                
                point1 = [i[0] for i in cur]
                #updates the points for the student
                cur.execute("UPDATE nchs.track SET Points = (Points + {}) WHERE (ID = {})".format(count*10, idMenu.get()))
                mydb.commit()
                #stores the activities that were checked on that date in another table.
                for item in activitie:
                    if eval(item).get() == 1:
                        cur.execute("INSERT INTO nchs.date (studentID, date, activity) VALUES ('{}','{}','{}')".format(idMenu.get(), str(cal.get_date()), str(activitie[item]["text"])))
                        mydb.commit()
    
                cur.execute("SELECT Points FROM nchs.track WHERE ID = '{}'".format(idMenu.get()))
                point2 = [i[0] for i in cur]
                tk.Label(parent, text= idMenu.get() + " points updated successfully!\n{} points to {}".format(point1[0],point2[0]), font=("Algerian", 15), bg="#11635b", fg="yellow").grid(row=5, column=0, pady=10)           
                idMenu.set("Search")
                for var in [fbla, math, mun, mocktrial, spanish, wresting, swim, soccer, football, track]:
                    var.deselect()
            


        # Create A Main Frame for the update screen
        main_frame = tk.Frame(win)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Create A Canvas
        screenCanvas = tk.Canvas(main_frame, bg="#11635b")
        screenCanvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        screenScroll = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=screenCanvas.yview)
        screenScroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure The Canvas
        screenCanvas.configure(yscrollcommand=screenScroll.set)
        screenCanvas.bind('<Configure>', lambda e: screenCanvas.configure(scrollregion = screenCanvas.bbox("all")))

        # Create ANOTHER Frame INSIDE the Canvas
        parent = tk.Frame(screenCanvas, bg="#11635b", width=screenWidth, height=screenHeight)

        # Add that New frame To a Window In The Canvas
        screenCanvas.create_window((0,0), window=parent, anchor="nw")
        iconButton = tk.Button(parent, image=icon, bg = "#11635b", borderwidth=0, activebackground="#11635b", command=home)
        iconButton.place(x = 0, y = 0)

        iconButton.bind('<Enter>', lambda e: iconButton.config(bg="#93089d"))
        iconButton.bind('<Leave>', lambda l: iconButton.config(bg="#11635b"))

        #inserting frames for the three actions
        tk.Label(parent, text="Update", bg="#11635b", font=("lucida calligraphy", 30), fg= "gold").grid(row=0, column=0, padx=300, pady = 20)

        nameFrame = tk.Frame(parent, bg="white", width=1000, height=250)
        nameFrame.grid(row=1, column = 0, padx=200, pady=10) 

        activity = tk.Frame(parent, bg="white",width=1000, height=250)
        activity.grid(row=4, column = 0, padx=200, pady=10)

        date = tk.Frame(parent, bg="white", width=1000, height=250)
        date.grid(row=3, column = 0, padx=200, pady=10)

        #space label
        tk.Label(parent, font=("comic sans ms", 50), bg="#11635b").grid(row=6, column=0, pady=40)

        #Name selection 
        cur.execute("SELECT ID FROM nchs.track")
        tk.Label(nameFrame, text="Student ID: ", font = ("comic sans ms", 15, "bold"), bg="white", fg = "#11635b").place(x=10,y=10)
        idMenu = ttk.Combobox(nameFrame, values=[name[0] for name in cur], width=25,font=("Georgia", 20))
        idMenu.set('Search')
        idMenu.place(x=10, y=80)
        idMenu.bind("<KeyRelease>", lambda e: [cur.execute("SELECT ID FROM nchs.track"), idMenu.config(values = [Id[0] for Id in cur if idMenu.get() in str(Id[0])])])
        Name = tk.Label(nameFrame, font = ("comic sans ms", 13), bg="white", fg = "blue")
        

        #date selection
        tk.Label(date, text="Select the date of attendance: ", font = ("comic sans ms", 15, "bold"), bg="white", fg = "#11635b").place(x=10,y=10)
        cal = DateEntry(date, width= 26, background= "magenta3", foreground= "white",bd=2, mindate = dt.today() + timedelta(days=-7), maxdate = dt.today())
        cal.place(x=10, y = 60)

        tk.Button(activity, text="Submit", command=submit).place(x=10, y=200)

        #Activity Selection
        tk.Label(activity, text="Select the activity attended: ", font = ("comic sans ms", 15, "bold"), bg="white", fg = "#11635b").place(x=10,y=10)

            #checkbuttons and their variables to store those values
        a, b, c, d, e, f, g, h, i, j = tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar(),tk.IntVar()
        fbla = tk.Checkbutton(activity, text="FBLA", bg="white", activebackground="white", fg="#11635b", selectcolor="gold", font=("Georgia", 12), variable=a)
        fbla.place(x=10, y = 50)

        math = tk.Checkbutton(activity, text="Math", bg="white", activebackground="white", fg="#11635b", selectcolor="gold", font=("Georgia", 12), variable=b)
        math.place(x=10, y = 90)

        mun = tk.Checkbutton(activity, text="Model UN", bg="white", activebackground="white", fg="#11635b", selectcolor="gold", font=("Georgia", 12), variable=c)
        mun.place(x=10, y = 130)

        mocktrial = tk.Checkbutton(activity, text="Mock Trial", bg="white", activebackground="white", fg="#11635b", selectcolor="gold", font=("Georgia", 12), variable=d)
        mocktrial.place(x=150, y = 50)

        spanish = tk.Checkbutton(activity, text="Spanish club", bg="white", activebackground="white", fg="#11635b", selectcolor="gold", font=("Georgia", 12), variable=e)
        spanish.place(x=150, y = 90)

        wresting = tk.Checkbutton(activity, text="Wrestling meet", bg="white", activebackground="white", fg="#11635b", selectcolor="gold", font=("Georgia", 12), variable=f)
        wresting.place(x=150, y = 130)

        swim = tk.Checkbutton(activity, text="Swim Meet", bg="white", activebackground="white", fg="#11635b", selectcolor="gold", font=("Georgia", 12), variable=g)
        swim.place(x=290, y = 50)

        soccer = tk.Checkbutton(activity, text="soccer meet", bg="white", activebackground="white", fg="#11635b", selectcolor="gold", font=("Georgia", 12), variable=h)
        soccer.place(x=290, y = 90)

        football = tk.Checkbutton(activity, text="Football meet", bg="white", activebackground="white", fg="#11635b", selectcolor="gold", font=("Georgia", 12), variable=i)
        football.place(x=290, y = 130)

        track = tk.Checkbutton(activity, text="Track", bg="white", activebackground="white", fg="#11635b", selectcolor="gold", font=("Georgia", 12), variable=j)
        track.place(x=430, y = 50)

        #checks if the activities were already checked under the same name and date when the name and date are selected.
        def selected(event):
            if idMenu.get() != "Search":
                cur.execute("SELECT Name FROM nchs.track WHERE ID = {}".format(int(idMenu.get())))
                Name.config(text = [name[0] for name in cur][0])
                Name.place(x=10,y=140)
                for var in [fbla, math, mun, mocktrial, spanish, wresting, swim, soccer, football, track]:
                    var.config(state=tk.NORMAL)
                for var in [fbla, math, mun, mocktrial, spanish, wresting, swim, soccer, football, track]:
                    cur.execute("SELECT activity FROM nchs.date WHERE studentID = {} and date = '{}'".format(idMenu.get(), str(cal.get_date())))
                    
                    for item in cur:
                        if var.cget("text") == item[0]:
                            var.config(state=tk.DISABLED)

        #binding the above function to when the widgets are selected.        
        idMenu.bind('<<ComboboxSelected>>', selected)
        cal.bind('<<DateEntrySelected>>', selected)

        


    """function to view the standings and student points (Second page after loading)"""
    def view():
        for widgets in win.winfo_children():
            if widgets != iconBtn and widgets != help_btn:
                widgets.destroy()

        #opens and closes the search bar when the search button is clicked
        def animate_search_bar():
            student_search.place(x = (screenWidth/2)-160, y = 120)
            if student_search['width'] == 0:
                for i in range(7):
                    student_search.config(width=i*10, fg="gray")
                    win.update()
                    sleep(0.009)
                student_search.insert(0, 'Search a student status')
            else:
                student_search.delete(0, tk.END)
                for i in range(7, -1, -1):
                    student_search.config(width=i*10)
                    win.update()
                    sleep(0.009)
                student_search.place_forget()
                display_list.place_forget()
        
        #displays the selected student from the list
        def display(event):
            element = display_list.get(display_list.curselection()[0])
            display_list.delete(0, tk.END)
            display_list.insert(tk.END, element)
            display_list.config(height=1)
        
        scroll_list = tk.Scrollbar(win, orient=tk.VERTICAL)
        display_list = tk.Listbox(win, font=("comic sans ms", 11), fg="blue", yscrollcommand=scroll_list.set, width=70)
        display_list.bind('<Double-Button>', display)
        
        #searches for the student when entered
        def search(event):
            if student_search['width'] != 0:
                if display_list.size() < 10:
                    display_list.config(height=display_list.size())
                else:
                    display_list.config(height = 10)
                display_list.delete(0, tk.END)
                display_list.place_forget()
                cur.execute("SELECT Name FROM nchs.track")
                names = [name for name in cur]
                for name in names:
                    if student_search.get().upper() in name[0]:
                        cur.execute("SELECT Name, Grade, Points FROM nchs.track WHERE Name = '{}'".format(name[0]))
                        for info in cur:
                            display_list.insert(tk.END, str(info[0]) + " "*(42-len(info[0])) + str(info[1]) + " "*(42-len(str(info[1]))) + str(info[2]))
                            display_list.place(x=(screenWidth/2)-200, y = 160)
                            scroll_list.config(command=display_list.yview)
                            scroll_list.pack(side=tk.RIGHT, fill= "y")
                if display_list.size() < 10:
                    display_list.config(height=display_list.size())
                else:
                    display_list.config(height = 10)
        #displays the winners for the current quarter when winners button is clicked
        def show_winners():
            winner = tk.Tk()
            winner.config(bg="#11635b")
            now = datetime.now().strftime("%m")
            for i, num in enumerate([11, 1, 4]):
                if int(now) >= num and int(now) <= num+2:
                    text = "Winners for Quarter " + str(i+1) 
                    break
            tk.Label(winner, text=text, font=("lucida calligraphy", 30), bg="#11635b", fg='gold').place(x = (screenWidth/2)-200,y = 10)
            tk.Label(winner, text="Title\t\t     Name\t\t\tGrade\t\t       Points\t\tPrizes", font=("Comic Sans ms", 12, "bold"), bg="#11635b", fg = "gold").place(x = 435,y = 170)
            titles = tk.Listbox(winner, justify="center", font=("Georgia", 12))
            titles.place(x = 350, y = 200)

            names = tk.Listbox(winner, justify="center", font=("Georgia", 12))
            names.place(x = 550, y = 200)
            
            grade = tk.Listbox(winner, justify="center", font=("Georgia", 12))
            grade.place(x = 750, y = 200)

            point = tk.Listbox(winner, justify="center", font=("Georgia", 12))
            point.place(x = 950, y = 200)

            prize = tk.Listbox(winner, justify="center", font=("Georgia", 12))
            prize.place(x = 1150, y = 200)

            randWinnerTitles = tk.Listbox(winner, justify="center", font=("Georgia", 12), width=30)
            randWinnerTitles.place(x = 350, y = 500)
            
            randWinnerNames = tk.Listbox(winner, justify="center", font=("Georgia", 12), width=30)
            randWinnerNames.place(x = 650, y = 500)
            
            randWinnerGrade = tk.Listbox(winner, justify="center", font=("Georgia", 12), width=30)
            randWinnerGrade.place(x = 950, y = 500)
            
            cur.execute("SELECT Name FROM nchs.data")
            randWins = [name[0][1:] for name in cur if name[0][1:].isupper()]
            cur.execute("SELECT Name FROM nchs.data")
            prizes = [name[0][1:] for name in cur]
            prizes = prizes[4:]
            print(prizes)
            title_list = ["Top point accumulation", "Grade 9 winner", "Grade 10 winner", "Grade 11 winner", "Grade 12 winner"]
            sqls = ["SELECT  Name, Grade, winners FROM track t1 WHERE winners = (SELECT MAX(winners) FROM track t)", "SELECT Name, Grade, winners FROM nchs.track WHERE Grade = 9 AND winners = (SELECT MAX(winners) FROM nchs.track WHERE Grade = 9)", "SELECT Name, Grade, winners FROM nchs.track WHERE Grade = 10 AND winners = (SELECT MAX(winners) FROM nchs.track WHERE Grade = 10)", "SELECT Name, Grade, winners FROM nchs.track WHERE Grade = 11 AND winners = (SELECT MAX(winners) FROM nchs.track WHERE Grade = 11)", "SELECT Name, Grade, winners FROM nchs.track WHERE Grade = 12 AND winners = (SELECT MAX(winners) FROM nchs.track WHERE Grade = 12)"]

            rand_title_list = ["Grade 9 Lucky winner", "Grade 10 lucky winner", "Grade 11 lucky winner", "Grade 12 lucky winner", ""]
            sql_for_rand = ["SELECT  Name, Grade FROM track t1 WHERE Name = '{}'".format(randWins[0]), "SELECT  Name, Grade FROM track t1 WHERE Name = '{}'".format(randWins[1]), "SELECT  Name, Grade FROM track t1 WHERE Name = '{}'".format(randWins[2]), "SELECT  Name, Grade FROM track t1 WHERE Name = '{}'".format(randWins[3]), ""]
            
            #function to insert the winners and the details into a listbox which appears on the screen
            def insert_wins(title, sql, ListTitles, ListNames, ListGrades, ListPoints = None):
                for ind in range(5):
                    size = 0
                    ListTitles.insert(tk.END, title[ind])
                    
                    cur.execute(sql[ind])
                    
                    for info in cur:
                        if ListPoints is not None:
                            if info[2] != 0:
                                size += 1
                                ListNames.insert(tk.END, info[0])
                                ListGrades.insert(tk.END, info[1])
                                ListPoints.insert(tk.END, info[2])
                                
                        else:
                            size += 1
                            ListNames.insert(tk.END, info[0])
                            ListGrades.insert(tk.END, info[1])
                    if ListPoints is not None:       
                        prize.insert(tk.END, prizes[ind])
                        
                    ListNames.insert(tk.END, "")
                    ListGrades.insert(tk.END, "")
                    if ListPoints is not None:
                        ListPoints.insert(tk.END, "")
                    
                    for i in range(size):
                        ListTitles.insert(tk.END, "")
                        prize.insert(tk.END, "")
                ListNames.config(height=names.size())
                ListGrades.config(height=grade.size())
                if ListPoints is not None:
                    ListPoints.config(height=point.size())
                ListTitles.config(height=names.size())
                prize.config(height=names.size())
            
            insert_wins(title_list, sqls, titles, names, grade, point)
            insert_wins(rand_title_list, sql_for_rand, randWinnerTitles, randWinnerNames, randWinnerGrade)

        #initializing the view screen with the widgets      
        tk.Label(win, text="Standings", bg="#11635b", font=("lucida calligraphy", 30), fg= "gold").place(x = (screenWidth/2)-100, y = 20)
        searchImg = tk.Button(win, image=searchGlass, bg="#11635b", activebackground="#11635b", borderwidth=0, command=animate_search_bar)
        searchImg.place(x = (screenWidth/2)-200, y = 120)

        student_search = tk.Entry(win, width = 0, font=('Georgia', 12), fg="gray")
        student_search.config(width=0)
        student_search.bind('<Button-1>', lambda e: [student_search.delete(0, tk.END), student_search.config(fg="black")])
        student_search.bind('<Key>', search)

        captions = tk.Label(win, font=("Georgia", 14), text="Name\t\t\t\tGrade\t\t\t\tPoints", bg="#11635b", fg = "gold")
        captions.place(x=250, y=(screenHeight/2)-60)

        nameList = tk.Listbox(win, bg="black", font=("comic sans ms", 13),borderwidth=0, width=40, fg="white")
        nameList.place(x = 100, y = (screenHeight/2)-30)

        gradeList  = tk.Listbox(win, bg="black", font=("comic sans ms", 13),borderwidth=0, width = 40, justify='center', fg="white")
        gradeList.place(x = 500, y = (screenHeight/2)-30)

        pointList = tk.Listbox(win, bg="black", font=("comic sans ms", 13),borderwidth=0, width = 40, justify = 'center', fg="white")
        pointList.place(x = 900, y = (screenHeight/2)-30)

        #displays students with top three highest scores
        cur.execute("SELECT Name, Grade, Points FROM nchs.track ORDER BY Points DESC")
        count = 0
        for detail in cur:
            if count < 3:
                nameList.insert(tk.END, "")
                nameList.insert(tk.END, "       " + str(count + 1) + ['st', 'nd','rd'][count] + "              " +  detail[0])

                gradeList.insert(tk.END, "")
                gradeList.insert(tk.END, detail[1])

                pointList.insert(tk.END, "")
                pointList.insert(tk.END, detail[2])
                count+=1
            else:
                break
        
        #buttons
        report_generator = tk.Button(win, text="Generate report", width=25, height=1, font=("Lucida Calligraphy", 8), command= lambda: open_file("C:/Users/Sonit Maddineni/Documents/ProjectPy/studentGenuis/Report.xlsx"))
        report_generator.place(x = 250, y = (screenHeight/2)+250)

        winners = tk.Button(win, text="Winners", width=25, height=1, font=("Lucida Calligraphy", 8), command=show_winners)
        winners.place(x = 900, y = (screenHeight/2)+250)

    #Initializing the first page after loading
    iconBtn = tk.Button(win, image=icon, bg = "#11635b", borderwidth=0, activebackground="#11635b", command=home)
    iconBtn.place(x = 0, y = 0)

    iconBtn.bind('<Enter>', lambda e: iconBtn.config(bg="#93089d"))
    iconBtn.bind('<Leave>', lambda l: iconBtn.config(bg="#11635b"))

    help_btn = tk.Button(win, text="HELP", font = ("Georgia", 15), borderwidth=0, command=help)
    help_btn.place(x = screenWidth-100, y = 10)

    edit_btn = tk.Button(win, text="Update", bg="gold", width=15, height=2, font=("Lucida Calligraphy", 15, "bold"), command=Update)
    edit_btn.place(x = (screenWidth/2)-90, y = (screenHeight/2)-200)

    view_btn = tk.Button(win, text="View", bg="gold", width=15, height=2, font=("Lucida Calligraphy", 15, "bold"), command=view)
    view_btn.place(x = (screenWidth/2)-90, y = (screenHeight/2)-100)

home()

root.mainloop()
