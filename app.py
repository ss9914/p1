import json
import os
import streamlit as st
import random
from openai import OpenAI
import streamlit as st
import speech_recognition as sr
import playsound 
from dotenv import load_dotenv
from gtts import gTTS
from time import sleep
from deep_translator import GoogleTranslator
from pathlib import Path
import tempfile
load_dotenv()
st.set_page_config(
    page_title="Voice Assistant",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

session_state = st.session_state
if "user_index" not in st.session_state:
    st.session_state["user_index"] = 0

account_number = ""
pin =''
task=''


def play_audio(text):
    try:
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            file_path = tmp_file.name

        # Generate and save the speech audio to the temporary file
        speech = gTTS(text=text, lang='en', slow=False)
        speech.save(file_path)

        # Play the audio file
        playsound.playsound(file_path)
    except Exception as e:
        st.error(f"Error playing audio: {str(e)}")
    finally:
        # Remove the temporary file after use
        if os.path.exists(file_path):
            os.remove(file_path)
def withdraw(acc_no, amount, pin):
    st.write(amount)
    st.write(f"Account number {acc_no}")

    with open('accounts.json', 'r+') as f:
        data = json.load(f)
        accounts = data['accounts']
        account_exists = False
        for acc in accounts:
            if acc['account_number'] == acc_no:
                account_exists = True
                if acc['pin'] != pin:
                    play_audio("Incorrect PIN. Please try again.")
                    play_audio('Thavarana pin. Meendum Muyarchikkavum')
                    st.write("Incorrect PIN. Please try again.")
                    return
                if acc['balance'] < int(amount):
                    st.write("Insufficient balance. Please try again.")
                    play_audio("Insufficient balance. Please try again.")
                    return
                acc['balance'] -= int(amount)
                break

        if not account_exists:
            st.write("Invalid account number. Please try again.")
            play_audio("Invalid account number. Please try again.")
            play_audio(' Kanakku Illai')
            return

        # Write the updated data back to the file
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    st.success(f"Withdrawing Rs. {amount} from account {acc_no} successful. New balance: {acc['balance']}")
    play_audio(f"Withdrawing  from account {acc_no}. New balance: {acc['balance']}")
    play_audio(f"Kanakkilirundhu Rubaai {amount} eduka padugiradhu. Pudhiya iruppu: {acc['balance']}")
    

def transfer(amount, acc_no_from, acc_no_to, pin):
    st.write(amount)
    st.write(acc_no_from)
    st.write(acc_no_to)
    if pin:
        with open('accounts.json', 'r') as f:
            data = json.load(f)
            accounts = data['accounts']
            account_exists_from = False
            account_exists_to = False
            for acc in accounts:
                if acc['account_number'] == acc_no_from:
                    account_exists_from = True
                
                # if acc['pin'] != pin:
                #     st.write("Incorrect PIN. Please try again.")
                #     play_audio('Thavarana pin. Meendum Muyarchikkavum')
                #     return
                if acc['balance'] < int(amount):
                    st.write("Insufficient balance. Please try again.")
                    return

            # for acc in accounts:
            #     if acc['account_number'] == acc_no_to:
            #         account_exists_to = True
            #         break

            # if not account_exists_from:
            #     play_audio("Invalid Sender account number. Please try again.")
            #     play_audio(' Thavarana anupunar kanakku en . Dhayavai seidhu meendum Muyarchikkavum ')
            #     st.write("Sender account does not exist.")
            #     return
            # if not account_exists_to:
            #     play_audio("Invalid Reciever account number. Please try again.")
            #     st.write("Receiver account does not exist.")
            #     return

            for acc in accounts:
                if acc['account_number'] == acc_no_from:
                    acc['balance'] -= int(amount)
                elif acc['account_number'] == acc_no_to:
                    acc['balance'] += int(amount)

            with open('accounts.json', 'w') as f:
                json.dump(data, f, indent=4)
            play_audio(f"Transfer successful. ")
            play_audio(f" Parimaatram vetrigaramaga nadandhadhu . Pudhiya iruppu {acc_no_from}")
            st.write(f"Transfer successful. {acc_no_from}")

def deposit(amount, acc_no, pin):
    print(amount)
    print(acc_no)
    if pin  :
        with open('accounts.json', 'r') as f:
            data = json.load(f)
            accounts = data['accounts']
            account_exists = False
            for acc in accounts:
                if acc['account_number'] == acc_no:
                    account_exists = True
                    if acc['pin'] != pin:
                        play_audio("Incorrect PIN. Please try again.")
                        play_audio('Thavarana pin. Meendum Muyarchikkavum')
                        st.write("Incorrect PIN. Please try again.")
                        return
                    break

            if not account_exists:
                play_audio("Account does not exist.")
                play_audio(' Kanakku Illai')
                st.write("Account does not exist.")
                return
            for acc in accounts:
                if acc['account_number'] == acc_no:
                    acc['balance'] += int(amount)

            with open('accounts.json', 'w') as f:
                json.dump(data, f, indent=4)
            play_audio(f"Deposit successful")
            st.write(f"Deposit successful. New balance for {acc_no}")

def balance_inquiry(acc_no, pin):
    st.write(acc_no)
    if pin :
        with open('accounts.json', 'r') as f:
            data = json.load(f)
            accounts = data['accounts']
            account_exists = False
            for acc in accounts:
                if acc['account_number'] == acc_no:
                    account_exists = True
                    if acc['pin'] != pin:
                        st.write("Incorrect PIN. Please try again.")
                        play_audio('Thavarana pin. Meendum Muyarchikkavum')
                        return
                    play_audio(f"Your current balance is {acc['balance']} rs")
                    play_audio(f"Ungal tharpodhaiya iruppu {acc['balance']} rs")
                    st.write(f"Your current balance is {acc['balance']} rs")
                    return

            if not account_exists:
                play_audio("Account does not exist.")
                play_audio(' Kanakku Illai')
                st.write("Account does not exist.")
                return


def change_pin(acc_no, current_pin):
    st.write(acc_no)
    play_audio('Enter New Pin')
    play_audio(' Pudhu pinnai Ul idavum')
    new_pin = st.text_input("Enter your new PIN", type="password")
    sleep(3)
    if new_pin:
        hashed_current_pin = (current_pin)
        hashed_new_pin = (new_pin)

        with open('accounts.json', 'r') as f:
            data = json.load(f)
            accounts = data['accounts']
            account_exists = False
            for acc in accounts:
                if acc['account_number'] == acc_no:
                    account_exists = True
                    # if acc['pin'] != hashed_current_pin:
                    #     play_audio("Incorrect current PIN. Please try again.")
                    #     st.write("Incorrect current PIN. Please try again.")
                    #     return
                    acc['pin'] = hashed_new_pin
                    break

        with open('accounts.json', 'w') as f:
            json.dump(data, f, indent=4)
        play_audio("PIN change successful.")
        play_audio(' Pin vetrigaramaga maatrapattadhu')
        st.write("PIN change successful.")

def generateAccountNumber():
    account = "".join([str(random.randint(0, 9)) for _ in range(10)])
    return account
        

def play_audio(text):
    speech = gTTS(text=text, lang='en', slow=False)
    speech.save('audio.mp3')
    playsound.playsound('audio.mp3')
    if os.path.exists('audio.mp3'):
        os.remove('audio.mp3')
    return True

def voice_assistant(voice_command):
    try:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        tasks = ['Withdraw', 'Balance', 'Transfer', 'Change PIN','Deposit','Exit']
        command_segments = voice_command.split(' ')
        task = ''
        amount = ''

        prompt = f"""
            You're a voice assistant for the ATM. Your task is to identify the intent of the user's voice command and segment the command into the following categories:

            1. Task: Withdraw, Balance, Transfer, Change PIN, Deposit, Exit
            2. Amount: Any numeric value (e.g., 1000)


            Voice Command: "{voice_command}"

            You should return the segmented categories separated by commas.

            For example:
            - "Withdraw 1000" should return: Withdraw,1000
            - "Transfer 500" should return: Transfer,500
            - "I want to deposite rupees 100" should return: Deposite,100
            - "I dont want to withdraw 100" should return: None,None
            - "I want to Change Pin" should return: Change Pin,None

            If the voice command is not clear or does not match any of the categories or the user intent doest not match any of the categories, return an empty string.
        """
        messages = [{"role": "system", "content": prompt}]
        response = client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo-0125",
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
def validate_task(task, amount):
    if task=='Withdraw' and len(amount)>0 and amount.strip() != "None":
        return True
    if task=='Deposit' and len(amount)>0 and amount.strip() != "None" :
        return True
    if task=='Transfer' and len(amount)>0 and amount.strip() != "None":
        return True
    if task=='Change PIN':
        return True 
    if task=='Balance':
        return True
    return False  
def get_voice_input(prompt):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        playsound.playsound(prompt)  # Play the prompt asking for input
        audio = recognizer.listen(source)
    
    try:
        voice_input = recognizer.recognize_google(audio)
        return voice_input
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return None
def main():
    st.markdown(
    """
    <style>
    body {
        background-color: Brown; 
        color: white;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
        )
    st.markdown(
        """
        <style>
        .stApp {
            background: url("https://t3.ftcdn.net/jpg/06/14/70/02/240_F_614700207_vBV0ljBPlnx3WjesnIEIAEifVZtYn0g6.jpg");
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("WELCOME TO THE ATM")
    
    play_audio('Welcome to the ATM')
    play_audio('ATM il Vaazhthukkal')

    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write('         ')

    with col2:
        st.image("ATM1.png" ,width=550)

    with col3:
        st.write('          ')
    translator = GoogleTranslator(source='auto', target='en')
    
    with st.form(key="voice_command_form"):
        pin = st.text_input("Enter your PIN", type="password")
        play_audio("Please enter your pin to continue")
        play_audio('Toṭara uṅkaḷ piṉṉai uḷḷiṭavum')
        account_number = st.text_input("Enter the account number to perform the transaction", type="password")
        play_audio("Enter Your Account Number to transact with")
        play_audio('Parivarttaṉai ceyya uṅkaḷ kaṇakku eṇṇai uḷḷiṭavum')
        
        submit_button = st.form_submit_button(label="Submit")
        if submit_button:
            with open('accounts.json', 'r') as f:
                data = json.load(f)
                accounts = data['accounts']
                account_exists = False
                for acc in accounts:
                    if acc['account_number'] == account_number:
                        account_exists = True
                        if acc['pin'] != pin:
                            play_audio("Incorrect PIN. Please try again.")
                            play_audio('Thavarana pin. Meendum Muyarchikkavum')
                            st.write("Incorrect PIN. Please try again.")
                            return
                        break

                if not account_exists:
                    play_audio("Account does not exist.")
                    play_audio(' Kanakku Illai')
                    st.write("Account does not exist.")
                    return

            while True:
                play_audio("Please speak your command")
                recognizer = sr.Recognizer()
                microphone = sr.Microphone()
                with microphone as source:
                    try:
                        print("Listening...")
                        recognizer.adjust_for_ambient_noise(source)
                        audio = recognizer.listen(source)   
                        voice_command_tamil = recognizer.recognize_google(audio, language="ta-IN")
                        print("Input (Tamil):", voice_command_tamil)
                        st.write(voice_command_tamil)
                        # Translate Tamil input to English
                        voice_command_english = translator.translate(voice_command_tamil)
                        print("Translated (English):", voice_command_english)
                        
                        response = voice_assistant(voice_command_english).split(",")
                        task = response[0].strip()
                        amount = response[1].strip()
                        
                        print(response)
                        print("VT",validate_task(task,amount))
                        if validate_task(task,amount):
                            break
                        else:
                            play_audio("Invalid Command")
                            play_audio("Thavarana Kattalai")
                        st.write(task)
                        if amount.strip() != "None":
                            amount = int(amount.strip())
                    except Exception as e:
                        print(e)
                        play_audio("Could not understand audio. Listening again...")
            try:

                with st.spinner("Processing..."):
                    if task == 'Withdraw':
                        print('Withdraw')
                        withdraw(account_number, amount, pin)
                        st.rerun()
                    elif task == 'Transfer':
                        print('Transfer')
                        transfer(amount, account_number, account_number, pin)
                        st.rerun()
                    elif task == 'Deposit':
                        print('D')
                        deposit(amount, account_number, pin)
                        st.rerun()  
                    elif task == 'Balance':
                        print('B')
                        balance_inquiry(account_number,pin)
                        st.rerun()  
                    # elif task == 'Change PIN':
                    #     print('Change_Pin')
                    #     change_pin(account_number, pin)
                    #     st.rerun()  
            except Exception as e:
                print(e)
                play_audio("Could not understand audio. Listening again...")

                st.rerun()
    # if st.button("Give another command"):
    #     st.rerun()            
        

if __name__ == "__main__":
    # import os 
    # if os.path.exists("audio.mp3"):
    #     os.remove("audio.mp3")

    # initialize_database()
    main()


