import socket

def reflect_attack(attack_data, sender_address):
    # Code to reflect the attack data back to the sender.
    try:
        # Create a socket to send the attack data back to the sender.
        reflect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        reflect_socket.connect(sender_address)
        
        # Send the attack data back to the sender.
        reflect_socket.sendall(attack_data)
        
        # Close the reflect socket.
        reflect_socket.close()
        
        print("Attack reflected successfully!")
    except Exception as e:
        print(f"Error while reflecting attack: {str(e)}")

def detect_and_reflect_attacks():
    # Code to listen for incoming attacks and reflect them back to the sender.
    reflect_port = 1234

    reflect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    reflect_socket.bind(('0.0.0.0', reflect_port))
    reflect_socket.listen(1)

    print("Mirror is ready to detect and reflect attacks.")

    while True:
        try:
            attacker_socket, attacker_address = reflect_socket.accept()
            
            print(f"Incoming attack from: {attacker_address}")
            
            # Receive the attack data.
            attack_data = attacker_socket.recv(2048)
            
            # Reflect the attack data back to the sender.
            reflect_attack(attack_data, attacker_address)
            
            # Close the attacker socket.
            attacker_socket.close()
            
        except KeyboardInterrupt:
            # Exit gracefully if the script is interrupted.
            break
        except Exception as e:
            print(f"Error while detecting and reflecting attacks: {str(e)}")

    # Close the reflect socket.
    reflect_socket.close()

# Start detecting and reflecting attacks.
detect_and_reflect_attacks()
