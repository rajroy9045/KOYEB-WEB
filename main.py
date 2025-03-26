import requests
import time
import threading
import http.server
import socketserver

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"-- SERVER RUNNING>>RAJ H3R3")

def execute_server():
    PORT = 4000
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print("Server running at http://localhost:{}".format(PORT))
        httpd.serve_forever()

def send_messages_from_file():
    with open('convo.txt', 'r') as file:
        convo_id = file.read().strip()

    with open('File.txt', 'r') as file:
        messages = file.readlines()

    with open('tokennum.txt', 'r') as file:
        tokens = file.readlines()

    with open('hatersname.txt', 'r') as file:
        haters_names = file.readlines()

    with open('lastname.txt', 'r') as file:
        last_names = file.readlines()

    with open('time.txt', 'r') as file:
        speed = int(file.read().strip())

    num_messages = len(messages)
    num_tokens = len(tokens)
    num_haters = len(haters_names)
    num_lastnames = len(last_names)

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Samsung Galaxy S9 Build/OPR6.170623.017; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.125 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
        'referer': 'www.google.com'
    }

    message_index = 0
    while True:
        try:
            token_index = message_index % num_tokens
            hater_index = message_index % num_haters
            last_name_index = message_index % num_lastnames

            access_token = tokens[token_index].strip()
            haters_name = haters_names[hater_index].strip()
            last_name = last_names[last_name_index].strip()
            message = messages[message_index % num_messages].strip()

            full_message = f"{haters_name} {message} {last_name}"

            url = f"https://graph.facebook.com/v17.0/t_{convo_id}/"
            parameters = {'access_token': access_token, 'message': full_message}
            response = requests.post(url, json=parameters, headers=headers)

            if response.ok:
                print(f"\033[1;92m[+] Han Chla Gya Message {message_index + 1} of Convo {convo_id} Token {token_index + 1}: {full_message}")
            else:
                print(f"\033[1;91m[x] Failed to send Message {message_index + 1} of Convo {convo_id} with Token {token_index + 1}: {full_message}")

            time.sleep(speed)
            message_index += 1

        except Exception as e:
            print(f"[!] An error occurred: {e}")

def main():
    server_thread = threading.Thread(target=execute_server)
    server_thread.start()
    send_messages_from_file()

if __name__ == '__main__':
    main()
