# Secure Voice Chat Application using TCP

Voice communication is one of the most popular and effective means of communication. This project aims to develop a secure voice chat application using TCP and Python, allowing users to establish a real-time voice call over a network connection. The application will employ encryption and security measures to ensure the privacy of the communication.

## Features

- User-friendly interface for easy navigation
- Audio capture and playback functionality
- Network communication module for establishing and maintaining connections
- Secure encryption for maintaining the privacy of communication

## Libraries Used

- Socket: for socket programming
- Pyaudio: for conversion of audio to digital data and back
- SSL: utilizes OpenSSL to implement a secure socket layer, including encryption and authentication
- Tkinter: for GUI

## Getting Started

### Prerequisites

To generate SSL certificates for secure communication, you need OpenSSL installed on your system. You can install OpenSSL through your package manager or download it from the official website.

### SSL Certificate Generation

To generate SSL certificates, use the following commands:

```bash
# Generate a private key
openssl genrsa -out private_key.pem 2048

# Generate a certificate signing request (CSR)
openssl req -new -key private_key.pem -out csr.pem

# Self-sign the CSR to generate a self-signed certificate
openssl x509 -req -days 365 -in csr.pem -signkey private_key.pem -out certificate.pem
```
Replace the certificate and key paths in the code with the paths to your generated SSL certificates.

### Installation

To run the application, you'll need to have Python installed. You can clone the repository and execute the files using any Python IDE or terminal.

### Usage

Run the `server.py` file to initiate the server. Once the server is up and running, execute the `client.py` file to establish a connection and start the voice call. You can have multiple instances of client on multiple devices in the same subnet, enter the required addresses in the code. A new window will appear, allowing you to interact with the call functions.

