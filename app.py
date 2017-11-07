import Tkinter
import zeep
import csv
import os
import shutil
import requests
import smtplib
import datetime
import re
from email.mime.text import MIMEText

class articleInfoGUI(Tkinter.Tk):
    """This class will hold information about the article under consideration."""

    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        stepOne = Tkinter.LabelFrame(self, text="Article Info")
        stepOne.grid(row=0, columnspan=7, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
        self.Val1Lbl = Tkinter.Label(stepOne,text="Article Title:")
        self.Val1Lbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        self.Val1Txt = Tkinter.Entry(stepOne)
        self.Val1Txt.grid(row=0, column=1, columnspan=3, pady=2, sticky='WE')

        self.Val2Lbl = Tkinter.Label(stepOne,text="Author:")
        self.Val2Lbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        self.Val2Txt = Tkinter.Entry(stepOne)
        self.Val2Txt.grid(row=1, column=1, columnspan=3, pady=2, sticky='WE')

        self.Val3Lbl = Tkinter.Label(stepOne,text="Affliation:")
        self.Val3Lbl.grid(row=2, column=0, sticky='E', padx=5, pady=2)
        self.Val3Txt = Tkinter.Entry(stepOne)
        self.Val3Txt.grid(row=2, column=1, columnspan=3, pady=2, sticky='WE')

        self.Val4Lbl = Tkinter.Label(stepOne,text="Abstract:")
        self.Val4Lbl.grid(row=3, column=0, sticky='E', padx=5, pady=2)
        self.Val4Txt = Tkinter.Entry(stepOne)
        self.Val4Txt.grid(row=3, column=1, columnspan=3, pady=2, sticky='WE')

        self.Val5Lbl = Tkinter.Label(stepOne,text="Article url:")
        self.Val5Lbl.grid(row=4, column=0, sticky='E', padx=5, pady=2)
        self.Val5Txt = Tkinter.Entry(stepOne)
        self.Val5Txt.grid(row=4, column=1, columnspan=3, pady=2, sticky='WE')

        self.Val6Lbl = Tkinter.Label(stepOne,text="Review Manager:")
        self.Val6Lbl.grid(row=5, column=0, sticky='E', padx=5, pady=2)
        self.Val6Txt = Tkinter.Entry(stepOne)
        self.Val6Txt.grid(row=5, column=1, columnspan=3, pady=2, sticky='WE')

        self.val1 = None
        self.val2 = None
        self.val3 = None
        self.val4 = None
        self.val5 = None
        self.val6 = None

        SubmitBtn = Tkinter.Button(stepOne, text="Submit",command=self.submit1)
        SubmitBtn.grid(row=6, column=3, sticky='W', padx=5, pady=2)
    def submit1(self):

        self.articleTitle=self.Val1Txt.get()
        if self.articleTitle=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.articleAuthor=self.Val2Txt.get()
        if self.articleAuthor=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.authorAffliation=self.Val3Txt.get()
        if self.authorAffliation=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.articleAbstract=self.Val4Txt.get()
        if self.articleAbstract=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.articleUrl=self.Val5Txt.get()
        if self.articleUrl=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.reviewManager=self.Val6Txt.get()
        if self.reviewManager=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()
        self.quit()

def convertThisShit(shit):
    if type(shit) != str:
        shit=shit.encode('utf-8')
    return shit

def constructEmail(d, AuthorLastName):
    AuthorLastName=AuthorLastName
    newpath = os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName))
    for i in d.keys():
        d[i]["emailText"] = d[i]["emailText"].replace("REVIEWERLASTNAME", d[i]["lastName"])
        d[i]["emailText"] = d[i]["emailText"].replace("SENDERNAME", d[i]["reviewManager"])
        d[i]["emailText"] = d[i]["emailText"].replace("ARTICLETITLE", d[i]["article"])
        d[i]["emailText"] = d[i]["emailText"].replace("AUTHORNAME", d[i]["author"])
        d[i]["emailText"] = d[i]["emailText"].replace("AUTHORAFFILIATION", d[i]["authorAffliation"])
        d[i]["emailText"] = d[i]["emailText"].replace("THEABSTRACT", d[i]["abstract"])
        d[i]["emailText"] = d[i]["emailText"].replace("ARTICLEHOMEPAGE", d[i]["homepage"])

        emailTextFile = d[i]["emailTextFile"]
        thisEmail = open(emailTextFile, "w")
        thisEmail.write(d[i]["emailText"])
        thisEmail.close()

