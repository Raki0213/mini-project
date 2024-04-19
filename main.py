import cv2
import face_recognition
import speech_recognition as sr
import pyttsx3
#import pywhatkit
import datetime
# import wikipedia
# import pyjokes

# Load and encode known faces
known_face_names = ['ganesh']  # Add more known names
known_face_encodings = []

for name in known_face_names:
    known_face_image = face_recognition.load_image_file(f"known_faces/{name.lower()}.jpg")
    known_face_encoding = face_recognition.face_encodings(known_face_image)[0]
    known_face_encodings.append(known_face_encoding)

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def recognize_and_greet():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame.")
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            cv2.imshow("Face and Voice Recognition Robot", frame)

            if any(matches):
                matched_index = matches.index(True)
                name = known_face_names[matched_index]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                response = f"Hi {name}! How can I assist you?"
                talk(response)
                print(response)
                cap.release()
                #cv2.destroyAllWindows()
                break

            if "Unknown" in name:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                response = "Hello there! Nice to meet you."
                print(response)
                talk(response)
                cap.release()
                #cv2.destroyAllWindows()
                break

        cv2.imshow("Face and Voice Recognition Robot", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alpha' in command:
                command = command.replace('alpha', '')
                print(command)
    except:
        pass
    return command


def run_alexa():
    command = take_command()
    #command=input("enter the command: ")
    print(command)
    if 'hello' in command:
        recognize_and_greet()
    elif 'how are you' in command:
        talk('I am doing great, thanks for asking. Hope you are also doing great')
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'date' in command:
        talk('sorry, I have a boyfriend')
    elif 'are you single' in command:
        talk('I am in a relationship with wifi')
    # elif 'joke' in command:
    #     print(pyjokes.get_joke())
    #     talk(pyjokes.get_joke())
    elif 'electrical block' in command:
        talk('Electrical block is located in the N block')
    # elif 'who is' in command:
    #     person = command.replace('who is', '')
    #     info = wikipedia.summary(person, 1)
    #     print(info)
    #     talk(info)
    # elif 'play' in command:
    #     song = command.replace('play', '')
    #     talk('playing ' + song)
    #     pywhatkit.playonyt(song)
    elif 'thanks' in command:
        talk("It's my pleasure to help you")
    else:
        talk('Please say the command again.')


while True:
    run_alexa()