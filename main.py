import os
import re
import signal
import subprocess
import webview

EXECUTE_DIR = os.path.dirname(os.path.abspath(__file__))
msgbox = lambda msg: webview.windows[0].evaluate_js("alert('{}')".format(msg.replace("'","\\'")))

class Api():
    def __init__(self):
        self.phantom_proc = None
    
    def __set_btn_state(self, starting_server):
        if starting_server:
            webview.windows[0].evaluate_js("document.getElementById('btn-start').disabled=true")
            if self.phantom_proc is None:
                webview.windows[0].evaluate_js("document.getElementById('btn-start').innerText='Starting...'")
            else:
                webview.windows[0].evaluate_js("document.getElementById('btn-start').innerText='Stopping...'")
        else:
            webview.windows[0].evaluate_js("document.getElementById('btn-start').disabled=false")
            if self.phantom_proc is None:
                webview.windows[0].evaluate_js("document.getElementById('btn-start').classList.remove('activated')")
                webview.windows[0].evaluate_js("document.getElementById('btn-start').innerText='Start Phantom Proxy'")
            else:
                webview.windows[0].evaluate_js("document.getElementById('btn-start').classList.add('activated')")
                webview.windows[0].evaluate_js("document.getElementById('btn-start').innerText='Stop Phantom Proxy'")
        self.__set_fields_state()
    
    def __set_fields_state(self):
        if self.phantom_proc is None:
            webview.windows[0].evaluate_js("document.forms[0]['server-url'].disabled=false")
            webview.windows[0].evaluate_js("document.forms[0]['port-number'].disabled=false")
        else:
            webview.windows[0].evaluate_js("document.forms[0]['server-url'].disabled=true")
            webview.windows[0].evaluate_js("document.forms[0]['port-number'].disabled=true")
    
    def __save_fields(self, server_url, server_port):
        server_txt = os.path.join(EXECUTE_DIR, "lastserver.txt")
        with open(server_txt, "w") as f:
            f.write(server_url)
            f.write("\n")
            f.write(server_port)
    
    def __get_phantom_path(self):
        # Detect the Phantom executable. Returns a tuple of (bool, string),
        # where the first part is whether the executable was detected or not,
        # and the second part is the path if detected, error message if not.

        phantom_dir = os.path.join(EXECUTE_DIR, "bin")
        if not os.path.exists(phantom_dir):
            return (False, 'You need to create a folder named "bin" in the same path as the GUI executable, then place the Phantom executable in it.')
        phantom_exes = [f for f in os.listdir(phantom_dir) if f.startswith("phantom")]
        if len(phantom_exes) == 0:
            return (False, 'You need to place a Phantom executable in the "bin" folder.')
        elif len(phantom_exes) > 1:
            return (False, 'You can only place one Phantom executable in the "bin" folder. Please remove the others in this folder.')
        phantom_exe = os.path.join(phantom_dir, phantom_exes[0])

        return (True, phantom_exe)
    
    def initialize(self):
        # Read from server text file if it exists, and if not create it.
        # Populate with default values if file doesn't exist or if file data invalid.

        # Check if Phantom executable found. If not, inform that it wasn't found
        phantom_detected, _ = self.__get_phantom_path()
        if not phantom_detected:
            webview.windows[0].evaluate_js("document.getElementById('dl-link').style.display='block'")

        server_txt = os.path.join(EXECUTE_DIR, "lastserver.txt")
        if not os.path.exists(server_txt):
            f = open(server_txt, "w")
            f.close()
            return

        with open(server_txt) as f:
            server_info = f.readlines()
        server_url = server_info[0].strip() if len(server_info) > 0 else ""
        server_port = server_info[1].strip() if len(server_info) > 1 else "19132"
        if len(server_port) == 0 or not server_port.isnumeric():
            server_port = "19132"

        webview.windows[0].evaluate_js("document.forms[0]['server-url'].value='{}'".format(server_url.replace("'","\\'")))
        webview.windows[0].evaluate_js("document.forms[0]['port-number'].value='{}'".format(server_port))

    def runPhantom(self, server_url, server_port):
        # Disable start/stop button while starting up server
        self.__set_btn_state(starting_server=True)

        # Validate form input
        form_valid = bool(re.match(r"^(?:[a-z0-9]+\.)*[a-z0-9]+\.[a-z0-9]+$", server_url, re.IGNORECASE)) and server_port.isnumeric()
        if not form_valid:
            msgbox("You need a server URL and port number. If you're unsure of the port, use the default Bedrock server port 19132.")
            self.__set_btn_state(starting_server=False)
            return

        # Get phantom executable path
        phantom_detected, phantom_exe = self.__get_phantom_path()
        if not phantom_detected:
            msgbox(phantom_exe)
            self.__set_btn_state(starting_server=False)
            return

        # Run phantom executable with provided server URL/port
        full_server_url = "{}:{}".format(server_url, server_port)
        try:
            self.phantom_proc = subprocess.Popen([
                phantom_exe, "-server", full_server_url
            ])
            self.__save_fields(server_url, server_port)
        except OSError:
            msgbox('Permissions error. Make sure that Phantom executable is able to be executed by running "chmod +x {}" in a terminal, if on macOS/Linux.'.format(phantom_exe))
            self.phantom_proc = None

        self.__set_btn_state(starting_server=False)
    
    def stopPhantom(self, program_closed=False):
        if not program_closed:
            self.__set_btn_state(starting_server=True)
        if self.phantom_proc is not None:
            self.phantom_proc.terminate()
            self.phantom_proc.wait()
            self.phantom_proc = None
        if not program_closed:
            self.__set_btn_state(starting_server=False)

api = Api()

if __name__ == "__main__":
    window = webview.create_window("Phantom Proxy GUI",
        os.path.join("html", "index.html"),
        background_color="#000000",
        width=450, height=250,
        js_api = api,
        resizable=False
    )
    window.closed += lambda: api.stopPhantom(True)
    webview.start(debug=True)