from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import schedule
import smtplib
import time
import requests
from datetime import datetime
import openai
import speech_recognition as sr
import pyttsx3
import webbrowser
import pywhatkit
import pyautogui
import cv2

openai.api_key = "replace-with-your-openai-api-key" 


# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty('voice', voices[1].id)

def wishMe():
    hour = int(datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Zira sir. Plase tell me how may I help you")
    
def send_email(email_list, subject_entry, body_text):
    sender_email = "yadavyash11062004@gmail.com"
    sender_password = "dyyovwayzkdeecby" # Replace with your own Gmail password
    subject = subject_entry.get()
    body = body_text.get("1.0", "end-1c")
    message = f"Subject: {subject}\n\n{body}"
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(sender_email, sender_password)
            for email in email_list:
                connection.sendmail(from_addr=sender_email, to_addrs=email, msg=message)
            messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {e}")

def open_popup():
    global email_entry, subject_entry, body_text, time_entry

    popup_window =  Toplevel(root)

    email_entry =  Entry(popup_window, width=70)
    subject_entry =  Entry(popup_window, width=70)
    body_text =  Text(popup_window, width=70, height=20)
    time_entry =  Entry(popup_window)

    email_label =  Label(popup_window, text="Recipient Emails (To send multiple peolpe use comma separated emails):")
    subject_label =  Label(popup_window, text="Subject:")
    body_label =  Label(popup_window, text="Message Body:")
    time_label =  Label(popup_window, text="Time (in HH:MM format):")

    send_button =  Button(popup_window, text="Send Email", command=lambda: [send_email(email_entry.get().split(','), subject_entry, body_text), popup_window.destroy()])
    email_label.pack()
    email_entry.pack()
    subject_label.pack()
    subject_entry.pack()
    body_label.pack()
    body_text.pack()
    time_label.pack()
    time_entry.pack()
    send_button.pack()

    def schedule_email():
     scheduled_time = time_entry.get()

     def send_scheduled_email():
        send_email(email_entry.get().split(','), subject_entry, body_text),stop_scheduler(),popup_window.destroy()
        
        
     job = schedule.every().day.at(scheduled_time).do(send_scheduled_email)
     messagebox.showinfo("Success", "Email scheduled successfully!")
     running = True

     def stop_scheduler():
        nonlocal running
        running = False

     while running:
        schedule.run_pending()
        time.sleep(1)

            

    schedule_button =  Button(popup_window, text="Schedule Email", command=schedule_email)
    schedule_button.pack()

def Photo():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Pythonn webcam")
    img_counter = 0
    while True:
        ret,frame = cam.read()
        if not ret:
            print("Failed to grad frame ")
            break
        cv2.imshow("ZIRA WebCam",frame)
        k = cv2.waitKey(1)
        if k%256 ==27:
            print("Escape hit , closing the app")
            break
        elif k%256 == 32:
            img_name = "ZIRA_CAM_{}.png".format(img_counter)
            cv2.imwrite(img_name,frame)
            img_counter +=1
            textArea.insert(END, f"Zira: Photo {img_counter} Saved \n\n")
            print(f"Photo {img_counter} Saved ")
            speak(f"Photo {img_counter} Saved")
    cam.release()
    cv2.destroyAllWindows()


    
def take_screenshot():
    counter = 1  # initialize a counter to keep track of screenshots
    screenshot = pyautogui.screenshot()
    # Open a file dialog to choose a directory to save the screenshot
    directory = filedialog.askdirectory()
    if directory:
        # If a directory was chosen, save the screenshot to that directory with a unique name
        now = datetime.now()
        file_path = f"{directory}/screenshot_{now.strftime('%Y%m%d_%H%M%S')}_{counter}.png"
        screenshot.save(file_path)
        counter += 1 

def ai_response(user_question):
    model = "text-davinci-003"
    completion = openai.Completion.create(
        model=model,
        prompt=user_question,
        max_tokens=2024,
        temperature=0.5,
        n=1,
        stop=None
    )
    return completion.choices[0].text



def speak(text):
    engine.say(text)
    engine.runAndWait() 
   
def reply():
    question = qField.get()
    textArea.insert(END, "YOU: " + question.capitalize() + "\n\n")

    if "open " in question:
        ope,web = question.split(" ")
        webbrowser.open(web+".com")
        textArea.insert(END, "Zira: opening "+web+" \n\n")
        speak(f"opening {web}")
  

    elif 'time' in question:
        time = datetime.now().strftime('%I:%M %p')
        textArea.insert(END, "Zira: Current time of is " + time + "\n\n")
        speak('Current time is ' + time) 

    elif "screenshot" in question:
        take_screenshot() 
        textArea.insert(END, "Zira: Screenshot Saved \n\n") 
        speak("Screenshot saved")
        
    elif "take a photo" in question or "take photo" in question or "photo mode" in question :
        textArea.insert(END, "Zira: Photo Saved \n\n") 
        speak("Press Spacebar to take photo")
        speak("Press Escape to exit") 
        Photo()

    elif "write a program" in question or "write a code" in question or "Write a program" in question or "Write a code" in question :
        response = ai_response(question)
        textArea.insert(END, "Zira: " + response + "\n\n")     
    
    elif "weather mode" in question or "weather" in question or "check weather" in question:
        show_weather_popup() 
        speak('weather mode activated')   

    elif "activate email mode" in question or"Activate email mode" in question or "Activate Email Mode" in question:
        open_popup()
        speak("Email mode is activited")

    elif "repeat after me" in question :
        say = question.replace("repeat after me"," ")
        speak(say)
        textArea.insert(END, "Zira: "+say.capitalize()+ "\n\n")

    elif "text to speech mode:" in question:
        say = question.replace("text to speech mode:"," ")
        speak(say)
        textArea.insert(END, "Zira: "+say.capitalize()+ "\n\n")

    elif "speech to text" in question:
        say = question.replace("speech to text"," ")
        textArea.insert(END, "Zira: "+say.capitalize()+ "\n\n")

    elif "play" in question:
        song = question.replace('play', '')
        speak('playing ' + song)
        textArea.insert(END, "Zira: playing" +song  + "\n\n")
        pywhatkit.playonyt(song)

    elif"clear screen" in question:
        textArea.delete('1.0', 'end')

    else:
        response = ai_response(question)
        speak(response)
        textArea.insert(END, "Zira: " + response + "\n\n")         
    qField.delete(0, END)               
    


def speechRecognition():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source,duration=1)
            audio = r.listen(source)        
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print("User said:"+query)
            qField.delete(0,END)
            qField.insert(0,query)
            reply()
       

    except Exception as e:
        print(e)
        print("try again please...")
        return "None"
    return query


