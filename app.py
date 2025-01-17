from fasthtml.common import *
import pysos
import time
import threading
from hmac import compare_digest
import uuid
from homepage_content import generate_homepage_content

# Initialize persistent storage
sessions_db = pysos.Dict('sessions.db')

# Admin credentials
ADMIN_PASSWORD = "admin"

# Initialize FastHTML app
app = FastHTML(
    hdrs=(
        picolink,
        Style(':root { --pico-font-size: 100%; }')
    )
)

# Login page
@app.route("/login")
def get():
    frm = Form(
        Input(id='name', placeholder='Username'),
        Input(id='pwd', type='password', placeholder='Password'),
        Button('Login'),
        action='/login',
        method='post'
    )
    return Titled("Login", frm)

# Login form data class
@dataclass
class Login:
    name: str
    pwd: str

# Login handler
@app.route("/login")
def post(login: Login, resp):
    if not login.name or not login.pwd:
        return RedirectResponse('/login', status_code=303)
    
    # Check if username is 'admin' and password matches
    if login.name != "admin" or not compare_digest(ADMIN_PASSWORD.encode("utf-8"), login.pwd.encode("utf-8")):
        return RedirectResponse('/login', status_code=303)
    
    # Create session in PySOS
    session_id = str(uuid.uuid4())
    sessions_db['uuid'] = {
        session_id: {
            'username': login.name,
            'login_time': int(time.time())
        }
    }
    
    # Create response with cookie
    response = RedirectResponse('/', status_code=303)
    response.set_cookie(key="session", value=session_id)
    return response

# Check session middleware
def check_session(req):
    session_id = req.cookies.get("session")
    if not session_id:
        return False
        
    stored_sessions = sessions_db.get('uuid', {})
    return session_id in stored_sessions

# Protected content route
@app.route("/")
def get(req):
    # Check if user is authenticated
    if not check_session(req):
        return RedirectResponse('/login', status_code=303)
    
    # Get session data
    session_id = req.cookies.get("session")
    session_data = sessions_db['uuid'][session_id]
    
    # Generate HTML content using the new function
    login_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(session_data['login_time']))
    return generate_homepage_content(session_data['username'], login_time)

# Logout handler
@app.get("/logout")
def logout(req, resp):
    session_id = req.cookies.get("session")
    if session_id:
        stored_sessions = sessions_db.get('uuid', {})
        if session_id in stored_sessions:
            del stored_sessions[session_id]
            sessions_db['uuid'] = stored_sessions
    
    response = RedirectResponse('/login', status_code=303)
    response.delete_cookie("session")
    return response

def session_status_checker():
    while True:
        print("=== Session Status Check ===")
        sessions = sessions_db.get('uuid', {})
        current_time = int(time.time())
        for session_id, data in list(sessions.items()):  # Use list() to avoid runtime errors when modifying the dict
            username = data['username']
            login_time = data['login_time']
            elapsed_time = current_time - login_time
            print(f"User {username} on session {session_id} has logged in for {elapsed_time} seconds")
            
            # Check if the session should be deleted
            if login_time + 60 <= current_time:
                print(f"Session {session_id} for user {username} has expired. Deleting...")
                del sessions[session_id]
                sessions_db['uuid'] = sessions  # Update the database
        
        time.sleep(10)

# Start the background task
background_thread = threading.Thread(target=session_status_checker, daemon=True)
background_thread.start()

if __name__ == "__main__":
    serve()
