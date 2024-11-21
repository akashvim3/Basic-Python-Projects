import http.server
import socket
import socketserver
import webbrowser
import pyqrcode
import os
from datetime import datetime
import base64

# Define the default port and working directory (Desktop in OneDrive)
PORT = 8000
desktop = os.path.join(os.environ['USERPROFILE'], 'OneDrive', 'Desktop')  # Desktop is the default location
os.chdir(desktop)

# Authentication setup (simple username/password)
USERNAME = 'admin'
PASSWORD = 'password'

# Function for HTTP Basic Authentication
def check_authentication(self):
    auth_header = self.headers.get('Authorization')
    if not auth_header:
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="Login"')
        self.end_headers()
        self.wfile.write(b'Authentication required.')
        return False

    auth_type, auth_value = auth_header.split(' ', 1)
    if auth_type.lower() != 'basic':
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b'Invalid authentication type.')
        return False

    try:
        user, pwd = base64.b64decode(auth_value).decode().split(':', 1)
    except Exception:
        self.send_response(400)
        self.end_headers()
        self.wfile.write(b'Invalid credentials format.')
        return False

    if user == USERNAME and pwd == PASSWORD:
        return True
    else:
        self.send_response(403)
        self.end_headers()
        self.wfile.write(b'Forbidden: Invalid username or password.')
        return False

# Set up the HTTP server handler with custom responses
class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            if not check_authentication(self):
                return
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            # HTML content with styling and layout improvements
            html_content = """
            <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Local Web Server</title>
                    <link rel="icon" href="/favicon.ico" type="image/x-icon">
                    <style>
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f9;
                            color: #333;
                            margin: 0;
                            padding: 0;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                        }
                        .container {
                            text-align: center;
                            background-color: #fff;
                            border-radius: 10px;
                            padding: 40px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                            width: 80%;
                            max-width: 600px;
                        }
                        h1 {
                            color: #2c3e50;
                        }
                        p {
                            font-size: 18px;
                            color: #7f8c8d;
                        }
                        .qr-code {
                            margin: 30px 0;
                        }
                        a {
                            text-decoration: none;
                            font-size: 18px;
                            color: #2980b9;
                        }
                        a:hover {
                            text-decoration: underline;
                        }
                        .upload-section {
                            margin-top: 40px;
                        }
                        input[type="file"] {
                            padding: 10px;
                            background-color: #2980b9;
                            color: white;
                            border: none;
                            cursor: pointer;
                        }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Welcome to Your Local Web Server!</h1>
                        <p>Access this page by clicking the link below or scan the QR code.</p>
                        <div class="qr-code">
                            <img src="myqr.svg" alt="QR Code">
                        </div>
                        <p><a href="http://{ip}:{port}">Click here to open the server in your browser</a></p>
                        <p>Serving at: <strong>http://{ip}:{port}</strong></p>
                        <p><small>Generated on: {datetime}</small></p>
                        
                        <div class="upload-section">
                            <p>Upload a file:</p>
                            <form action="/" method="POST" enctype="multipart/form-data">
                                <input type="file" name="file" accept="*">
                                <button type="submit">Upload</button>
                            </form>
                        </div>
                    </div>
                </body>
            </html>
            """.format(ip=IP, port=PORT, datetime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

            self.wfile.write(html_content.encode('utf-8'))
        else:
            super().do_GET()  

    def log_message(self, format, *args):
        """Override to log requests to the console with timestamps."""
        log_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{log_time}] {self.client_address} - {format % args}")

    def do_POST(self):
        """Handle file uploads."""
        if not check_authentication(self):
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Here we process the uploaded file, this is just an example
        with open("uploaded_file", "wb") as f:
            f.write(post_data)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'File uploaded successfully!')

# Try to determine the IP address
try:
    hostname = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))  
    IP = s.getsockname()[0]
    s.close()
except OSError:
    IP = "127.0.0.1"  

# Create the full link for the QR code
link = f"http://{IP}:{PORT}"
url = pyqrcode.create(link)

# Generate and save the QR code with improved colors (using 'foreground' instead of 'fill')
url.svg("myqr.svg", scale=8, background="white", foreground="black")

# Open the QR code automatically in the default browser
webbrowser.open('myqr.svg')

# Add a favicon to the server's directory (favicon.ico file must exist)
# You can generate or download a favicon.ico file and place it in the same directory as this script

# Start the server
with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
    print("Serving at port", PORT)
    print("Access the server at this link:", link)
    print("Or use the QR Code to access it on your mobile.")
    httpd.serve_forever()