class authorInfoGUI(Tkinter.Tk):
    """Article_info holds information about the author last name. if we already started searching
    for reviews, then this will skip the metadata entry box and go to the search."""
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
    def initialize(self):
        self.grid()
        stepOne = Tkinter.LabelFrame(self, text="Enter article author last name")
        stepOne.grid(row=0, columnspan=7, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
        self.Val1Lbl = Tkinter.Label(stepOne,text="Author Last Name:")
        self.Val1Lbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        self.Val1Txt = Tkinter.Entry(stepOne)
        self.Val1Txt.grid(row=0, column=1, columnspan=3, pady=2, sticky='WE')
        self.val1 = None
        SubmitBtn = Tkinter.Button(stepOne, text="Submit",command=self.submit2)
        SubmitBtn.grid(row=1, column=3, sticky='W', padx=5, pady=2)
    def submit2(self):
        self.AuthorLastName=self.Val1Txt.get()
        if self.AuthorLastName=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()
        self.quit()

class searchTextGUI(Tkinter.Tk):
    """searchTextGUI grabs the text to search for."""
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
    def initialize(self):
        self.grid()
        stepOne = Tkinter.LabelFrame(self, text="Enter some text to search for peer reviewers.")
        stepOne.grid(row=0, columnspan=7, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
        self.Val1Lbl = Tkinter.Label(stepOne,text="Search Text:")
        self.Val1Lbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        self.Val1Txt = Tkinter.Entry(stepOne)
        self.Val1Txt.grid(row=0, column=1, columnspan=3, pady=2, sticky='WE')
        self.val1 = None
        SubmitBtn = Tkinter.Button(stepOne, text="Submit",command=self.submit3)
        SubmitBtn.grid(row=1, column=3, sticky='W', padx=5, pady=2)
    def submit3(self):
        self.searchText=self.Val1Txt.get()
        if self.searchText=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()
        self.quit()

def getTheAuthorLastName():
    article_meta_data = authorInfoGUI(None)
    article_meta_data.title('Open Peer Review App')
    article_meta_data.mainloop() #this will run until it closes
    return article_meta_data.AuthorLastName

def getTheSearchText():
    searchText = searchTextGUI(None)
    searchText.title('Open Peer Review App')
    searchText.mainloop() #this will run until it closes
    return searchText.searchText

def getTheMetaData():
    article_meta_data = articleInfoGUI(None)
    article_meta_data.title('Open Peer Review App')
    article_meta_data.mainloop() #this will run until it closes
    return article_meta_data.articleTitle, article_meta_data.articleAuthor, article_meta_data.authorAffliation, article_meta_data.articleAbstract, article_meta_data.articleUrl, article_meta_data.reviewManager

AuthorLastName = getTheAuthorLastName()

def writeHeader(AuthorLastName):
    AuthorLastName = AuthorLastName
    now = datetime.datetime.now()
    now = "-"+str(now).replace(".", "-").replace(":", "-").replace(" ", "-")
    if os.path.isdir(os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName))) == False:
        os.mkdir(os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName)))
    if os.path.isfile(os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName+"/reviewerList.csv"))) == False:
        newpath = os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName))
        header = [["lastName", "lastandFirstInit", "email", "yearEmail", "paperTitle", "paperYear","reviewManager","article","author","authorAffliation","abstract","homepage","emailText", "dateTime"]]
        resultFile = open(os.path.join(newpath + "/reviewerList.csv"), "a")
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerows(header)
        resultFile.close()
    else:
        newpath = os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName))
    return AuthorLastName, newpath

AuthorLastName,newpath=writeHeader(AuthorLastName)

