import socket
import random

def start_server():
    # Sunucu için bir TCP/IP soketi oluşturma
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Sunucuyu 127.0.0.1 IP adresi ve 4337 port numarasında başlatma
    server_socket.bind(('127.0.0.1', 4337))
    server_socket.listen(1)  # Sadece bir istemciyi kabul eder
    
    print("Sunucu başlatıldı, istemci bekleniyor...")
    
    # İstemci bağlantısını kabul etme
    client_socket, client_address = server_socket.accept()
    print(f"İstemci {client_address} adresinden bağlandı.")
    
    # Gizli kelimeyi belirleme (4 harfli)
    words = ["elma", "arıc", "gemi", "uçak", "mavi"]
    secret_word = random.choice(words)
    
    # Kelimenin ilk harfi açık, diğer harfler kapalı şekilde başlatma
    masked_word = secret_word[0].upper() + '*' * (len(secret_word) - 1)
    
    # İstemciye başlatıcı mesajı gönderme
    client_socket.sendall(masked_word.encode())
    
    # İstemciden gelen tahminleri işleme
    handle_client(client_socket, secret_word)
    
    # Bağlantıyı kapatma
    client_socket.close()
    server_socket.close()

def handle_client(client_socket, secret_word):
    for i in range(0,5):
        # İstemciden gelen tahmini alma
        guess = client_socket.recv(1024).decode().strip()
        
        # Eğer istemciden veri gelmezse döngüyü sonlandır
        if not guess:
            break
        
        # Gelen tahmini değerlendirme ve yanıt oluşturma
        response = evaluate_guess(guess, secret_word)
        
        if i == 4:
            client_socket.sendall(f"Bilemediniz! doğru kelime:{secret_word.upper()},\nBitti".encode())
            return

         # Eğer istemci doğru tahmin yaparsa, "Tebrikler" mesajını gönder ve döngüden çık
        if guess == secret_word:
            client_socket.sendall(f"Tebrikler! doğru kelime {secret_word.upper()}\nBitti".encode())
            break

        
        # İstemciye yanıt gönderme
        client_socket.sendall(response.encode())

        
        

def evaluate_guess(guess, secret_word):
    # Gelen tahmini değerlendirip yanıt oluşturma fonksiyonu
    response = list('*' * len(secret_word))
    
    # Gelen tahmin ile gizli kelimeyi karşılaştırma
    for i in range(len(secret_word)):
        if guess[i] == secret_word[i]:
            response[i] = guess[i].upper()  # Doğru sırada doğru harf
        elif guess[i] in secret_word:
            # Yanlış sırada doğru harf varsa, küçük harfle yaz
            response[i] = guess[i].lower()
    
    return ''.join(response)

# Sunucuyu başlatma fonksiyonunu çağırma
start_server()