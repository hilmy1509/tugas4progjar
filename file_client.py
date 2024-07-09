import socket
import json
import base64
import logging

server_address = ('127.0.0.1', 7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)  # timeout 10 detik
    try:
        sock.connect(server_address)
        logging.warning(f"connecting to {server_address}")
        try:
            logging.warning(f"sending message ")
            sock.sendall(command_str.encode())
            # Look for the response, waiting until socket is done (no more data)
            data_received = ""  # empty string
            while True:
                # socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
                data = sock.recv(16)
                if data:
                    # data is not empty, concat with previous content
                    data_received += data.decode()
                    if "\r\n\r\n" in data_received:
                        break
                else:
                    # no more data, stop the process by break
                    break
            # at this point, data_received (string) will contain all data coming from the socket
            # to be able to use the data_received as a dict, need to load it using json.loads()
            hasil = json.loads(data_received)
            logging.warning("data received from server:")
            return hasil
        except Exception as e:
            logging.warning(f"error during data receiving: {e}")
            return False
    except socket.timeout:
        logging.warning("Koneksi ke server timeout")
        return False
    except Exception as e:
        logging.warning(f"Error: {e}")
        return False
    finally:
        sock.close()

def remote_list():
    command_str = f"LIST"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        # proses file dalam bentuk base64 ke bentuk bytes
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        fp = open(namafile, 'wb+')
        fp.write(isifile)
        fp.close()
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename=""):
    try:
        with open(filename, 'rb') as f:
            file_content = base64.b64encode(f.read()).decode()
        command_str = f"UPLOAD {filename} {file_content}"
        hasil = send_command(command_str)
        if hasil and hasil['status'] == 'OK':
            print(hasil['data'])
            return True
        else:
            print("Gagal")
            return False
    except FileNotFoundError:
        print(f"File {filename} tidak ditemukan")
        return False

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil and hasil['status'] == 'OK':
        print(hasil['data'])
        return True
    else:
        print("Gagal")
        return False

if __name__ == '__main__':
    server_address = ('127.0.0.1', 7778)
    remote_list()
    remote_get('donalbebek.jpg')
    remote_upload('protokol.txt')
    remote_delete('protokol.txt')
    remote_upload('try3.txt')
    remote_delete('try3.txt')