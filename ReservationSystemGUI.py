from tkinter import *
import pymysql
import urllib.request
import base64
from tkinter import messagebox
import datetime
import time
from datetime import date

class GUI:

    def __init__(self):
        self.ticketsList = []
        self.tickets2List = []
        self.currentIndex = 0
        self.connect()
        self.loginPage()

    def connect(self):
        try:
            self.db = pymysql.connect(host="DATABASE SERVER",user="USERNAME",passwd = "PASSWORD",db="DATABASE NAME")
            self.c = self.db.cursor()
            return self.db
        except:
            messagebox.showwarning("Warning","Please check your internet connection and try again!")

    def loginPage(self):
        self.rootWin = Tk()
        self.rootWin.title("Login")
        self.cardPage = Toplevel()
        self.cardPage.withdraw()
        self.ticketsPage = Toplevel()
        self.ticketsPage.withdraw()
        response = urllib.request.urlopen("http://www.cc.gatech.edu/classes/AY2015/cs2316_fall/codesamples/techlogo.gif")
        self.image = response.read()
        self.b64_data = base64.encodebytes(self.image)
        self.photo = PhotoImage(data=self.b64_data)
        self.pic = Label(self.rootWin, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=4)
        Label(self.rootWin, text="GTTrain.com", font=("Times New Roman", 18)).grid(row=1,column=0,columnspan=3,sticky=E+W)
        Label(self.rootWin, text="Username").grid(row=2,column=0,sticky=E)
        Label(self.rootWin, text="Password").grid(row=3,column=0,sticky=E)
        self.usernameLogin = Entry(self.rootWin,width=30)
        self.usernameLogin.grid(row=2,column=1,columnspan=2,sticky=E+W)
        self.passwordLogin = Entry(self.rootWin,width=30)
        self.passwordLogin.grid(row=3,column=1,columnspan=2,sticky=E+W)
        self.registerButton = Button(self.rootWin, text="Register", command=self.registerPage)
        self.registerButton.grid(row=4,column=1,sticky=E+W)
        self.loginButton = Button(self.rootWin, text="Login", command=self.login)
        self.loginButton.grid(row=4,column=2,sticky=E+W)
        self.rootWin.mainloop()

    def registerPage(self):
        self.rootWin.withdraw()
        self.regWin = Toplevel()
        self.regWin.title("New User Registration")
        Label(self.regWin, text="New User Registration", font=("Times New Roman", 18)).grid(row=0,column=0,columnspan=4,sticky=E+W)
        Label(self.regWin,text="Username").grid(row=1,column=0,sticky=W)
        Label(self.regWin,text="Email Address").grid(row=2,column=0,sticky=W)
        Label(self.regWin,text="Password").grid(row=3,column=0,sticky=W)
        Label(self.regWin,text="Confirm Password").grid(row=4,column=0,sticky=W)
        self.userEntry = Entry(self.regWin,width=30,state="normal")
        self.userEntry.grid(row=1,column=1)
        self.emailEntry = Entry(self.regWin,width=30,state="normal")
        self.emailEntry.grid(row=2,column=1)
        self.password1Entry = Entry(self.regWin,width=30,state="normal")
        self.password1Entry.grid(row=3,column=1)
        self.password2Entry = Entry(self.regWin,width=30,state="normal")
        self.password2Entry.grid(row=4,column=1)
        self.officialRegisterButton = Button(self.regWin,text="Create",width = 15,command=self.registerNew)
        self.officialRegisterButton.grid(row=5,column=1)

    def registerNew(self):
        database=self.connect()
        self.user=self.userEntry.get()
        self.pass1=self.password1Entry.get()
        self.pass2=self.password2Entry.get()
        self.email=self.emailEntry.get()
        if self.pass1 != self.pass2:
            messagebox.showwarning("Warning!","Passwords Do Not Match")
            return
        elif self.user=="" or self.pass1=="" or self.pass2=="":
            messagebox.showwarning("Hey!","Fill in Blanks")
            return
        cursor=database.cursor()

        #### CHECKING IF USER EXISTS IN THE DATABASE
        cursor1=cursor.execute("SELECT * FROM User WHERE Username=%s",(self.user))
        cursor2=cursor.execute("SELECT * FROM Customer WHERE Email=%s",(self.email))
        if cursor1!=0:
           messagebox.showwarning("What?!","Username Already in Database!")
        elif cursor2!=0:
           messagebox.showwarning("What?!","Email Already in Database!")
        else:
            #### INSERTING THE USER INTO THE DATABASE
            userInsert = ("INSERT INTO User(Username,Password) VALUES (%s,%s)")
            cursor.execute(userInsert,(self.user,self.pass1))
            customerInsert= ("INSERT INTO Customer(Username,Email) VALUES (%s,%s)")
            cursor.execute(customerInsert,(self.user,self.email))
            database.commit()
            messagebox.showinfo("New User Registered!", "The new user has been registered!!")
            self.regWin.withdraw()
            self.rootWin.deiconify()

    def login(self):
        self.removeVar = IntVar()
        self.removeVar.set(10000)
        database=self.connect()
        cursor=database.cursor()
        self.username=self.usernameLogin.get()
        self.password=self.passwordLogin.get()
        #### CHECKING WHICH TYPE OF USER THE LOGGED IN USER IS
        managercursor=cursor.execute("SELECT * FROM Manager WHERE Username=%s",(self.username))
        customercursor=cursor.execute("SELECT * FROM User WHERE Username=%s and Password=%s",(self.username,self.password))
        if managercursor !=0:
            mngrcursor=cursor.execute("Select * FROM User Where Username=%s and Password=%s",(self.username,self.password))
            if mngrcursor !=0:
              self.managerPage()
            else:
                messagebox.showwarning("Error","Username or Password Not Found")
        elif customercursor!=0:
            self.customerPage()
        else:
              messagebox.showwarning("Error","Username or Password Not Found")

    def customerPage(self):
        self.rootWin.withdraw()
        self.custPage=Toplevel()
        self.pic = Label(self.custPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=4)
        self.custPage.title("Choose Functionality")
        self.viewButton = Button(self.custPage,text="View Train Schedule",width = 15,command=self.viewPage)
        self.viewButton.grid(row=1,column=1)
        self.makeButton=Button(self.custPage,text="Make a New Reservation",width = 15,command=self.makeReservationPage)
        self.makeButton.grid(row=2,column=1)
        self.updateButton=Button(self.custPage,text="Update a Reservation",width = 15,command=self.updateReservation)
        self.updateButton.grid(row=3,column=1)
        self.cancelButton = Button(self.custPage,text="Cancel a Reservation",width = 15,command=self.cancelReservation)
        self.cancelButton.grid(row=4,column=1)
        self.giveButton = Button(self.custPage,text="Give Review",width = 15,command=self.makegiveReviewPage)
        self.giveButton.grid(row=5,column=1)
        self.viewReviewButton = Button(self.custPage,text="View Reviews", width=15,command=self.makeViewReviews)
        self.viewReviewButton.grid(row=6,column=1)
        self.schoolButton = Button(self.custPage,text="Add School Info",width = 15,command=self.schoolPage)
        self.schoolButton.grid(row=7,column=1)
        self.logoutButton=Button(self.custPage,text="Log Out", width =5,command=self.logout)
        self.logoutButton.grid(row=7,column=2)

    def schoolPage(self):
        self.custPage.withdraw()
        self.schoolPage=Toplevel()
        self.pic = Label(self.schoolPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=4)
        self.schoolPage.title("Add School Info")
        Label(self.schoolPage,text="School Email Address").grid(row=1,column=0,sticky=W)
        self.schoolEmail = Entry(self.schoolPage,width=30,state="normal")
        self.schoolEmail.grid(row=1,column=1)
        Label(self.schoolPage,text="Must End with .edu").grid(row=2,column=0)
        self.backButton=Button(self.schoolPage,text="Back", width =5,command=self.back)
        self.backButton.grid(row=4,column=0)
        self.submitButton=Button(self.schoolPage,text="Submit",width=8, command=self.submit)
        self.submitButton.grid(row=4,column=1)

    def managerPage(self):
        self.rootWin.withdraw()
        self.managerWindow = Toplevel()
        self.managerWindow.title("Manager View")
        self.pic = Label(self.managerWindow, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=2)
        Label(self.managerWindow, text="Choose Functionality", font=("Times New Roman", 18)).grid(row=1, column=0, columnspan=2)
        revenue = Button(self.managerWindow, text='View Revenue Report', command=self.revenueReport)
        train = Button(self.managerWindow, text='View Popular Train Report', command=self.popularTrain)
        revenue.grid(row=2, column=0)
        train.grid(row=2, column=1)
        Button(self.managerWindow, text="Back", command=self.closeManager).grid(row=3, column=0, sticky=W)

    def closeManager(self):
        self.managerWindow.withdraw()
        self.rootWin.deiconify()

    def revenueReport(self):
        self.managerWindow.withdraw()
        self.revenue = Toplevel()
        self.revenue.title("Revenue Report")
        self.pic = Label(self.revenue, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=2)
        revenueInfo = []
        cursor=self.connect().cursor()
        monthlyRevenue = [0,0,0]
        currentMonth = datetime.datetime.now().month
        includedMonths = []
        for i in range(currentMonth-2, currentMonth+1):
            if i > 0:
                includedMonths.append(i)
            else:
                includedMonths.append(i+12)
        monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        revenues = []
        for i in includedMonths:
            #### RETURNS REVENUE REPORT VALUES FOR SELECTED MONTHS
            cursor.execute("Select SUM(Reservation.TotalCost) FROM Reservation INNER JOIN Reserves On Reservation.ReservationID=Reserves.ReservationID WHERE month(Reserves.DepartureDate)="+str(i))
            for x in cursor:
                revenues.append(x[0])
        for i in range(len(revenues)):
            if revenues[i] == None:
                revenues[i] = 0
            Label(self.revenue, text="$"+str("%.2f" %round(revenues[i], 2))).grid(row=i+2, column=1, sticky=W)
        Label(self.revenue, text="Month", font=("Times New Roman", 14, "bold")).grid(row=1, column=0, sticky=W)
        Label(self.revenue, text="Revenue", font=("Times New Roman", 14, "bold")).grid(row=1, column=1, sticky=W)
        for i in range(len(includedMonths)):
            Label(self.revenue, text=monthNames[includedMonths[i]-1]).grid(row=2+i, column=0, sticky=W)
        Button(self.revenue, text="Back", command=self.closeRev).grid(row=5, column=0)

    def popularTrain(self):
        cursor=self.connect().cursor()
        self.managerWindow.withdraw()
        self.popularWindow = Toplevel()
        self.popularWindow.title("Most Popular Trains")
        self.pic = Label(self.popularWindow, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=3)
        try:
            #### REGENERATES VIEWS EACH TIME THE BUTTON IS CLICKED, DROPS THE OLD ONE IF IT EXISTS
            self.c.execute("DROP VIEW TopMonths")
        except:
            pass
        try:
            self.c.execute("DROP VIEW TopTrains")
        except:
            pass
        cursor.execute("CREATE VIEW TopMonths AS SELECT month(DepartureDate) AS Month, TrainNumber, Count(R.ReservationID) AS  NumReservations FROM Reserves INNER JOIN Reservation R WHERE R.isCancelled = FALSE AND R.ReservationID=Reserves.ReservationID GROUP BY month(DepartureDate) LIMIT 3;")
        cursor.execute("CREATE VIEW TopTrains AS SELECT month(DepartureDate) AS Month, TrainNumber, Count(R.ReservationID) AS  NumReservations FROM Reserves INNER JOIN Reservation R WHERE isCancelled = FALSE AND R.ReservationID=Reserves.ReservationID GROUP BY TrainNumber LIMIT 3;")
        cursor.execute("SELECT * FROM TopMonths UNION SELECT * FROM TopTrains GROUP BY Month LIMIT 3;")
        months = ['January','February','March','April','May','June','July','August','September','October','November','December']
        monthInfo = []
        for x in cursor:
            monthInfo.append(x)
        i = 0
        while i < 3 and len(monthInfo) > i:
            Label(self.popularWindow, text=months[int(monthInfo[i][0])-1]).grid(row=i+2, column=0)
            Label(self.popularWindow, text=monthInfo[i][1]).grid(row=i+2, column=1)
            Label(self.popularWindow, text=monthInfo[i][2]).grid(row=i+2, column=2)
            i += 1
        trainReportMonth = Label(self.popularWindow, text="Month", font=("Times New Roman", 14, "bold"))
        trainReportName = Label(self.popularWindow, text="Train", font=("Times New Roman", 14, "bold"))
        trainReportFrequency = Label(self.popularWindow, text="Frequency", font=("Times New Roman", 14, "bold"))
        closeTrainReport = Button(self.popularWindow, text="Back", command=self.closePopularTrains)
        trainReportMonth.grid(row=1, column=0)
        trainReportName.grid(row=1, column=1)
        trainReportFrequency.grid(row=1, column=2)
        closeTrainReport.grid(row=5, column=0, columnspan=3)

    def closePopularTrains(self):
        self.popularWindow.withdraw()
        self.managerWindow.deiconify()

    def closeRev(self):
        self.revenue.withdraw()
        self.managerWindow.deiconify()

    def submit(self):
        database=self.connect()
        schoolEmail2=self.schoolEmail.get()
        if schoolEmail2[-4:] == ".edu":
          cursor=database.cursor()
          #### UPDATES USER INFO TO CONFIRM THAT HE/SHE IS A STUDENT
          cursor.execute("UPDATE Customer SET isStudent = TRUE WHERE Username=%s",(self.username))
          messagebox.showwarning("Success","You're a Student")
        else:
          messagebox.showwarning("Error","Not a School Email")

    def viewPage(self):
        self.custPage.withdraw()
        self.viewPage=Toplevel()
        self.viewPage.title("View Train Schedule")
        self.viewEntry=Entry(self.viewPage,width=30,state="normal")
        self.viewEntry.grid(row=1,column=1)
        Label(self.viewPage, text="Train Number").grid(row=1,column=0)
        self.pic = Label(self.viewPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=4)
        self.searchButton=Button(self.viewPage, text="Search",width=8,command=self.viewSchedule)
        self.searchButton.grid(row=2,column=0,stick=EW)

    def viewSchedule(self):
        db=self.connect()
        cursor=db.cursor()
        #### RETURNING TRAIN ROUTES
        cursor.execute("Select * FROM TrainRoute WHERE TrainNumber=%s",(self.viewEntry.get()))
        if cursor !=0:
          self.viewPage.withdraw()
          self.viewSched=Toplevel()
          self.viewSched.title("View Train Schedule")
          self.pic = Label(self.viewSched, image = self.photo)
          self.pic.grid(row = 0, column = 0, columnspan=4)
          Label(self.viewSched, text="Train Number").grid(row=1,column=0,sticky=E+W)
          Label(self.viewSched, text="Arrival Time").grid(row=1,column=1,sticky=E+W)
          Label(self.viewSched, text="Departure Time").grid(row=1,column=2,sticky=E+W)
          Label(self.viewSched, text="Station Location").grid(row=1,column=3,sticky=E+W)
          cursor.execute("SELECT TrainNumber,ArrivalTime,DepartureTime,Name,Location FROM Stop NATURAL JOIN Station WHERE TrainNumber = %s ORDER BY ArrivalTime",(self.viewEntry.get()))
          stops = cursor.fetchall()
          Button(self.viewSched, text = "Back", command = self.backView).grid(row=2+len(stops), column= 0)
          for i in range(len(stops)):
              for j in range(len(stops[i])):
                  if j != 4:
                      if j == 3:
                          txt = stops[i][4] + " (" + stops[i][j] + ")"
                      elif j == 0 and i != 0:
                          txt = ""
                      elif isinstance(stops[i][j], datetime.datetime):
                          txt = stops[i][j].strftime("%I:%M %p")
                      else:
                          txt = stops[i][j]
                      Label(self.viewSched, text= txt).grid(row = 2+i, column=j)
        else:
            messagebox.showwarning("Error","Train Number Not Found")

    def backView(self):
        self.viewSched.destroy()
        self.viewPage.destroy()
        self.custPage.deiconify()

    def makeReservationPage(self):
        self.custPage.withdraw()
        self.reservationPage=Toplevel()
        self.reservationPage.title("Make a New Reservation")
        self.pic = Label(self.reservationPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=2)
        Label(self.reservationPage, text="Search Train", font=("Times New Roman", 18)).grid(row=1,column=0,columnspan=2,sticky=E+W)
        Label(self.reservationPage, text="Departs From").grid(row = 2, column = 0)
        Label(self.reservationPage, text="Arrives At").grid(row =3, column = 0)
        Label(self.reservationPage, text="Departure Date").grid(row =4, column = 0)
        self.findTrainsButton = Button(self.reservationPage, text="Find Trains", command = self.findTrains)
        self.findTrainsButton.grid(row = 5, column=1, columnspan = 3, sticky=E+W)
        self.departDateEntry = Entry(self.reservationPage, width = 15, state="normal")
        self.departDateEntry.grid(row=4, column = 1)
        departureStops = []
        self.c.execute("SELECT Location,Name FROM Station")
        aTuples = self.c.fetchall()
        for i in range(len(aTuples)):
            departureStops.append(aTuples[i][0] + " (" + aTuples[i][1] + ")")
        self.departureVar = StringVar()
        self.departuredropdown = OptionMenu(self.reservationPage,self.departureVar,*departureStops)
        self.departuredropdown.grid(row = 2, column = 1, sticky = E+W)
        self.arrivalVar = StringVar()
        self.arrivaldropdown = OptionMenu(self.reservationPage,self.arrivalVar,*departureStops)
        self.arrivaldropdown.grid(row = 3, column = 1, sticky = E+W)

    def findTrains(self):
        if self.departureVar.get() == "" or self.arrivalVar.get() == "" or self.departureVar.get()==self.arrivalVar.get():
            messagebox.showwarning("Error","Please select a valid departure location and arrival location.")
            return
        else:
            try:
                self.departDateTime = datetime.datetime.strptime(self.departDateEntry.get(),"%m/%d/%Y")
            except:
                messagebox.showwarning("Error","Incorrect departure date. Please input a departure date in the format MM/DD/YYYY")
                return
            self.selectDeparturePage()

    def selectDeparturePage(self):
        self.reservationPage.withdraw()
        self.findTrainsPage =Toplevel()
        self.reservationPage.title("Select Departure")
        self.pic = Label(self.findTrainsPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=4)
        Label(self.findTrainsPage, text="Select Departure", font=("Times New Roman", 18)).grid(row=1,column=1,columnspan=2,sticky=E+W)
        Label(self.findTrainsPage, text="Train (Train Number)").grid(row=2,column=0,sticky=E+W)
        Label(self.findTrainsPage, text="Time (Duration)").grid(row=2,column=1,sticky=E+W)
        Label(self.findTrainsPage, text="1st Class Price").grid(row=2,column=2,sticky=E+W)
        Label(self.findTrainsPage, text="2nd Class Price").grid(row=2,column=3,sticky=E+W)
        self.depStopName = self.departureVar.get()[self.departureVar.get().index("(")+1:self.departureVar.get().index(")")]
        self.arrStopName = self.arrivalVar.get()[self.arrivalVar.get().index("(")+1:self.arrivalVar.get().index(")")]
        self.c.execute("CREATE OR REPLACE VIEW GoodArrivals AS SELECT TrainNumber, ArrivalTime FROM Stop NATURAL JOIN Station WHERE Name = '" + self.arrStopName + "'")
        self.c.execute("CREATE OR REPLACE VIEW GoodDeparts AS SELECT TrainNumber, DepartureTime FROM Stop NATURAL JOIN Station WHERE Name = '" + self.depStopName + "'")
        self.c.execute("CREATE OR REPLACE VIEW GoodTrains AS SELECT TrainNumber, DepartureTime, ArrivalTime FROM GoodArrivals A NATURAL JOIN GoodDeparts D WHERE TIMEDIFF(D.DepartureTime, A.ArrivalTime) < 0 GROUP BY TrainNumber")
        self.c.execute("SELECT TrainNumber, DepartureTime, ArrivalTime,TIMEDIFF(ArrivalTime, DepartureTime) AS Duration, FirstClassPrice, SecondClassPrice FROM TrainRoute NATURAL JOIN GoodTrains")
        goodTrains = self.c.fetchall()
        self.goodTrains = goodTrains
        self.selectedTicket = StringVar()
        self.selectedTicket.set("NOT SELECTED")
        for i in range(len(goodTrains)):
            Label(self.findTrainsPage, text=goodTrains[i][0]).grid(row=3+i,column=0)
            Label(self.findTrainsPage, text=goodTrains[i][1].strftime("%I:%M%p")+"-"+goodTrains[i][2].strftime("%I:%M%p")).grid(row=3+i,column=1)
            Radiobutton(self.findTrainsPage, text="$"+str(goodTrains[i][4]), variable=self.selectedTicket, value=(str(i)+","+"1")).grid(row=3+i,column=2)
            Radiobutton(self.findTrainsPage, text="$"+str(goodTrains[i][5]), variable=self.selectedTicket, value=(str(i)+","+"2")).grid(row=3+i,column=3)
        Button(self.findTrainsPage, text="Back", command=self.backToReservationPage).grid(row=3+len(goodTrains),column=0,sticky=E+W)
        Button(self.findTrainsPage, text="Next", command=self.makeTravelExtrasPage).grid(row=3+len(goodTrains),column=3,sticky=E+W)

    def makeTravelExtrasPage(self):
        self.findTrainsPage.withdraw()
        self.travelExtrasPage =Toplevel()
        self.travelExtrasPage.title("Travel Extras / Passenger Info")
        self.pic = Label(self.travelExtrasPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=2)
        Label(self.travelExtrasPage, text="Travel Extras & Passenger Info", font=("Times New Roman", 18)).grid(row=1,column=0,columnspan=2,sticky=E+W)
        Label(self.travelExtrasPage, text="Number of Baggage").grid(row=2,column=0,sticky=W)
        Label(self.travelExtrasPage, text="4 Bag Max. 2 Free of Charge. Next 2 are $30 per bag.").grid(row=3,column=0,columnspan=2,sticky=E+W)
        Label(self.travelExtrasPage, text="Passenger Name").grid(row=4,column=0,sticky=W)
        self.baggageNumVar = StringVar()
        self.baggageDropDown = OptionMenu(self.travelExtrasPage,self.baggageNumVar,"0","1","2","3","4")
        self.baggageDropDown.grid(row = 2, column = 1, sticky = E+W)
        self.passNameEntry=Entry(self.travelExtrasPage,width=30,state="normal")
        self.passNameEntry.grid(row=4,column=1)
        Button(self.travelExtrasPage, text="Back", command=self.backToFindTrains).grid(row=5,column=0,sticky=E+W)
        Button(self.travelExtrasPage, text="Next", command=self.setupTicket).grid(row=5,column=1,sticky=E+W)

    def setupTicket(self):
        if self.baggageNumVar.get() == "":
            messagebox.showwarning("Error!","Please input how many bags you will take on your trip!")
        else:
            if self.passNameEntry.get() == "":
                messagebox.showwarning("Error!","Please input your passenger name!")
            else:
                trainIndex = int((self.selectedTicket.get()).split(",")[0])
                if (self.selectedTicket.get()).split(",")[1] == "1":
                    classStr = "1st Class"
                    classIndex = 4
                else:
                    classStr = "2nd Class"
                    classIndex = 5
                ticket = []
                ticket2 = []
                ticket.append(Label(self.ticketsPage, text=self.goodTrains[trainIndex][0]))
                dDate = self.goodTrains[trainIndex][1].replace(day=self.departDateTime.day, month = self.departDateTime.month, year=self.departDateTime.year)
                aDate = dDate + (self.goodTrains[trainIndex][2].replace(day=1,month=1,year=2000) - self.goodTrains[trainIndex][1].replace(day=1,month=1,year=2000))
                ticket.append(Label(self.ticketsPage, text=dDate.strftime("%b %d %I:%M%p")+"-"+aDate.strftime("%b %d %I:%M%p")+ "\n" +str(aDate-dDate) + " Duration"))
                ticket.append(Label(self.ticketsPage, text=self.depStopName))
                ticket.append(Label(self.ticketsPage, text=self.arrStopName))
                ticket.append(Label(self.ticketsPage, text=classStr))
                ticket.append(Label(self.ticketsPage, text=self.goodTrains[trainIndex][classIndex]))
                ticket.append(Label(self.ticketsPage, text=self.baggageNumVar.get()))
                ticket.append(Label(self.ticketsPage, text=self.passNameEntry.get()))
                ticket.append(Radiobutton(self.ticketsPage,variable=self.removeVar, value=len(self.ticketsList)))
                self.currentIndex = self.currentIndex + 1
                self.ticketsList.append(ticket)
                ticket2.append(classIndex-3)
                ticket2.append(dDate)
                ticket2.append(int(self.baggageNumVar.get()))
                ticket2.append(self.depStopName)
                ticket2.append(self.arrStopName)
                ticket2.append(self.passNameEntry.get())
                ticket2.append(self.goodTrains[trainIndex][0])
                self.tickets2List.append(ticket2)
                self.makeTicketsPage()

    def removeTicket(self):
        self.ticketsList.remove(self.ticketsList[self.removeVar.get()])
        self.tickets2List.remove(self.tickets2List[self.removeVar.get()])
        for i in range(len(self.ticketsList)):
            self.ticketsList[i][8].config(value=i)
        for label in self.ticketsPage.winfo_children():
            label.grid_forget()
        self.makeTicketsPage()

   def makeTicketsPage(self):
        self.travelExtrasPage.withdraw()
        self.ticketsPage.deiconify()
        self.ticketsPage.title("Make Reservation Page")
        self.pic = Label(self.ticketsPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=8)
        Label(self.ticketsPage, text="Make Reservation", font=("Times New Roman", 18)).grid(row=1,column=0,columnspan=9,sticky=E+W)
        Label(self.ticketsPage, text="Currently Selected").grid(row=2,column=0,columnspan=2,sticky=W)
        Label(self.ticketsPage, text="Train(Train Number)").grid(row=3,column=0)
        Label(self.ticketsPage, text="Time (Duration)").grid(row=3,column=1)
        Label(self.ticketsPage, text="Departs From").grid(row=3,column=2)
        Label(self.ticketsPage, text="Arrives At").grid(row=3,column=3)
        Label(self.ticketsPage, text="Class").grid(row=3,column=4)
        Label(self.ticketsPage, text="Price").grid(row=3,column=5)
        Label(self.ticketsPage, text="# of Bags").grid(row=3,column=6)
        Label(self.ticketsPage, text="Passenger Name").grid(row=3,column=7)
        Button(self.ticketsPage, text="Remove", command=self.removeTicket).grid(row=3,column=8)
        if len(self.ticketsList) != 0:
            for i in range(len(self.ticketsList)):
                for j in range(len(self.ticketsList[0])):
                    self.ticketsList[i][j].grid(row=4+i,column=j)
            #### CHECKS FOR STUDENT STATUS
            self.c.execute("SELECT IsStudent FROM Customer WHERE Username = '" +self.username+ "'")
            a = self.c.fetchall()
            if a[0][0] == 1:
                Label(self.ticketsPage, text="Student Discount Applied.").grid(row=4+len(self.ticketsList),column=0,columnspan=2,sticky=W)
                self.isStudent = True
            else:
                Label(self.ticketsPage, text="No Student Discount Applied.").grid(row=4+len(self.ticketsList),column=0,columnspan=2,sticky=W)
                self.isStudent = False
            Label(self.ticketsPage, text="Total Cost").grid(row=5+len(self.ticketsList),column=0)
            self.totalcost = 0
            for ticket in self.ticketsList:
                price = ticket[5].cget("text")
                self.totalcost += price
                numBags = ticket[6].cget("text")
                numBags = int(numBags)
                if numBags > 2:
                    self.totalcost += (30*(numBags-2))
            if self.isStudent:
               self.totalcost = self.totalcost * .8
            Label(self.ticketsPage, text=str(self.totalcost)).grid(row=5+len(self.ticketsList),column=1)
            Label(self.ticketsPage, text="Use Card").grid(row=6+len(self.ticketsList),column=0)
            #### FINDS CREDIT CARD INFO FOR THE USER
            x = self.c.execute("SELECT CardNumber FROM PaymentInfo WHERE Username = '" + self.username + "'")
            self.cardList = []
            cards = self.c.fetchall()
            if x == 0:
                self.lastFourList= ["No Card Found"]
            else:
                for card in cards:
                    self.cardList.append(card[0])
                self.lastFourList = []
                for card in self.cardList:
                    self.lastFourList.append(card[-4:])
            self.cardVar = StringVar()
            self.selectedCardMenu = OptionMenu(self.ticketsPage, self.cardVar,*self.lastFourList)
            self.selectedCardMenu.grid(row=6+len(self.ticketsList),column=1,sticky=E+W)
            Button(self.ticketsPage, text="Add Card", command=self.makeCardPage).grid(row=6+len(self.ticketsList),column=2,sticky=W)
            Button(self.ticketsPage, text="Continue adding a train", command=self.newTrainPressed).grid(row=7+len(self.ticketsList),column=0,columnspan=2)
            Button(self.ticketsPage, text="Back", command=self.backFromMakeReservation).grid(row=8+len(self.ticketsList),column=0)
            Button(self.ticketsPage, text="Submit", command=self.payForReservation).grid(row=8+len(self.ticketsList),column=2)
        else:
            Button(self.ticketsPage, text="Back", command=self.backFromMakeReservation).grid(row=4,column=0)

    def payForReservation(self):
        if self.cardVar.get() != "" and self.cardVar.get() != "No Card Found":
            i = self.lastFourList.index(self.cardVar.get())
            cardNo = self.cardList[i]
            #### CHECKS FOR EXPIRED CREDIT CARD
            self.c.execute("SELECT ExpDate FROM PaymentInfo WHERE CardNumber = '" + str(cardNo) + "'")
            expD = self.c.fetchall()[0][0]
            if expD < datetime.datetime.now().date():
                messagebox.showwarning("Error","Your card is expired!")
            else:
                a = self.c.execute("SELECT MAX(ReservationID) FROM Reservation")
                b = self.c.fetchall()
                if b[0][0] == 0 or b[0][0] == None:
                    self.reservationNumber = 1000
                else:
                    self.reservationNumber = b[0][0]+1
                #### CREATES THE PAID RESERVATION IN THE SYSTEM
                self.c.execute("INSERT INTO Reservation VALUES(%s,%s,%s,%s,%s)",(self.username,self.reservationNumber,False,cardNo,self.totalcost))
                for ticket in self.tickets2List:
                    print("ticket[6] is: " + ticket[6])
                    self.c.execute("INSERT INTO Reserves VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(ticket[0],ticket[1],ticket[2],ticket[3],ticket[4],ticket[5],self.reservationNumber,ticket[6]))
                self.ticketsList = []
                self.tickets2List = []
                self.createConfirmationPage()
        else:
            messagebox.showwarning("Error","No Card selected as a payment option!")

    def createConfirmationPage(self):
        self.ticketsPage.withdraw()
        self.confirmationPage = Toplevel()
        self.confirmationPage.title("Confirmation")
        self.pic = Label(self.confirmationPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=3)
        Label(self.confirmationPage, text="Confirmation", font=("Times New Roman", 18)).grid(row=1,column=0,columnspan=3,sticky=E+W)
        Label(self.confirmationPage, text="Reservation ID").grid(row=2,column=0)
        Label(self.confirmationPage, text=str(self.reservationNumber)).grid(row=2,column=3)
        Label(self.confirmationPage, text="Thank you for your purchase! Please save this reservation ID for your records.").grid(row=3,column=0,columnspan=3,sticky=E+W)
        Button(self.confirmationPage, text="Go Back to choose functionality",command=self.backFromConfirmation).grid(row=4,column=0,columnspan=3,sticky=E+W)
        for label in self.ticketsPage.winfo_children():
            label.grid_forget()

    def backFromConfirmation(self):
        self.confirmationPage.destroy()
        self.customerPage()

    def backFromMakeReservation(self):
        self.ticketsPage.withdraw()
        for label in self.ticketsPage.winfo_children():
            label.grid_forget()
        self.customerPage()

    def newTrainPressed(self):
        self.ticketsPage.withdraw()
        for label in self.ticketsPage.winfo_children():
            label.grid_forget()
        self.makeReservationPage()

    def backFromCardPage(self):
        self.cardPage.withdraw()
        for label in self.ticketsPage.winfo_children():
            label.grid_forget()
        self.makeTicketsPage()

    def makeCardPage(self):
       self.ticketsPage.withdraw()
       self.cardPage.deiconify()
       self.cardPage.title("Payment Info")
       self.pic = Label(self.cardPage, image = self.photo)
       self.pic.grid(row = 0, column = 0, columnspan=2)
       Label(self.cardPage, text="Add Card").grid(row=1,column=0)
       Label(self.cardPage, text="Name on Card").grid(row=2,column=0)
       Label(self.cardPage, text="Card Number").grid(row=3,column=0)
       Label(self.cardPage, text="CVV").grid(row=4,column=0)
       Label(self.cardPage, text="Exp. Date (MM/YYYY)").grid(row=5,column=0)
       self.nameOnCard=Entry(self.cardPage,width=30,state="normal")
       self.nameOnCard.grid(row=2,column=1)
       self.cardNumber=Entry(self.cardPage,width=30,state="normal")
       self.cardNumber.grid(row=3,column=1)
       self.CVV=Entry(self.cardPage,width=30,state="normal")
       self.CVV.grid(row=4,column=1)
       self.expDate=Entry(self.cardPage,width=30,state="normal")
       self.expDate.grid(row=5,column=1)
       Label(self.cardPage, text="Delete Card").grid(row=1,column=2)
       Label(self.cardPage, text="Card Number").grid(row=2,column=2)
       Button(self.cardPage, text="Back", command=self.backFromCardPage).grid(row=7,column=0)
       x = self.c.execute("SELECT CardNumber FROM PaymentInfo WHERE Username = '" + self.username + "'")
       self.cardList2 = []
       cards = self.c.fetchall()
       if x == 0:
           self.addDelLastFourList= ["No Card Found"]
       else:
           for card in cards:
               self.cardList2.append(card[0])
           self.addDelLastFourList = []
           for card in self.cardList2:
               self.addDelLastFourList.append(card[-4:])
       self.cardVar2 = StringVar()
       self.cardVar2.set("No Card Found")
       self.dropCard = OptionMenu(self.cardPage, self.cardVar2,*self.addDelLastFourList)
       self.dropCard.config(width=20)
       self.dropCard.grid(row=2,column=3)
       self.submitPaymentInfoButton=Button(self.cardPage, text="Submit",width=10,command=self.submitPaymentInfo)
       self.submitPaymentInfoButton.grid(row=6,column=0)
       self.submitDeleteInfoButton=Button(self.cardPage,text="Submit",width=10, command=self.submitDeleteInfo)
       self.submitDeleteInfoButton.grid(row=6,column=2)

    def submitPaymentInfo(self):
        db=self.connect()
        cursor=db.cursor()
        try:
           a = datetime.datetime.strptime(self.expDate.get(),"%m/%Y")
           try:
               int(self.cardNumber.get())
               int(self.CVV.get())
               if len(self.cardNumber.get()) != 16 or len(self.CVV.get())!=3:
                   raise Exception
               if self.cardNumber.get()==""or self.nameOnCard.get()=="" or self.CVV.get()=="" or self.expDate.get()=="":
                   messagebox.showwarning("Error","Please Fill in all Fields.")
                   return
               else:
                   #### INSERTS NEW CREDIT CARD INFO INTO DATABASE
                   cursor.execute("Insert into PaymentInfo (NameonCard,ExpDate,CVV,CardNumber,Username) Values (%s,%s,%s,%s,%s)",(self.nameOnCard.get(),a,self.CVV.get(),self.cardNumber.get(),self.username))
                   messagebox.showinfo("Success!","Card successfully added!")
                   for label in self.cardPage.winfo_children():
                      label.grid_forget()
                   self.makeCardPage()
           except:
               messagebox.showwarning("Error","Please input correct information.\nCard Number must be 16 digits\nCVV must be 3 digits\nThis card also may already exist for your username")
        except:
           messagebox.showwarning("Error","Incorrect exp date. Please input a exp date in the format MM-YYYY")
           return

    def submitDeleteInfo(self):
       db=self.connect()
       cursor=db.cursor()
       if self.addDelLastFourList[0] == "No Card Found" or self.cardVar2.get() == "No Card Found":
           messagebox.showwarning("Error","No Card Selected to delete")
       else:
           i = self.addDelLastFourList.index(self.cardVar2.get())
           card = self.cardList2[i]
           #### REMOVES CREDIT CARD FROM THE DATABASE
           a = cursor.execute("Delete from PaymentInfo where Username=%s and CardNumber=%s",(self.username,card))
           messagebox.showinfo("Success!","Card successfully deleted!")
           for label in self.cardPage.winfo_children():
                label.grid_forget()
           self.makeCardPage()

    def updateReservation(self):
        self.custPage.withdraw()
        self.updateReservationPage=Toplevel()
        self.updateReservationPage.title("Update Reservation")
        self.pic = Label(self.updateReservationPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=2)
        Label(self.updateReservationPage,text="Reservation ID").grid(row=1,column=0)
        self.updateIDEntry=Entry(self.updateReservationPage,width=10,state="normal")
        self.updateIDEntry.grid(row=1,column=1)
        self.searchUpdateButton=Button(self.updateReservationPage, text="Search",width=10,command=self.updateReservationSearch)
        self.searchUpdateButton.grid(row=1,column=2)
        self.UpdateBackButton=Button(self.updateReservationPage, text="Back",width=10,command=self.updateBack)
        self.UpdateBackButton.grid(row=3,column=1)

    def updateBack(self):
        self.updateReservationPage.withdraw()
        self.custPage.deiconify()

    def updateReservationSearch(self):
        self.updateIDEntry1=int(self.updateIDEntry.get())
        #### RETURNS ALL RESERVATIONS FOR THE PARTICULAR USER
        num=self.c.execute("SELECT * FROM Reservation NATURAL JOIN Customer WHERE ReservationID =%s AND Username =%s AND isCancelled = FALSE",(self.updateIDEntry1,self.username))
        self.updateIDEntry1=int(self.updateIDEntry.get())
        if num !=0:
            self.updateReservationPage.withdraw()
            self.updateSearchPage=Toplevel()
            self.pic = Label(self.updateSearchPage, image = self.photo)
            self.pic.grid(row = 0, column = 0, columnspan=2)
            Label(self.updateSearchPage,text="Train").grid(row=1,column=1)
            Label(self.updateSearchPage,text="Time").grid(row=1,column=2)
            Label(self.updateSearchPage,text="Duration").grid(row=1,column=3)
            Label(self.updateSearchPage,text="Departure Date").grid(row=1,column=4)
            Label(self.updateSearchPage,text="Departs From").grid(row=1,column=5)
            Label(self.updateSearchPage,text="ArrivesAt").grid(row=1,column=6)
            Label(self.updateSearchPage,text="Class").grid(row=1,column=7)
            Label(self.updateSearchPage,text="Price").grid(row=1,column=8)
            Label(self.updateSearchPage,text="# of Baggages").grid(row=1,column=9)
            Label(self.updateSearchPage,text="Passenger Name").grid(row=1,column=10)
            self.c.execute("SELECT TrainNumber,ArrivesAt,DepartsFrom FROM Reserves WHERE ReservationID =%s",(self.updateIDEntry1))
            trains=self.c.fetchall()

            rowcount=2
            intcount=0
            self.radioVar1=IntVar()
            self.radioVar1.set(1000)
            self.help33List=[]
            for item in trains:
                self.c.execute("CREATE or Replace VIEW ArrivalTime AS SELECT TrainNumber, ArrivalTime FROM Stop NATURAL JOIN Station WHERE TrainNumber=%s AND Name=%s",(item[0],item[1]))
                self.c.execute("CREATE OR REPLACE VIEW DepartureTime AS SELECT TrainNumber, DepartureTime FROM Stop NATURAL JOIN Station WHERE TrainNumber = %s AND Name = %s",(item[0],item[2]))
                self.c.execute("CREATE OR REPLACE VIEW Times AS SELECT * FROM ArrivalTime NATURAL JOIN DepartureTime")
                self.c.execute("SELECT TrainNumber,TIMEDIFF(ArrivalTime, DepartureTime) AS Duration, DepartsFrom, ArrivesAt,Class, FirstClassPrice as Price,NumberBags, PassengerName,ArrivalTime,DepartureTime,DepartureDate FROM (Reserves NATURAL JOIN Times) Natural Join TrainRoute WHERE ReservationID =%s AND TrainNumber =%s and Class=1",(self.updateIDEntry1,item[0]))
                firstclass=self.c.fetchall()
                point=self.c.execute("SELECT TrainNumber,TIMEDIFF(ArrivalTime, DepartureTime) AS Duration, DepartsFrom, ArrivesAt,Class, FirstClassPrice as Price,NumberBags, PassengerName,ArrivalTime,DepartureTime,DepartureDate FROM (Reserves NATURAL JOIN Times) Natural Join TrainRoute WHERE ReservationID =%s AND TrainNumber =%s and Class=1",(self.updateIDEntry1,item[0]))
                self.c.execute("SELECT TrainNumber,TIMEDIFF(ArrivalTime, DepartureTime) AS Duration, DepartsFrom, ArrivesAt,Class, SecondClassPrice as Price,NumberBags, PassengerName,ArrivalTime,DepartureTime,DepartureDate FROM (Reserves NATURAL JOIN Times) Natural Join TrainRoute WHERE ReservationID =%s AND TrainNumber =%s and Class=2",(self.updateIDEntry1,item[0]))
                secondclass=self.c.fetchall()
                point2=self.c.execute("SELECT TrainNumber,TIMEDIFF(ArrivalTime, DepartureTime) AS Duration, DepartsFrom, ArrivesAt,Class, SecondClassPrice as Price,NumberBags, PassengerName,ArrivalTime,DepartureTime,DepartureDate FROM (Reserves NATURAL JOIN Times) Natural Join TrainRoute WHERE ReservationID =%s AND TrainNumber =%s",(self.updateIDEntry1,item[0]))
                self.c.execute("SELECT TrainNumber,TIMEDIFF(ArrivalTime, DepartureTime) AS Duration, DepartsFrom, ArrivesAt,Class, SecondClassPrice as Price,NumberBags, PassengerName,ArrivalTime,DepartureTime,DepartureDate FROM (Reserves NATURAL JOIN Times) Natural Join TrainRoute WHERE ReservationID =%s AND TrainNumber =%s",(self.updateIDEntry1,item[0]))
                listcreate=self.c.fetchall()
                self.help2List=[]
                for item in listcreate:
                    self.help2List.append(item)
                self.help33List.append(self.help2List)

                if point!=0:
                    for x in firstclass:
                        Label(self.updateSearchPage,text=x[0]).grid(row=rowcount,column=1)
                        Label(self.updateSearchPage,text=x[9].strftime("%I:%M%p")+"-"+x[8].strftime("%I:%M%p")).grid(row=rowcount,column=2)
                        Label(self.updateSearchPage,text=x[1]).grid(row=rowcount,column=3)
                        Label(self.updateSearchPage,text=x[2]).grid(row=rowcount,column=4)
                        Label(self.updateSearchPage,text=x[10]).grid(row=rowcount,column=5)
                        Label(self.updateSearchPage,text=x[3]).grid(row=rowcount,column=6)
                        Label(self.updateSearchPage,text=x[4]).grid(row=rowcount,column=7)
                        Label(self.updateSearchPage,text=x[5]).grid(row=rowcount,column=8)
                        Label(self.updateSearchPage,text=x[6]).grid(row=rowcount,column=9)
                        Label(self.updateSearchPage,text=x[7]).grid(row=rowcount,column=10)
                        Radiobutton(self.updateSearchPage, variable=self.radioVar1, value=intcount).grid(row=rowcount,column=0)
                        rowcount=rowcount+1
                        intcount=intcount+1
                elif point2!=0:
                    for x in secondclass:
                        Label(self.updateSearchPage,text=x[0]).grid(row=rowcount,column=1)
                        Label(self.updateSearchPage,text=x[9].strftime("%I:%M%p")+"-"+x[8].strftime("%I:%M%p")).grid(row=rowcount,column=2)
                        Label(self.updateSearchPage,text=x[1]).grid(row=rowcount,column=3)
                        Label(self.updateSearchPage,text=x[2]).grid(row=rowcount,column=4)
                        Label(self.updateSearchPage,text=x[10]).grid(row=rowcount,column=5)
                        Label(self.updateSearchPage,text=x[3]).grid(row=rowcount,column=6)
                        Label(self.updateSearchPage,text=x[4]).grid(row=rowcount,column=7)
                        Label(self.updateSearchPage,text=x[5]).grid(row=rowcount,column=8)
                        Label(self.updateSearchPage,text=x[6]).grid(row=rowcount,column=9)
                        Label(self.updateSearchPage,text=x[7]).grid(row=rowcount,column=10)
                        Radiobutton(self.updateSearchPage, variable=self.radioVar1, value=intcount).grid(row=rowcount,column=0)
                        rowcount=rowcount+1
                        intcount=intcount+1
            self.nextUpdateButton=Button(self.updateSearchPage,text="Next",command=self.nextUpdate,width=10)
            self.nextUpdateButton.grid(row=rowcount,column=0)
            self.backUpdate2CusButton=Button(self.updateSearchPage,text="Back",command=self.backUpdate2Cus,width=10)
            self.backUpdate2CusButton.grid(row=rowcount,column=1)
        else:
            messagebox.showwarning("Error", "ID Not in System")

    def nextUpdate(self):
        if self.radioVar1.get()==1000:
            messagebox.showwarning("Error","No Ticket Selected")
        else:
            self.updateSearchPage.withdraw()
            self.nextUpdatePage=Toplevel()

            self.helpList=self.help33List
            self.radioVar12=self.radioVar1.get()

            Label(self.nextUpdatePage,text="Train").grid(row=1,column=1)
            Label(self.nextUpdatePage,text="Duration").grid(row=1,column=2)
            Label(self.nextUpdatePage,text="Time").grid(row=1,column=3)
            Label(self.nextUpdatePage,text="Departure Date").grid(row=1,column=4)
            Label(self.nextUpdatePage,text="Departs From").grid(row=1,column=5)
            Label(self.nextUpdatePage,text="ArrivesAt").grid(row=1,column=6)
            Label(self.nextUpdatePage,text="Class").grid(row=1,column=7)
            Label(self.nextUpdatePage,text="Price").grid(row=1,column=8)
            Label(self.nextUpdatePage,text="# of Baggages").grid(row=1,column=9)
            Label(self.nextUpdatePage,text="Passenger Name").grid(row=1,column=10)
            Label(self.nextUpdatePage,text=self.helpList[self.radioVar12][0][0]).grid(row=2,column=1)
            Label(self.nextUpdatePage,text=self.helpList[self.radioVar12][0][1]).grid(row=2,column=2)
            Label(self.nextUpdatePage,text=self.helpList[self.radioVar12][0][9].strftime("%I:%M%p")+"-"+self.helpList[self.radioVar12][0][8].strftime("%I:%M%p")).grid(row=2,column=3)
            Label(self.nextUpdatePage,text=self.helpList[self.radioVar12][0][10]).grid(row=2,column=4)
            Label(self.nextUpdatePage,text=self.helpList[self.radioVar12][0][2]).grid(row=2,column=5)
            Label(self.nextUpdatePage,text=self.helpList[self.radioVar12][0][3]).grid(row=2,column=6)
            Label(self.nextUpdatePage,text=self.helpList[self.radioVar12][0][4]).grid(row=2,column=7)
            Label(self.nextUpdatePage,text=self.helpList[self.radioVar12][0][5]).grid(row=2,column=8)
            Label(self.nextUpdatePage,text=self.helpList[self.radioVar12][0][6]).grid(row=2,column=9)
            Label(self.nextUpdatePage,text=self.helpList[self.radioVar12][0][7]).grid(row=2,column=10)
            Label(self.nextUpdatePage,text="New Departure Date").grid(row=3,column=0)
            self.updateDepartureEntry=Entry(self.nextUpdatePage, state="normal",width=10)
            self.updateDepartureEntry.grid(row=3,column=1)
            self.searchAvailabilityButton=Button(self.nextUpdatePage, text="Search",width=10,command=self.searchAvailability)
            self.searchAvailabilityButton.grid(row=3,column=2)
            self.backNotTrue=Button(self.nextUpdatePage, text="Back",width=10,command=self.backTooLate)
            self.backNotTrue.grid(row=3,column=3)

    def backTooLate(self):
        self.nextUpdatePage.withdraw()
        self.custPage.deiconify()

    def searchAvailability(self):
                    try:
                        self.updateDepartureEntry45 = datetime.datetime.strptime(self.updateDepartureEntry.get(),"%m/%d/%Y")
                    except:
                        messagebox.showwarning("Error","Incorrect departure date. Please input a departure date in the format MM/DD/YYYY")
                        return
                    #### CHECKS FOR AVAILABILITY BASED ON THE GIVEN CRITERIA
                    cursor34=self.c.execute("SELECT * FROM Reserves WHERE ReservationID =%s AND DATEDIFF(DepartureDate,CURDATE()) <=1",(self.updateIDEntry1))


                    if cursor34!=0:
                        messagebox.showwarning("Error","Too Late to Change")
                        return
                    else:
                        x2=datetime.datetime.strptime(self.updateDepartureEntry.get(),"%m/%d/%Y")
                        self.c.execute("Update Reserves Set DepartureDate=%s WHERE ReservationID=%s and TrainNumber=%s",(x2,self.updateIDEntry1,self.helpList[self.radioVar12][0][0]))
                        self.nextUpdate2()

    def nextUpdate2(self):
            self.nextUpdatePage.withdraw()
            self.nextUpdatePage2=Toplevel()
            self.radioVar12=self.radioVar1.get()
            Label(self.nextUpdatePage2,text="Train").grid(row=1,column=1)
            Label(self.nextUpdatePage2,text="Duration").grid(row=1,column=2)
            Label(self.nextUpdatePage2,text="Time").grid(row=1,column=3)
            Label(self.nextUpdatePage2,text="Departure Date").grid(row=1,column=4)
            Label(self.nextUpdatePage2,text="Departs From").grid(row=1,column=5)
            Label(self.nextUpdatePage2,text="ArrivesAt").grid(row=1,column=6)
            Label(self.nextUpdatePage2,text="Class").grid(row=1,column=7)
            Label(self.nextUpdatePage2,text="Price").grid(row=1,column=8)
            Label(self.nextUpdatePage2,text="# of Baggages").grid(row=1,column=9)
            Label(self.nextUpdatePage2,text="Passenger Name").grid(row=1,column=10)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][0]).grid(row=2,column=1)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][1]).grid(row=2,column=2)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][9].strftime("%I:%M%p")+"-"+self.helpList[self.radioVar12][0][8].strftime("%I:%M%p")).grid(row=2,column=3)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][10]).grid(row=2,column=4)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][2]).grid(row=2,column=5)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][3]).grid(row=2,column=6)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][4]).grid(row=2,column=7)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][5]).grid(row=2,column=8)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][6]).grid(row=2,column=9)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][7]).grid(row=2,column=10)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][0]).grid(row=4,column=1)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][1]).grid(row=4,column=2)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][9].strftime("%I:%M%p")+"-"+self.helpList[self.radioVar12][0][8].strftime("%I:%M%p")).grid(row=4,column=3)
            Label(self.nextUpdatePage2,text=self.updateDepartureEntry.get()).grid(row=4,column=4)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][2]).grid(row=4,column=5)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][3]).grid(row=4,column=6)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][4]).grid(row=4,column=7)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][5]).grid(row=4,column=8)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][6]).grid(row=4,column=9)
            Label(self.nextUpdatePage2,text=self.helpList[self.radioVar12][0][7]).grid(row=4,column=10)
            Label(self.nextUpdatePage2,text="NEW TICKET:").grid(row=3,column=1)
            self.back2Next=Button(self.nextUpdatePage2,width=10,command=self.back2next,text="Back")
            self.back2Next.grid(row=7,column=1)
            self.submitChangeButton=Button(self.nextUpdatePage2,width=10,text="Submit",command=self.submitChange)
            self.submitChangeButton.grid(row=7,column=2)
            self.c.execute("Select totalCost from Reservation where ReservationID=%s",self.updateIDEntry1)
            price=self.c.fetchall()
            self.price=float(price[0][0]+50)
            Label(self.nextUpdatePage2,text="Change Fee").grid(row=5,column=1)
            Label(self.nextUpdatePage2,text="$50").grid(row=5,column=2)
            Label(self.nextUpdatePage2,text="Updated Total Cost").grid(row=6,column=1)
            Label(self.nextUpdatePage2,text=self.price).grid(row=6,column=2)

    def submitChange(self):
        self.c.execute("Update Reservation SET totalCost=%s where ReservationID=%s",(self.price,self.updateIDEntry1))
        self.nextUpdatePage2.withdraw()
        self.custPage.deiconify()

    def back2next(self):
        self.nextUpdatePage2.withdraw()
        self.updateReservationPage.deiconify()

    def makegiveReviewPage(self):
        self.custPage.withdraw()
        self.giveReviewPage=Toplevel()
        self.giveReviewPage.title("Give Review")
        self.pic = Label(self.giveReviewPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=2)
        Label(self.giveReviewPage,text="Train Number").grid(row=1,column=0)
        Label(self.giveReviewPage,text="Rating").grid(row=2,column=0)
        Label(self.giveReviewPage,text="Comment").grid(row=3,column=0)
        self.trainNumberReview=Entry(self.giveReviewPage,width=30,state="normal")
        self.trainNumberReview.grid(row=1,column=1)
        self.commentReview=Entry(self.giveReviewPage,width=30,state="normal")
        self.commentReview.grid(row=3,column=1)
        list1=["Good","Neutral", "Bad"]
        self.reviewVar = StringVar()
        self.dropReview = OptionMenu(self.giveReviewPage,self.reviewVar,*list1)
        self.dropReview.config(width=20)
        self.dropReview.grid(row=2,column=1)
        self.submitReviewButton=Button(self.giveReviewPage, text="Submit",width=10,command=self.submitReview)
        self.submitReviewButton.grid(row=4,column=0)
        self.giveReviewBackButton=Button(self.giveReviewPage, text="Back",width=10,command=self.giveReviewBack)
        self.giveReviewBackButton.grid(row=4,column=1)

    def giveReviewBack(self):
        self.giveReviewPage.withdraw()
        self.custPage.deiconify()

    def makeViewReviews(self):
       self.custPage.withdraw()
       self.viewReviews=Toplevel()
       self.viewReviews.title("View Review")
       self.pic = Label(self.viewReviews, image = self.photo)
       self.pic.grid(row = 0, column = 0, columnspan=2)
       Label(self.viewReviews, text="Train Number").grid(row=1,column=0)
       self.trainReview=Entry(self.viewReviews,width=30,state="normal")
       self.trainReview.grid(row=1,column=1)
       self.viewReviewBackButton=Button(self.viewReviews,text="Back",width=10, command=self.viewReviewBack)
       self.viewReviewBackButton.grid(row=2,column=0)
       self.viewReviewNextButton=Button(self.viewReviews,text="Next",width=10, command=self.makeviewReviewNextPage)
       self.viewReviewNextButton.grid(row=2,column=1)

    def viewReviewBack(self):
        self.viewReviews.withdraw()
        self.custPage.deiconify()

    def makeviewReviewNextPage(self):
       db=self.connect()
       cursor=db.cursor()
       #### FINDS REVIEWS FOR THE TRAIN NUMBER SPECIFIED
       cursor1=cursor.execute("Select * from Review where TrainNumber=%s",(self.trainReview.get()))
       if cursor1 !=0:
           self.viewReviews.withdraw()
           self.viewReviewNext=Toplevel()
           self.viewReviews.title("View Review")
           self.pic = Label(self.viewReviewNext, image = self.photo)
           self.pic.grid(row = 0, column = 0, columnspan=2)
           Label(self.viewReviewNext, text="Rating").grid(row=1,column=0)
           Label(self.viewReviewNext, text="Comment").grid(row=1,column=1)
           cursor.execute("Select Rating,Comment,TrainNumber FROM Review where TrainNumber=%s",(self.trainReview.get()))
           a=cursor.fetchall()
           rowcount=2
           for x in a:
               Label(self.viewReviewNext,text=x[0]).grid(row=rowcount,column=0)
               Label(self.viewReviewNext,text=x[1]).grid(row=rowcount,column=1)
               rowcount=rowcount+1
           self.viewReviewBack2Button=Button(self.viewReviewNext,text="Back to Choose Functionality",width=20, command=self.viewReviewBack2)
           self.viewReviewBack2Button.grid(row=rowcount+1,column=0,columnspan=2)
       else:
            messagebox.showwarning("Error","No Train Reviews Found")

    def viewReviewBack2(self):
        self.viewReviewNext.withdraw()
        self.custPage.deiconify()

    def submitReview(self):
        db=self.connect()
        cursor=db.cursor()
        cursor2=db.cursor()
        cursor3=db.cursor()
        cursor.execute("Select max(ReviewNum) from Review")
        a=cursor.fetchall()
        for x in a:
            if x[0]==0 or x[0]==None:
                self.reviewNum=1
            else:
                self.reviewNum=x[0]+1
        cursor5=cursor2.execute("Select * From TrainRoute where TrainNumber=%s",(self.trainNumberReview.get()))
        if cursor5==0:
                messagebox.showwarning("Error","Invalid Train")
        elif self.reviewVar.get()=="":
                messagebox.showwarning("Error","No Rating")
        else:
            cursor3.execute("Insert into Review(TrainNumber,Username,Rating,ReviewNum,Comment) Values (%s,%s,%s,%s,%s)",(self.trainNumberReview.get(),self.username,self.reviewVar.get(),self.reviewNum,self.commentReview.get()))
            messagebox.showinfo("Success","Thank you for your feedback!")

    def backToReservationPage(self):
        self.findTrainsPage.destroy()
        self.reservationPage.deiconify()

    def backToFindTrains(self):
        self.travelExtrasPage.destroy()
        self.findTrainsPage.deiconify()


    def backUpdate2Cus(self):
        self.updateSearchPage.withdraw()
        self.custPage.deiconify()

    def cancelReservation(self):
        cursor=self.connect().cursor()
        #### RETURNS RESERVATIONS FOR THE CURRENT USER
        cursor.execute("SELECT Reserves.DepartureDate, Reserves.DepartsFrom, Reserves.ArrivesAt, Reserves.Class, Reservation.ReservationID, Reservation.totalCost FROM Reservation INNER JOIN Reserves ON Reservation.ReservationID=Reserves.ReservationID WHERE Reservation.Username='"+self.username+"' AND Reservation.IsCancelled=FALSE AND DATEDIFF(Now(), Reserves.DepartureDate) < -1")
        registrations = cursor.fetchall()
        if len(registrations) == 0:
            messagebox.showwarning("No reservations", "You have no reservations to cancel.")
            return
        self.custPage.withdraw()
        self.cancelPage = Toplevel()
        self.pic = Label(self.cancelPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=7)
        Label(self.cancelPage, text="Date").grid(row=1, column=0, sticky=W)
        Label(self.cancelPage, text="Departure Station").grid(row=1, column=1)
        Label(self.cancelPage, text="Arrival Station").grid(row=1, column=2)
        Label(self.cancelPage, text="Class").grid(row=1, column=3)
        Label(self.cancelPage, text="ID").grid(row=1, column=4)
        Label(self.cancelPage, text="Cost").grid(row=1, column=5)
        Label(self.cancelPage, text="Cancel?").grid(row=1, column=6)
        cancelList = []
        for i in range(len(registrations)):
            var = IntVar()
            cancelList.append(var)
        for i in range(len(registrations)):
            for j in range(7):
                if j == 5:
                    Label(self.cancelPage, text="$"+str("%.2f" % round(float(registrations[i][j]), 2))).grid(row=i+2, column=j, sticky=W)
                elif j < 5:
                    Label(self.cancelPage, text=registrations[i][j]).grid(row=i+2, column=j, sticky=W)
                else:
                    Checkbutton(self.cancelPage, variable=cancelList[i]).grid(row=i+2, column=j)
        confirmButton = Button(self.cancelPage, text="Confirm", command=lambda: self.cancelConfirmation(cancelList, registrations))
        confirmButton.grid(row=len(registrations)+3, column=1)
        backButton = Button(self.cancelPage, text="Back", command=self.closeCancel)
        backButton.grid(row=len(registrations)+3, column=0)

    def cancelConfirmation(self, cancelList, registrations):
        cancellation = False
        for x in cancelList:
           if x.get() == 1:
               cancellation = True
               break
        if not cancellation:
            messagebox.showwarning("No reservations selected", "Please select a reservation to cancel.")
            return
        cursor=self.connect().cursor()
        self.cancelPage.withdraw()
        self.confirmationPage = Toplevel()
        self.pic = Label(self.confirmationPage, image = self.photo)
        self.pic.grid(row = 0, column = 0, columnspan=6)
        newCancelList = []
        for i in range(len(cancelList)):
            if cancelList[i].get() == 1:
                regID = registrations[i][4]
                cursor.execute("SELECT CASE WHEN DATEDIFF(Now(), Reserves.DepartureDate) < -7 THEN (SELECT CASE WHEN (Reservation.totalCost * 0.8) - 50.0 > 0 THEN( Reservation.totalCost * 0.8) - 50.0  ELSE 0 END) ELSE (SELECT CASE WHEN Reservation.totalCost * 0.5 - 50 > 0 THEN Reservation.totalCost * 0.5 - 50 ELSE 0 END) END AS `Refund`, Reservation.ReservationID, Reservation.totalCost FROM Reservation INNER JOIN Reserves ON Reservation.ReservationID=Reserves.ReservationID WHERE Reservation.ReservationID="+str(regID))
        for x in cursor:
            newCancelList.append(x)
        Label(self.confirmationPage, text="Are you sure you want to cancel?").grid(row=1, column=0, columnspan=2)
        Label(self.confirmationPage, text="ID").grid(row=2, column=0)
        Label(self.confirmationPage, text="Refund").grid(row=2, column=1)
        for i in range(len(newCancelList)):
            Label(self.confirmationPage, text=newCancelList[i][1]).grid(row=i+3, column=0)
            Label(self.confirmationPage, text="$"+str("%.2f" % round(float(newCancelList[i][0])))).grid(row=i+3, column=1)
        Button(self.confirmationPage, text="No", command=self.backToCancel).grid(row=len(newCancelList)+3, column=0)
        Button(self.confirmationPage, text="Yes", command=lambda: self.cancelConfirm(newCancelList, registrations)).grid(row=len(newCancelList)+3, column=1)

    def backToCancel(self):
        self.confirmationPage.withdraw()
        self.cancelPage.deiconify()

    def cancelConfirm(self, cancelList, registrations):
        cursor=self.connect().cursor()
        for i in range(len(cancelList)):
            cursor.execute("UPDATE Reservation SET IsCancelled=TRUE WHERE ReservationID='"+str(cancelList[i][1])+"'")
            cursor.execute("UPDATE Reservation SET totalCost="+str(float(cancelList[i][2])-float(cancelList[i][0]))+" WHERE ReservationID='"+str(cancelList[i][1])+"'")
        self.connect().commit()
        if len(cancelList) == len(registrations):
            self.confirmationPage.withdraw()
            self.custPage.deiconify()
        else:
            self.confirmationPage.withdraw()
            self.cancelReservation()

    def closeCancel(self):
        self.cancelPage.withdraw()
        self.custPage.deiconify()

    def giveReview(self):
        print("Reviews")

    def logout(self):
        self.custPage.withdraw()
        self.rootWin.deiconify()

    def back(self):
        self.schoolPage.withdraw()
        self.custPage.deiconify()


GUI()