def insertArticleInfoIntoEmail(AuthorLastName,newpath):
    AuthorLastName=AuthorLastName
    newpath = newpath
    shutil.copyfile(os.path.normpath(os.path.join(os.getcwd()+"/"+'email.txt')), os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName+"/"+'email.txt')))
    with open(os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName+"/"+'email.txt')), 'r') as myfile:
        emailText=myfile.read()
    if os.path.isfile(os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName+"/"+"details.txt"))):
        details = os.path.normpath(os.getcwd()+"/"+AuthorLastName+"/"+"details.txt")
        d={}
        with open(details, "r") as f:
            for line in f:
                d[line.split()[0]]=" ".join(line.split()[1:])
        return d["reviewManager"],d["article"],d["author"],d["authorAffliation"],d["abstract"],d["homepage"],emailText
    else:
        articleTitle, articleAuthor, authorAffliation, articleAbstract, articleUrl, reviewManager = getTheMetaData()
        detailsTextFile = open(os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName+"/"+'details.txt')), 'w')
        detailsTextFile.write("leaveThisBlank" + "\n")
        detailsTextFile.write("reviewManager " + reviewManager+ "\n")
        detailsTextFile.write("article " + articleTitle + "\n")
        detailsTextFile.write("author " + articleAuthor+ "\n")
        detailsTextFile.write("authorAffliation " + authorAffliation+ "\n")
        detailsTextFile.write("abstract " + articleAbstract + "\n")
        detailsTextFile.write("homepage " + articleUrl + "\n")
        return reviewManager, articleTitle,articleAuthor,authorAffliation,articleAbstract,articleUrl,emailText

reviewManager,article,author,authorAffliation,abstract,homepage,emailText=insertArticleInfoIntoEmail(AuthorLastName,newpath)
def writeIt(x,AuthorLastName):
    x = x
    AuthorLastName = AuthorLastName
    newpath = os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName))
    resultFile = os.path.normpath(newpath + "/reviewerList.csv")
    wr = csv.writer(open(resultFile,'ab'), dialect='excel')
    wr.writerows(x)

def writeResults(d, AuthorLastName):
    d = d
    AuthorLastName=AuthorLastName
    now = datetime.datetime.now()
    for key in d.keys():
        x = [[d[key]["lastName"], d[key]["lastNameFirstInit"], d[key]["email"], d[key]["yearEmail"],
              d[key]["paperTitle"], d[key]["paperYear"], d[key]["reviewManager"], d[key]["article"],
             d[key]["author"], d[key]["authorAffliation"], d[key]["abstract"],d[key]["homepage"],
             d[key]["emailText"], str(now)]]
        for thisRow in range(len(x[0])):
            if type(x[0][thisRow]) != str:
                try:
                    x[0][thisRow] = x[0][thisRow].encode('utf-8')
                except:
                    print "You should probably read more about unicode characters."
        writeIt(x,AuthorLastName)

wsdl = 'http://jane.biosemantics.org:8080/JaneServer/services/JaneSOAPServer?wsdl'
client = zeep.Client(wsdl=wsdl)

class considerExcluding(Tkinter.Tk):
    """ No Doc String yet. """
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
    def initialize(self):

        frame = Tkinter.Frame(self)
        frame.pack()
        label = Tkinter.Label(self, text="Do you want to check the list, e.g. duplicates are automatically excluded, but you can manually exclude reviewers as well.")
        label.pack()

        closeButton = Tkinter.Button(self, text="No", command=self.no)
        closeButton.pack(side = "right")

        okButton = Tkinter.Button(self, text="Yes", command=self.yes)
        okButton.pack(side = "left")

    def yes(self):
        self.exclude="y"
        if self.exclude=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()
        self.quit()

    def no(self):
        self.exclude="n"
        if self.exclude=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()
        self.quit()

def perhapsExclude():
    a = considerExcluding(None)
    a.title('Open Peer Review App')
    a.mainloop() #this will run until it closes
    return a.exclude

