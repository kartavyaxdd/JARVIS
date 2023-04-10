import random
import pyperclip
import pyttsx3
import datetime
import speech_recognition as sr
import smtplib
from secrets_1 import senderEmail, epwd, to
import pyautogui
import webbrowser as wb
from time import sleep
import wikipedia
import requests
import openai
from dotenv import load_dotenv
import pywhatkit
import pyjokes
from googletrans import Translator
import os
import time as tt
import string
from nltk.tokenize import word_tokenize
import speedtest

for i in range(3):
    a = input("Enter Password to open - ")
    pw_file = open("password.txt","r")
    pw = pw_file.read()
    pw_file.close()
    if (a==pw):
        print("Welcome back master")
        break
    elif (i==2 and a!=pw):
        exit()

    elif (a!=pw):
        print("Try Again")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate',170)


def takeCommandMIC():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source,0,8)
    try:
        print("recognizing....")
        query = r.recognize_google(audio, language= "en-in")
        print(query)
        return query.lower()
    except Exception as e:
        print(e)
        speak("")
        return None


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("THe current time is")
    speak(Time)

def roll_dice():
    # Generate a random number between 1 and 6
    result = random.randint(1, 6)
    print(f"the dice rolls and the result is{result}")
    speak("The dice rolls and the result is " + str(result))
    return result

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    Date = int(datetime.datetime.now().day)
    speak("the current date is ")
    speak(Date)
    speak(month)
    speak(year)


def wishme():
    greeting()
    speak("Welcome back sir")
    speak("jarvis at your service sir.,please tell me, how can i help you?")


def greeting():
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("good morning sir")
    elif hour >= 12 and hour < 18:
        speak("good after noon sir")
    elif hour >= 18 and hour < 24:
        speak("Good evening sir")
    else:
        speak("Good night")


def takecommandcmd():
    query = input("how can i help you\n")
    return query


def sendemail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderEmail, epwd)
    emailmsg = takeCommandMIC()
    speak("what should i say")
    server.sendmail(senderEmail, to, emailmsg)
    server.close()
def screenshot():
    speak("taking screenshot")
    name_img = tt.time()
    name_img = f'D:\\python\\vision\\vision screenshots\\{name_img}.png'
    img = pyautogui.screenshot(name_img)
    img.show()
def translation():
    # Prompt user for the text to translate
    speak("What would you like to translate?")
    text = takeCommandMIC()

    # Prompt user for the language to translate to
    speak("What language would you like to translate to?")
    lang = takeCommandMIC()

    # Translate the text using the Google Translate API
    translator = Translator()
    translation = translator.translate(text, dest=lang)

    # Speak the translated text
    speak(f"The translation is {translation.text}")

def read_selected_text():
    selected_text = pyperclip.paste()
    if selected_text:
        speak(selected_text)
    else:
        print("No text selected.")
def sendwpmsg(phone_no, message):
    Message = message
    wb.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+Message)
    sleep(25)
    pyautogui.press('enter')
def searchgoogle():
    speak('what should i search on google')
    search = takeCommandMIC()
    if search:
        wb.open('https://www.google.com/search?q=' + search)
    else:
        speak("I'm sorry, I didn't catch that. Please try again with a valid search query.")

def passgen():
    s1=string.ascii_uppercase
    s2=string.ascii_lowercase
    s3=string.digits
    s4=string.punctuation
    passlenth = 8
    s=[]
    s.extend(list(s1))
    s.extend(list(s2))
    s.extend(list(s3))
    s.extend(list(s4))

    random.shuffle(s)
    newpass = ("".join(s[0:passlenth]))
    print(newpass)
    speak(newpass)




def flip_coin():
    speak("I'm flipping the coin. Please wait...")
    result = random.choice(['heads', 'tails'])
    speak(f"The result is {result}")
    return result

fileopen = open("api.txt","r")
API = fileopen.read()
fileopen.close()
openai.api_key = API
load_dotenv()
completion = openai.Completion()

def gpt_output(question,chat_log = None):
    FileLog = open("chat_log.txt","r", encoding="utf-8")
    chat_log_template = FileLog.read()
    FileLog.close()
    if chat_log is None:
        chat_log = chat_log_template
    prompt = f'{chat_log}You : {question}\nVision : '
    response = completion.create(
        model = "text-davinci-003",
        prompt=prompt,
        temperature = 0.5,
        max_tokens = 80,
        top_p = 0.3,
        frequency_penalty = 0.5,
        presence_penalty = 0)
    answer = response.choices[0].text.strip("jarvis :")
    chat_log_template_update = chat_log_template + f"\nYou : {question} \njarvis : {answer}"
    FileLog = open("chat_log.txt","w", encoding="utf-8")
    FileLog.write(chat_log_template_update)
    FileLog.close()
    print(answer)
    speak(answer)
