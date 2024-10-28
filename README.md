# p1
I developed a project that enables blind people to use ATM machines more easily.
ATM Voice Assistant for the Visually Impaired
This project is a voice-enabled ATM application designed to assist visually impaired users with ATM transactions. It provides a voice-guided interface to allow users to interact with ATMs via spoken commands and audio feedback, offering a more accessible banking experience.

Features
Voice Command Processing: Accepts voice commands for transactions like withdrawals, deposits, balance inquiries, transfers, and PIN changes.
Audio Feedback: Provides audio guidance for each step, ensuring a smooth and accessible user experience.
Multi-language Support: Includes support for both English and Tamil.
Error Handling: Provides verbal cues in case of invalid input or errors, ensuring clear feedback.
Technologies Used
Python
Streamlit: For web-based user interface
Google Text-to-Speech (gTTS): To generate spoken feedback
SpeechRecognition: For capturing and interpreting voice commands
OpenAI API: For intent detection and language processing
Deep Translator: For language translation of commands (Tamil to English)
Project Structure
app.py: Main application file containing the code for voice interaction and ATM functionalities.
accounts.json: JSON file to store and retrieve account details such as balance and PIN.
requirements.txt: Contains all required dependencies.