class excludeTheseGUI(Tkinter.Tk):

    def __init__(self, parent, buttonDic):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.buttonDic = buttonDic
        self.initialize()

    def initialize(self):
        self.grid()
        for key in self.buttonDic:
            thisText = self.buttonDic[key]
            self.buttonDic[key] = Tkinter.IntVar()
            aCheckButton = Tkinter.Checkbutton(self, text= thisText, variable=self.buttonDic[key])
            aCheckButton.grid(padx=5, pady=2)

        submitButton = Tkinter.Button(self, text="Submit", command=self.query_checkbuttons)
        submitButton.grid()

    def query_checkbuttons(self):
        self.excluded = []
        for key, value in self.buttonDic.items():
            state = value.get()
            if state != 0:
                self.excluded.append(key)
                self.buttonDic[key].set(0)
                Win2=Tkinter.Tk()
                Win2.withdraw()
        self.quit()

def getTheExcluded(buttonDic=dict):
    buttonDic=buttonDic
    gui = excludeTheseGUI(None,buttonDic)
    gui.mainloop()
    return gui.excluded

def getResults(newpath, AuthorLastName, reviewManager="",article="",author="",authorAffliation="",abstract="",homepage="",emailText="", buildDict=True):
    n = 0
    newpath=newpath
    AuthorLastName= AuthorLastName
    reviewManager=reviewManager
    article=article
    author=author
    authorAffliation=authorAffliation
    abstract=abstract
    homepage=homepage
    emailText=emailText
    searchText = getTheSearchText()
    #searchText = searchText.decode("utf-8")
    buildDict = buildDict
    d={}
    if buildDict == True:
        mylist = client.service.getAuthors(searchText)
        the_current_results = {}
        for i in range(len(mylist)):
            if mylist[i]["name"]:
                if len(client.service.getEMail(mylist[i]["name"], mylist[i]["papers"][0]["pmid"])) > 1:
                    lastName = mylist[i]["name"].split()[0]
                    lastName=convertThisShit(lastName)
                    lastandFirstInit = mylist[i]["name"]
                    lastandFirstInit=convertThisShit(lastandFirstInit)
                    email = client.service.getEMail(mylist[i]["name"], mylist[i]["papers"][0]["pmid"])[0]["eMail"]
                    yearEmail = client.service.getEMail(mylist[i]["name"], mylist[i]["papers"][0]["pmid"])[0]["year"]
                    paperTitle = mylist[i]["papers"][0]["title"]
                    paperTitle= convertThisShit(paperTitle)
                    paperYear =  mylist[i]["papers"][0]["year"]
                    now = datetime.datetime.now()
                    now = "-"+str(now).replace(".", "-").replace(":", "-").replace(" ", "-")
                    forthisFile=re.sub('[^a-zA-Z0-9-_*.]', '', lastName)
                    emailTextFile = os.path.normpath(os.path.join(newpath + "/"+forthisFile+now+".txt"))
                    the_current_results[n] = [lastandFirstInit, email, yearEmail, paperTitle, paperYear]
                    d[n] = {"lastName":lastName, "lastNameFirstInit": lastandFirstInit, "email": email, "yearEmail": yearEmail, "paperTitle": paperTitle,
                            "paperYear": paperYear, "reviewManager":reviewManager,"article":article,"author":author,"authorAffliation":authorAffliation,
                            "abstract":abstract,"homepage":homepage,"emailText":emailText, "emailTextFile":emailTextFile}
                    #print "-------------------------------------------------------"
                    n = n + 1
        del(mylist)
        exlcusion = perhapsExclude()
        if exlcusion == "y":
            newD = {}
            theseRanges=[]
            excludeTheseStr = getTheExcluded(buttonDic=the_current_results)
            excludeThese = [int(i) for i in excludeTheseStr]
            theseRanges.append(excludeThese)
            #print "these are excluded:", [i for sublist in theseRanges for i in sublist]
            thisKey=0
            for included in d.keys():
                 if included not in theseRanges:
                    newD[thisKey]=d[included]
                    thisKey=thisKey+1
            #print "the d is this long:", len(newD)
            return newD
        else:
            return d

n = ""
emailDict={}
allOldEmails=[]
with open(os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName+"/"+"reviewerList.csv")), "r") as f:
    reader=csv.reader(f)
    for row in reader:
        allOldEmails.append(row[2])

