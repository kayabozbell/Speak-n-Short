import tkinter as tk
import speech_recognition as sr
import subprocess
import pyautogui
import datetime
import threading

def show_commands():
    commands_text = """
    Sistemi aktif duruma getirmek için lütfen "aktif" diyiniz.
    Komutlar                                     Fonksiyonlar
    - Ses arttır               ===                 "arttır."
    - Ses azalt                ===                 "azalt."
    - Sesi kapat               ===                 "sessiz."
    - Ekran görüntüsü al       ===                 "ekran."
    - Tarayıcıyı aç            ===                 "aç."
    - Tarayıcıyı kapat         ===                 "kapat."
    - Sonraki parçayı çal      ===                 "sonraki."
    - Önceki parçayı çal       ===                 "önceki."
    - Medyayı oynat            ===                 "oynat."
    - Medyayı durdur           ===                 "dur."
    - Uygulamayı kapat         ===                 "bitir."
    """
    commands_label.config(text=commands_text)

def volume_boost():
    i = 0
    while i < 10:
        pyautogui.press("volumeup")
        i += 1


def volume_reduce():
    i = 0
    while i<10:
        pyautogui.press("volumedown") 
        i+=1

def mute_sound():
    pyautogui.press("volumemute")
    
def screenshot():
    # Şu anki zamanı kullanarak farklı bir dosya adı oluştur
    anlik_zaman = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dosya_adi = f"ekran_goruntusu_{anlik_zaman}.png"

    # Ekran görüntüsünü al ve yeni dosya adıyla kaydet
    screenshot = pyautogui.screenshot()
    screenshot.save(dosya_adi)

    print(f"{dosya_adi} adıyla ekran görüntüsü alındı.")

def open_browser():
    url = 'https://www.google.com.tr'
    subprocess.Popen(['start', url], shell=True)
    
def close_browser():
    subprocess.run(['taskkill', '/F', '/IM', 'opera.exe'], shell=True)

def play_media():
    pyautogui.press("playpause")

def stop_media():
    pyautogui.press("playpause")

def media_next_track():
    pyautogui.press("nexttrack")

def media_previous_track():
    pyautogui.press("prevtrack")
# Diğer fonksiyonlar da burada olacak

def listen_for_commands(r, mic):
    global is_active
    while True:
        with mic as source:
            print("Sesiniz algılanıyor, lütfen konuşun...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

        try:
            command = r.recognize_google(audio, language="tr-TR")  # Türkçe tanıma
            print("Anlaşılan komut: " + command)

            if "aktif" in command.lower():
                print("Etkinleştirme kelimesi algılandı. Komutları dinlemeye başla...")
                is_active = True
                show_commands()

            if is_active:
                if "arttır" in command.lower():
                    volume_boost()

                if "azalt" in command:
                    volume_reduce()

                if "sessiz" in command:
                    mute_sound()
                
                if "ekran" in command:
                    screenshot()
                
                if "aç" in command:
                    open_browser()

                if "kapat" in command:
                    close_browser()

                if "sonraki" in command:
                    media_next_track()

                if "önceki" in command:
                    media_previous_track()

                if "bitir" in command:
                    exit()
                
                if "oynat" in command:
                    play_media()
                
                if "dur" in command:
                    stop_media()

        except sr.UnknownValueError:
            print("Komut anlaşılamadı.")
        except sr.RequestError:
            print("Ses hizmeti çalışmıyor, lütfen daha sonra tekrar deneyin.")

def start_listening():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # Arka planda dinlemek için yeni bir thread başlat
    listening_thread = threading.Thread(target=listen_for_commands, args=(recognizer, microphone))
    listening_thread.daemon = True  # Arka plandaki işlemi program kapatılırken sonlandır
    listening_thread.start()

def main():
    global is_active
    is_active = False

    # Tkinter penceresini oluşturma
    root = tk.Tk()
    root.title("Komut Listesi")

    global commands_label
    commands_label = tk.Label(root, text="", justify="left")
    commands_label.pack()

    show_commands()  # Komutları görüntüle

    # Dinleme işlevini başlatma
    start_listening()

    root.mainloop()

if __name__ == "__main__":
    main()