if __name__ == "__main__":
    speak("Hello this is jarvis")
    wakeword = 'jarvis'
    while True:
        import nltk

        query = takeCommandMIC()
        query1=query
        if query is not None and wakeword in query:
            # do something

        # if wakeword in query:
                if "time" in query:
                    time()
                elif "date" in query:
                    date()
                elif 'offline' in query:
                    speak("good bye!")
                    break
                if 'message' in query:
                    user_name = {
                        #your contacts here in the format of:
                        'Jarvis' : '+91 9999999999',
                        'Friday' : '+91 7878827812'
                    }
                    try:
                        speak("to whom should i send the whatsapp message?")
                        name = takeCommandMIC()
                        phone_no = user_name[name]
                        speak("what should be the message?")
                        message = takeCommandMIC()
                        sendwpmsg(phone_no, message)
                        speak("message has been sent")
                    except Exception as e:
                        print(e)
                        speak('failed to send message')

                if 'wikipedia' in query:
                    try:
                        speak('Searching Wikipedia...')
                        query = query.replace("wikipedia", "")
                        results = wikipedia.summary(query, sentences=2)
                        speak("According to Wikipedia")
                        print(results)
                        speak(results)
                    except Exception as e:
                        print(e)
                        speak("Nothing found like this")
                elif 'read' in query:
                    read_selected_text()
                elif 'search' in query:
                    searchgoogle()
                    speak('Here are the search result')

                # if 'news' in query:
                #     news()

                elif 'youtube' in query:
                    speak("What should i search on youtube")
                    topic = takeCommandMIC()
                    pywhatkit.playonyt(topic)
                    speak(f"playing")

                elif 'weather' in query:
                    city = input("Whats The Name of Your city?   ")
                    apikey = input("Paste Your OpenWeather api key here:  ")
                    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={apikey}"
                    res = requests.get(url)
                    data = res.json()
                    weather = data['weather'] [0] ['main']
                    temp =  data['main']['temp']
                    temp = round((temp-32)*5/9)
                    dsp = data['weather'] [0] ['description']
                    print(weather)
                    print(temp)
                    print(dsp)
                    speak('the current temperature is {} celcious'.format(temp))
                    speak('the current weather is {}'.format(dsp))
                elif "open documents" in query:
                    os.system('explorer C://')
                elif 'flip' in query:
                    flip_coin()
                elif "open code" in query:
                    codepath= "C:\\Users\\DELL\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                    os.startfile(codepath)
                elif "open after effects" in query:
                    codepath = "#your file path here"
                    os.startfile(codepath)
                if 'joke' in query:
                    joke = pyjokes.get_joke()
                    print(joke)
                    speak(joke)
                elif 'translate' in query:
                    translation()
                elif 'email' in query:
                    sendemail()
                elif 'screenshot' in query:
                    screenshot()
                elif 'remember that' in query:
                    speak("what shall i remember")
                    data= takeCommandMIC()
                    speak("you said me to remember that"+data)
                    remember = open('data.txt','w')
                    remember.write(data)
                    remember.close
                elif 'what did i said you to remember' in query:
                    remember = open('data.txt','r')
                    speak('you told me to remember that'+remember.read())
                elif 'password' in query:
                    passgen()
                elif 'roll' in query:
                    roll_dice()

                elif "internet speed" in query:
                    speak('checking your wifi speed')
                    wifi  = speedtest.Speedtest()
                    upload_net = wifi.upload()/1048576         #Megabyte = 1024*1024 Bytes
                    download_net = wifi.download()/1048576
                    print("Wifi Upload Speed is", upload_net)
                    print("Wifi download speed is ",download_net)
                    speak(f"Wifi download speed is {download_net}")
                    speak(f"Wifi Upload speed is {upload_net}")
                elif "play a game" in query:
                    from game import game_play
                    game_play()
                elif "focus mode" in query or 'focus mod' in query:
                    a = int(input("Are you sure that you want to enter focus mode :- [1 for YES / 2 for NO "))
                    if (a==1):
                        speak("Entering the focus mode....")
                        os.startfile("D:\python\vision\FocusMode.py")
                        exit()

                        
                    else:
                        pass

                elif "show my focus" in query:
                    from FocusGraph import focus_graph
                    focus_graph()
                elif "feel" in query:
                    speak("I am feeling absolutely fine sir")

                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")
                
                elif "ipl score" in query:
                    from plyer import notification  #pip install plyer
                    import requests #pip install requests
                    from bs4 import BeautifulSoup #pip install bs4
                    url = "https://www.cricbuzz.com/"
                    page = requests.get(url)
                    soup = BeautifulSoup(page.text,"html.parser")
                    team1 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[0].get_text()
                    team2 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[1].get_text()
                    team1_score = soup.find_all(class_ = "cb-ovr-flo")[8].get_text()
                    team2_score = soup.find_all(class_ = "cb-ovr-flo")[10].get_text()

                    a = print(f"{team1} : {team1_score}")
                    b = print(f"{team2} : {team2_score}")

                    notification.notify(
                        title = "IPL SCORE :- ",
                        message = f"{team1} : {team1_score}\n {team2} : {team2_score}",
                        timeout = 15
                    )

                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
                    volumeup() 
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()

                elif "shutdown system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                        pass

                elif "hidden menu" in query:
                    pyautogui.hotkey('winleft', 'x')   
                elif "task manager" in query:

                    pyautogui.hotkey('ctrl', 'shift', 'esc')

                elif "task manager" in query:
    # Ctrl+Shift+Esc: Open the Task Manager
                    pyautogui.hotkey('ctrl', 'shift', 'esc')

                elif 'setting' in query:
                    pyautogui.hotkey('winleft', 'i')

                else:
                    if 'whatsapp' not in query:
                        gpt_output(query1)
                