class addMoreGUI(Tkinter.Tk):
    """No Doc String Yet."""
    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
    def initialize(self):

        frame = Tkinter.Frame(self)
        frame.pack()
        label = Tkinter.Label(self, text="Do you want to add more reviewers?")
        label.pack()

        closeButton = Tkinter.Button(self, text="No", command=self.no)
        closeButton.pack(side = "right")

        okButton = Tkinter.Button(self, text="Yes", command=self.yes)
        okButton.pack(side = "left")

    def yes(self):
        self.exclude=""
        if self.exclude=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()
        self.quit()

    def no(self):
        self.exclude="n"
        if self.exclude=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()
        self.quit()

def goAgain():
    a = addMoreGUI(None)
    a.title('Open Peer Review App')
    a.mainloop() #this will run until it closes
    return a.exclude

class sendEmailsGUI(Tkinter.Tk):

    """No doc string yet."""

    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
    def initialize(self):

        frame = Tkinter.Frame(self)
        frame.pack()
        label = Tkinter.Label(self, text="Do you want to send the emails to the reviewers?")
        label.pack()

        closeButton = Tkinter.Button(self, text="No", command=self.no)
        closeButton.pack(side = "right")

        okButton = Tkinter.Button(self, text="Yes", command=self.yes)
        okButton.pack(side = "left")

    def yes(self):
        self.exclude="y"
        if self.exclude=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()
        self.quit()

    def no(self):
        self.exclude="s"
        if self.exclude=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()
        self.quit()

def sendTheEmailButton():
    a = sendEmailsGUI(None)
    a.title('Open Peer Review App')
    a.mainloop() #this will run until it closes
    return [a.exclude]

def sendEmail(AuthorLastName="",  SERVER="", FROM="", TO=[""], SUBJECT="", TEXT="", PASSWORD="", LOADFILE=""):
    AuthorLastName=AuthorLastName
    newpath = os.path.normpath(os.path.join(os.getcwd()+"/"+AuthorLastName))
    TO=TO
    SERVER=SERVER
    FROM=FROM
    SUBJECT=SUBJECT
    TEXT=TEXT
    PASSWORD=PASSWORD
    LOADFILE=LOADFILE
    if SERVER == "":
        SERVER = "smtp.office365.com"
    if FROM == "":
        FROM = raw_input("Enter the sender email address: ")
    if TO == [""]:
        TO =  [raw_input("Enter the recipient email address: ")]
    if SUBJECT=="":
        SUBJECT = raw_input("Enter the email subject: ")
    if TEXT == "":
        TEXT = raw_input("Enter the text for the body or type 'load file' to load from file: ")
    if TEXT == "load file":
        with open(LOADFILE, 'r') as myfile:
            TEXT=myfile.read()
    msg=MIMEText(TEXT)
    msg["Subject"]=SUBJECT
    msg["To"] = ", ".join(TO)
    msg['Content-Type'] = "text/html; charset=utf-8"

    print SERVER
    # Send the mail
    if PASSWORD =="":
        PASSWORD = raw_input("Trust me? Enter your password: ")
    server = smtplib.SMTP(SERVER, 587)
    server.starttls()
    server.ehlo()
    server.login(FROM, PASSWORD)
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()

