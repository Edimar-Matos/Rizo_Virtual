import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
from bs4 import BeautifulSoup

# Inicialize os motores de reconhecimento de fala e texto para fala
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language="pt-BR")
        print("Você disse: " + command)
        return command
    except sr.UnknownValueError:
        print("Desculpe, não entendi.")
        return ""
    except sr.RequestError as e:
        print("Não foi possível fazer a solicitação; {0}".format(e))
        return ""

def open_web_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")

        if paragraphs:
            for paragraph in paragraphs[:3]:  # Lê os primeiros três parágrafos
                speak(paragraph.get_text())
        else:
            speak("Não encontrei informações na página.")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página da web: {e}")
        speak("Desculpe, ocorreu um erro ao acessar a página da web.")

def main():
    speak("Olá! Eu sou a Rizo. Como posso ajudar você?")
    
    while True:
        command = listen().lower()
        
        if "google" in command:
            speak("Que informações você deseja encontrar na web?")
            search_query = listen()
            print(f"Procurando informações na web: {search_query}")
            
            search_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
            open_web_page(search_url)

        elif "vídeo" in command:
            speak("Qual video você quer ver ?")
            search_query = listen()
            print(f"Procurar assunto: {search_query}")
            
            # Perform a web search using a search engine like Google
            search_url = f"https://www.youtube.com/results?search_query={search_query}"
            webbrowser.open(search_url)  

        

        elif "procurar" in command:
            speak("O que você quer procurar?")
            search_query = listen()
            print(f"Procurar assunto: {search_query}")
            
            # Perform a web search using a search engine like Google
            search_url = f"https://pt.wikipedia.org/wiki/{search_query}"
            webbrowser.open(search_url)

            def ler_texto_da_web(search_query):
                try:
                    # Faz uma solicitação HTTP para o URL
                    response = requests.get(search_query)

                    # Verifica se a solicitação foi bem-sucedida
                    if response.status_code == 200:
                        # Analisa o HTML da página
                        soup = BeautifulSoup(response.text, 'html.parser')

                        # Extrai o texto da página
                        texto = soup.get_text()
                        return texto
                    else:
                        print("Erro: Não foi possível obter o conteúdo da página.")
                        return None
                except Exception as e:
                    print(f"Erro: {e}")
                    return None

            # Exemplo de uso
            search_query = f"https://www.google.com/search?q={search_query}"
            search_query = ler_texto_da_web(search_query)
            if search_query:
                speak(search_query)

            elif "encerrar" in command:
                speak("Até a próxima!")
                break
           
              
        
        elif "encerrar" in command:
            speak("Até a próxima!")
            break

if __name__ == "__main__":
    main()