root = Tk()
root.geometry('500x600+700+30')
root.title("ZIRA A.I (Artificial Intelligence)")
root.config(bg='#2a2745')

# Logo Label
logo_label = Label(
    root,
    text='ZIRA A.I',
    font=('times new roman', 35, 'bold'),
    bg='#3d3963',
    fg='white',
    highlightthickness=2,
    highlightbackground="gray",
    highlightcolor="white"
)
logo_label.pack()

# center frame 1
centerFrame1=Frame(root,border=2,relief="solid",height=5,bg='#3d3963')
centerFrame1.pack(pady=5,fill="both")

# Question Field
qField = Entry(
    centerFrame1,
    font=('times new roman', 14, 'bold'),
    bg='#3d3963',
    fg='white',
    highlightthickness=2,
    highlightbackground="gray",
    highlightcolor="white",
    width=43
)
qField.pack(side=LEFT, fill=X)

submit_button = Button(centerFrame1,text='Enter',font=('times new roman',12), bg='#3d3963',
    fg='white',
    height=1,
    width=5,
    command=reply)
submit_button.pack(side=RIGHT)

# Center Frame
center_frame = Frame(root)
center_frame.pack(pady=10, fill=BOTH)



# Scrollbar
sbar = Scrollbar(center_frame, bg='#2a2745', width=15)
sbar.pack(side=RIGHT, fill=Y)

# Text Area
textArea = Text(
    center_frame,
    width=112,
    height=15,
    font=('times new roman', 18, 'bold'),
    yscrollcommand=sbar.set,
    wrap='word',
    bg='#3d3963',
    fg='white',
    highlightthickness=2,
    highlightbackground="gray",
    highlightcolor="white"
)
textArea.pack(side=LEFT, fill=BOTH)
sbar.config(command=textArea.yview)

#speak button
speak_button = Button(
    root,
    text='SPEAK',
    font=('times new roman', 10, 'bold'),
    height=2,
    width=10,
    bg='#3d3963',
    fg='white',
    command=speechRecognition 
)
speak_button.pack()


# Binding Enter key to Submit button
def click(event):
    submit_button.invoke()
root.bind("<Return>", click)

def get_weather_data(city):
    api_key = "replace-with-your-OpenWeatherMa-api-key"  # replace with your own OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        description = data["weather"][0]["description"]
        return f"Current weather in {city}: {description}, temperature: {temp}°C, feels like: {feels_like}°C"
    else:
        return f"Error getting weather data: {response.status_code}"

# Function to handle button click event for popup window
def show_weather(city):
    weather_data = get_weather_data(city)
    textArea.insert(END, "Zira:"+ weather_data +"\n\n") 
    speak(weather_data)
    

# Function to show weather popup window
def show_weather_popup():
    popup_window = Toplevel()
    popup_window.geometry("300x100")
    popup_window.title("Enter City")
    city_label = Label(popup_window, text="Enter city:")
    city_entry = Entry(popup_window)
    submit_button = Button(popup_window, text="Get Weather", command=lambda: show_weather(city_entry.get()))
    city_label.pack()
    city_entry.pack()
    submit_button.pack()

wishMe()
root.minsize(500,600)
root.maxsize(500,600)
# Main Loop
root.mainloop()