class sendEmailGUI(Tkinter.Tk):
    """No Doc String Yet."""

    def __init__(self, parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        stepOne = Tkinter.LabelFrame(self, text="Email the reviewers")
        stepOne.grid(row=0, columnspan=7, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
        self.Val1Lbl = Tkinter.Label(stepOne,text="Email Server, e.g. smtp.gmail.com or smtp.office365.com:")
        self.Val1Lbl.grid(row=0, column=0, sticky='E', padx=5, pady=2)
        self.Val1Txt = Tkinter.Entry(stepOne)
        self.Val1Txt.grid(row=0, column=1, columnspan=3, pady=2, sticky='WE')

        self.Val2Lbl = Tkinter.Label(stepOne,text="Sender email address, e.g. dan.cook@scienceopen.com or cookdj0128@gmail.com:")
        self.Val2Lbl.grid(row=1, column=0, sticky='E', padx=5, pady=2)
        self.Val2Txt = Tkinter.Entry(stepOne)
        self.Val2Txt.grid(row=1, column=1, columnspan=3, pady=2, sticky='WE')

        self.Val3Lbl = Tkinter.Label(stepOne,text="Email password:")
        self.Val3Lbl.grid(row=2, column=0, sticky='E', padx=5, pady=2)
        self.Val3Txt = Tkinter.Entry(stepOne)
        self.Val3Txt.grid(row=2, column=1, columnspan=3, pady=2, sticky='WE')

        self.Val4Lbl = Tkinter.Label(stepOne,text="Email Subject, e.g. 'Request to Peer Review Research Article': ")
        self.Val4Lbl.grid(row=3, column=0, sticky='E', padx=5, pady=2)
        self.Val4Txt = Tkinter.Entry(stepOne)
        self.Val4Txt.grid(row=3, column=1, columnspan=3, pady=2, sticky='WE')

        self.val1 = None
        self.val2 = None
        self.val3 = None
        self.val4 = None

        SubmitBtn = Tkinter.Button(stepOne, text="Submit",command=self.submit4)
        SubmitBtn.grid(row=6, column=3, sticky='W', padx=5, pady=2)
    def submit4(self):

        self.SenderEmailServer=self.Val1Txt.get()
        if self.SenderEmailServer=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.SenderEmailAddress=self.Val2Txt.get()
        if self.SenderEmailAddress=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.PassWord=self.Val3Txt.get()
        if self.PassWord=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()

        self.SubjectLine=self.Val4Txt.get()
        if self.SubjectLine=="":
            Win2=Tkinter.Tk()
            Win2.withdraw()
        self.quit()

def sendTheEmailsGuiSubmit():
    x_to_y = sendEmailGUI(None)
    x_to_y.title('Open Peer Review App')
    x_to_y.mainloop() #this will run until it closes
    return x_to_y.SenderEmailServer, x_to_y.SenderEmailAddress, x_to_y.PassWord, x_to_y.SubjectLine

while n == "":
    try:
        d = getResults(newpath, AuthorLastName,reviewManager,article,author,authorAffliation,abstract,homepage,emailText)
        writeResults(d, AuthorLastName)
        print "I wrote the results to file"
        constructEmail(d, AuthorLastName)
        print "I created the emails to the authors"
        if len(emailDict.keys()) > 0:
            lenOfResults = max(emailDict.keys())
            incrementer=1
            for thisKeyFromThisCurrentDict in d:
                emailDict[lenOfResults+incrementer]=d[thisKeyFromThisCurrentDict]
                incrementer=incrementer+1
        if len(emailDict.keys()) == 0:
            emailDict.update(d)
        del(d)
        n  = goAgain()
    except ValueError:
        print "something went wrong."

answers=["s", "y"]
sendTheEmails = sendTheEmailButton()
#for thisAnswer in sendTheEmails:
#    while thisAnswer not in answers:
#        sendTheEmails = [raw_input("Hit enter to send the emails, enter 's' to skip emails: ")]

if "y" in sendTheEmails:
    SenderEmailServer, SenderEmailAddress, SenderEmailPassword, SubjectLine = sendTheEmailsGuiSubmit()
    print SenderEmailServer
    print SenderEmailAddress
    print SenderEmailPassword
    print SubjectLine
    for i in emailDict.keys():
        if emailDict[i]["email"] not in allOldEmails:
            print "sending to...", emailDict[i]["email"]
            print emailDict[i]["emailTextFile"]
            try:
                sendEmail(AuthorLastName=AuthorLastName, SERVER=SenderEmailServer, FROM=SenderEmailAddress, TO=emailDict[i]["email"],
                 SUBJECT=SubjectLine, TEXT="load file",PASSWORD=SenderEmailPassword, LOADFILE=emailDict[i]["emailTextFile"])
                print "Sent email to: ", emailDict[i]["email"]
            except:
                print "Sorry. Something seems to be broken. We didn't send the message to: ", emailDict[i]["email"]
                print "--------"
if "s" in sendTheEmails:
    print "The csv file and the txt emails are available in the author folder."
