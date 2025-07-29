from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory, session
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "supersecret"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

pdfs = {}
email = []
employees = []
employee_logs = {}
employee_details = {}
employee_leaves = {}

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Fotoplane HR Portal</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    <style>
    html, body {
        height: 100%;
        margin: 0;
        font-family: Arial, sans-serif;
    }
    .golden-heading {
        background: linear-gradient(to right, #b8860b, #ffcc00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparen
        
        
        t;
        font-weight: bold;
    }
    body {
        background-color: #FFFAF0; /* Light blue */
        background-image: url('https://fotoplane.com/wp-content/uploads/2023/06/fp-logo-tm-1.png');
        background-repeat: no-repeat;
        background-position: right center;
        background-attachment: fixed;
        background-size: 70%;
    }
    .overlay {
        background-color: rgba(255, 255, 255, 0.8); /* 50% transparent white */
        min-height: 100vh;
        padding: 20px;
        width: 100%;
    }
    .sidebar {
        background: #00264d;
        color: white;
        min-height: 100vh;
        padding: 20px;
    }
    .sidebar a {
        color: white;
        text-decoration: none;
        display: block;
        margin: 10px 0;
    }
    .sidebar a:hover {
        text-decoration: underline;
    }
    .logo {
        width: 180px;
        margin-bottom: 30px;
    }
    .admin-tag {
        background: #ffc107;
        color: #000;
        font-weight: bold;
        padding: 5px 10px;
        border-radius: 10px;
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }
    th, td {
        padding: 10px;
        border: 1px solid #ccc;
    }
</style>

    <script>
        function showLeaveType(select) {
            const leaveType = document.getElementById("leave-type");
            leaveType.style.display = select.value === 'leave' ? 'block' : 'none';
        }
    </script>
</head>
<body>
<div class="d-flex">
    <div class="sidebar">
        <img src="https://fotoplane.com/wp-content/uploads/2023/06/fp-logo-tm-1.png" class="logo">
        <h5>HR Resource Hub</h5>
        {% if session.get('admin') %}
        <div class="admin-tag">Admin Access</div>
        {% endif %}
        <a href="{{ url_for('home') }}">🏠 Home</a>
        <a href="{{ url_for('leave') }}">📄 HR Policies</a>
        <a href="{{ url_for('employee') }}">👥 Employees</a>
        <a href="{{ url_for('employee_login') }}">🔐 Employee Login</a>
        
        {% if session.get('admin') %}
        <a href="{{ url_for('employees_data') }}">📋 Total Employees</a>
        {% endif %}
        
        {% if session.get('admin') or session.get('employee_name') %}
        <a href="{{ url_for('logout') }}">🚪 Logout</a>
        {% else %}
        <a href="{{ url_for('login') }}">🔑 Admin Login</a>
        {% endif %}
    </div>
    <div class="flex-fill overlay">
        {{ content|safe }}
    </div>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    content = """
    <h2 class="golden-heading">Welcome to FOTOPLANE SOCIAL HR Portal</h2><hr>
    <h4>Company Website</h4>
    <div style="height: 80vh;">
        <iframe src="https://fotoplane.com/" style="width:100%; height:100%; border:none;"></iframe>
    </div>
    """
    return render_template_string(TEMPLATE, content=content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['password'] == 'admin123':
        session['admin'] = True
        return redirect(url_for('home'))
    return render_template_string(TEMPLATE, content="""
    <div <div class='text-center mt-4'>
        <h2>Admin Login</h2>
        <form method="post">
            <input type="password" name="password" class="form-control w-100" placeholder="Enter Admin Password"><br>
            <button type='lOGIN' class='btn btn-primary'>Login</button>
        </form>
    </div>
    """)

@app.route('/employees-data', methods=['GET', 'POST'])
def employees_data():
    if not session.get('admin'):
        return render_template_string(
            TEMPLATE, 
            content="""
                <div class='alert alert-warning text-center mt-4'>
                    <h4 class='text-danger'>🔒 Access Denied</h4>
                    <p>This section is reserved for administrators only.</p>
                </div>
            """
        )

    msg = ""

    # Handle new employee addition
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        emp_id = request.form.get('emp_id', '').strip()
        email = request.form.get('email', '').strip()
        dob = request.form.get('dob', '').strip()

        if full_name and emp_id and email and dob:
            if emp_id in employee_details:
                msg = "<div class='alert alert-warning'>⚠️ Employee ID already exists.</div>"
            else:
                employee_details[emp_id] = {
                    'name': full_name,
                    'email': email,
                    'dob': dob
                }
                msg = "<div class='alert alert-success'>✅ Employee added successfully!</div>"
        else:
            msg = "<div class='alert alert-danger'>⚠️ Please fill in all fields.</div>"

    # Generate employee table
    table_rows = ""
    for emp_id, data in employee_details.items():
        table_rows += f"""
            <tr>
                <td>{data['name']}</td>
                <td>{emp_id}</td>
                <td>{data['email']}</td>
                <td>{data['dob']}</td>
            </tr>
        """

    content = f"""
    <h2 class="golden-heading mb-3">📋 Registered Employees</h2>
    {msg}
    <form method="POST" class="mb-4">
        <input name="full_name" placeholder="Full Name" class="form-control mb-2" required>
        <input name="emp_id" placeholder="Employee ID" class="form-control mb-2" required>
        <input name="email" placeholder="Email Address" class="form-control mb-2" required>
        <input type="date" name="dob" class="form-control mb-2" required>
        <button class="btn btn-success">➕ Add Employee</button>
    </form>
    <hr>
    <table class="table table-bordered table-striped mt-4">
        <thead class="table-dark">
            <tr>
                <th>Full Name</th>
                <th>Employee ID</th>
                <th>Email</th>
                <th>Date of Birth</th>
            </tr>
        </thead>
        <tbody>{table_rows}</tbody>
    </table>
    """

    return render_template_string(TEMPLATE, content=content)

@app.route('/employee-summary')
def employee_summary():
    emp_email = session.get('employee_email')
    data = employee_leave_data.get(emp_email)

    if data:
        total = data['total']
        availed = data['availed']
        left = max(0, total - availed)
    else:
        total = availed = left = 0

    return render_template_string(
        TEMPLATE,
        content=f"""
        <div class="text-center mt-4">
            <h4>📋 Leave Summary</h4>
            <p><strong>Total Leave:</strong> {total}</p>
            <p><strong>Leave Availed:</strong> {availed}</p>
            <p><strong>Leave Left:</strong> {left}</p>
        </div>
        """
    )

@app.route('/employee-login', methods=['GET', 'POST'])
def employee_login():
    if request.method == 'POST':
        emp_id = request.form['emp_id'].strip()
        email = request.form['email'].strip().lower()

        # Validate against registered employee data
        emp_data = employee_details.get(emp_id)
        if emp_data and emp_data.get('email', '').lower() == email:
            session['employee_name'] = emp_data['name']
            return redirect(url_for('employee_view'))
        else:
            # POST failed: show error message
            return render_template_string(
                TEMPLATE,
                content="""
                <div class='alert alert-danger text-center mt-4'>
                    <h4>❌ Login Failed</h4>
                    <p>Employee ID or Email not found. Please contact the admin.</p>
                    <p>Email: aastha@fotoplane.com</p>
                </div>
                """
            )

    # GET request: show login form
    return render_template_string(
        TEMPLATE,
        content="""
        <div class='text-center mt-4'>
            <h4>👤 Employee Login</h4>
            <form method='POST'>
                <input type='text' name='emp_id' placeholder='Enter Employee ID' class='form-control my-2' required>
                <input type='email' name='email' placeholder='Enter Registered Email' class='form-control my-2' required>
                <button type='submit' class='btn btn-primary'>Login</button>
            </form>
        </div>
        """
    )


@app.route('/employee-view')
def employee_view():
    emp_name = session.get('employee_name')
    if not emp_name:
        return redirect(url_for('employee_login'))

    emp_id = None
    # Match exact employee ID from employee_details (case-insensitive match)
    for eid, data in employee_details.items():
        if data['name'].lower() == emp_name.lower():
            emp_id = eid
            break

    if not emp_id:
        return render_template_string(TEMPLATE, content="<h4 class='text-danger'>Employee not found.</h4>")

    logs = employee_logs.get(emp_id, {})
    leave_quota = employee_leave_data.get(emp_id, {}).get('total', 24)
    leave_availed = sum(1 for log in logs.values() if log['status'].lower().startswith('leave'))
    leave_left = max(0, leave_quota - leave_availed)

    # Build work log table
    content = f"<h2>👋 Welcome, {emp_name.title()}</h2><h4 class='mt-4'>🗓️ Your Work Logs</h4>"
    content += "<table class='table table-bordered'><thead><tr><th>Date</th><th>Hours</th><th>Status</th></tr></thead><tbody>"
    for date, log in sorted(logs.items()):
        content += f"<tr><td>{date}</td><td>{log.get('hours')}</td><td>{log.get('status').upper()}</td></tr>"
    content += "</tbody></table>"

    # Leave Summary
    content += f"""
    <hr><h4>🧾 Leave Summary</h4>
    <table class='table table-striped table-bordered'>
        <tr><th>Total Leave</th><th>Leave Availed</th><th>Leave Left</th></tr>
        <tr><td>{leave_quota}</td><td>{leave_availed}</td><td>{leave_left}</td></tr>
    </table>
    """

    return render_template_string(TEMPLATE, content=content)


@app.route('/employee', methods=['GET', 'POST'])
def employee():
    if not session.get('admin'):
        return render_template_string(
            TEMPLATE,
            content="""
            <div class='alert alert-warning text-center mt-4'>
                <h4 class='text-danger'>🔒 Oops! You don’t have access to this page.</h4>
                <p class='text-muted'>This section is reserved for admin users only.</p>
            </div>
            """
        )

    global employee_logs, employee_details, employee_leave_data

    if 'employee_leave_data' not in globals():
        employee_leave_data = {}

    msg = ""

    if request.method == "POST":
        # Admin updating total leave quota
        if 'update_emp_id' in request.form and 'update_total' in request.form:
            emp_id = request.form['update_emp_id']
            try:
                total = int(request.form['update_total'])
                if emp_id in employee_leave_data:
                    employee_leave_data[emp_id]['total'] = total
                else:
                    employee_leave_data[emp_id] = {'total': total}
                msg = f"<p class='text-success'>Leave quota updated for {employee_details[emp_id]['name']}.</p>"
            except:
                msg = "<p class='text-danger'>Invalid total leave input.</p>"

        # Add new log
        elif 'emp' in request.form and 'date' in request.form:
            emp = request.form['emp'].strip()
            date = request.form['date']
            status = request.form.get('status', 'wfo')
            leave_detail = request.form.get('leave_detail', '')
            hours = "0:00"

            if status == 'leave' and leave_detail:
                status += f" ({leave_detail})"
            else:
                try:
                    login_time = request.form['login']
                    logout_time = request.form['logout']
                    login_dt = datetime.strptime(login_time, "%H:%M")
                    logout_dt = datetime.strptime(logout_time, "%H:%M")
                    hours = str(logout_dt - login_dt)
                except:
                    hours = "0:00"

            if emp in employee_logs and date in employee_logs[emp]:
                msg = "<p class='text-danger'>Error: Entry already exists for this date!</p>"
            else:
                employee_logs.setdefault(emp, {})[date] = {'hours': hours, 'status': status}

        # Update log
        elif 'edit_emp' in request.form and 'edit_date' in request.form:
            emp = request.form['edit_emp'].strip()
            date = request.form['edit_date']
            hours = request.form['edit_hours']
            status = request.form['edit_status']

            if emp in employee_logs and date in employee_logs[emp]:
                employee_logs[emp][date] = {'hours': hours, 'status': status}

        # Delete log
        elif 'delete_emp' in request.form and 'delete_date' in request.form:
            emp = request.form['delete_emp'].strip()
            date = request.form['delete_date']
            if emp in employee_logs and date in employee_logs[emp]:
                del employee_logs[emp][date]
                if not employee_logs[emp]:
                    del employee_logs[emp]

    # Employee dropdown
    options = "".join([
        f"<option value='{emp_id}'>{data['name']}</option>"
        for emp_id, data in employee_details.items()
    ])

    # Log Entry Form
    content = f"""
    <h2>🕒 Log Work Time (Admin Only)</h2>
    {msg}
    <form method='post'>
        <label>Employee:</label>
        <select name='emp' class='form-control w-50'>{options}</select><br>
        <label>Date:</label>
        <input type='date' name='date' class='form-control w-50' required><br>
        <label>Login Time:</label>
        <input type='time' name='login' class='form-control w-50'><br>
        <label>Logout Time:</label>
        <input type='time' name='logout' class='form-control w-50'><br>
        <label>Status:</label>
        <select name='status' class='form-control w-50' onchange="document.getElementById('leave-type').style.display = this.value === 'leave' ? 'block' : 'none';">
            <option value='wfo'>WFO</option>
            <option value='wfh'>WFH</option>
            <option value='leave'>Leave</option>
        </select><br>
        <div id="leave-type" style="display:none;">
            <label>Leave Type:</label>
            <select name="leave_detail" class="form-control w-50">
                <option value="casual">Casual Leave</option>
                <option value="sick">Sick Leave</option>
            </select>
        </div><br>
        <button class='btn btn-success'>Submit Log</button>
    </form>
    """

    # Work Logs Table
    content += """
    <hr><h4>📅 All Work Logs</h4>
    <table class='table table-bordered'>
        <thead class='table-dark'>
        <tr><th>Employee</th><th>Date</th><th>Hours</th><th>Status</th><th>Update</th><th>Delete</th></tr>
        </thead>
    """
    for emp_id, logs in employee_logs.items():
        for date, log in logs.items():
            content += f"""
            <tr>
                <form method='post'>
                    <td>{employee_details.get(emp_id, {}).get('name', emp_id)}<input type='hidden' name='edit_emp' value='{emp_id}'></td>
                    <td>{date}<input type='hidden' name='edit_date' value='{date}'></td>
                    <td><input name='edit_hours' value='{log['hours']}' class='form-control'></td>
                    <td><input name='edit_status' value='{log['status']}' class='form-control'></td>
                    <td><button class='btn btn-sm btn-warning'>Update</button></td>
                </form>
                <form method='post' style='display:inline;'>
                    <input type='hidden' name='delete_emp' value='{emp_id}'>
                    <input type='hidden' name='delete_date' value='{date}'>
                    <td><button class='btn btn-sm btn-danger'>Delete</button></td>
                </form>
            </tr>
            """

    content += "</table>"

    # Leave Summary Table
    content += """
    <hr><h4>🧾 Leave Summary</h4>
    <table class='table table-striped table-bordered'>
        <thead class='table-dark'>
        <tr><th>Employee</th><th>Total Leave</th><th>Availed</th><th>Left</th><th>Action</th></tr>
        </thead><tbody>
    """
    for emp_id, data in employee_details.items():
        name = data['name']
        logs = employee_logs.get(emp_id, {})
        availed = sum(1 for l in logs.values() if l['status'].lower().startswith('leave'))
        total = employee_leave_data.get(emp_id, {}).get('total', 24)
        left = max(0, total - availed)
        content += f"""
        <tr>
            <form method='post'>
                <td>{name}</td>
                <td><input name='update_total' value='{total}' class='form-control' type='number'></td>
                <td>{availed}</td>
                <td>{left}</td>
                <td>
                    <input type='hidden' name='update_emp_id' value='{emp_id}'>
                    <button class='btn btn-sm btn-primary'>Update</button>
                </td>
            </form>
        </tr>
        """

    content += "</tbody></table>"

    return render_template_string(TEMPLATE, content=content)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/leave', methods=['GET', 'POST'])
def leave():
    if request.method == "POST" and session.get('admin'):
        # Uploading new PDF
        if 'heading' in request.form and 'file' in request.files:
            heading = request.form['heading']
            file = request.files['file']
            if file and heading:
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                uploaded_time = datetime.now().isoformat()
                pdfs.setdefault(heading, []).append({'name': filename, 'uploaded': uploaded_time})

        # Updating heading
        elif 'old_heading' in request.form and 'new_heading' in request.form:
            old = request.form['old_heading']
            new = request.form['new_heading']
            if old in pdfs and new:
                pdfs[new] = pdfs.pop(old)

    # Build UI
    content = "<h2 class='golden-heading mb-4'>📄 HR Policy Documents</h2>"

    for heading, files in pdfs.items():
        content += f"""
        <div class='card mb-3 shadow-sm'>
            <div class='card-header bg-light d-flex justify-content-between align-items-center'>
                <h5 class='mb-0'>{heading}</h5>
        """
        if session.get('admin'):
            content += f"""
                <form method='post' class='d-flex gap-2 align-items-center'>
                    <input type='hidden' name='old_heading' value='{heading}'>
                    <input name='new_heading' placeholder='Rename heading' class='form-control form-control-sm'>
                    <button class='btn btn-sm btn-warning'>Rename</button>
                    <a href='/delete_heading/{heading}' class='btn btn-sm btn-danger'>Delete</a>
                </form>
            """
        content += "</div><div class='card-body'><ul class='list-group list-group-flush'>"

        for file_info in files:
            file_name = file_info['name']
            uploaded_time = datetime.fromisoformat(file_info.get('uploaded', datetime.now().isoformat()))
            is_new = datetime.now() - uploaded_time < timedelta(hours=24)
            new_tag = " <span class='badge bg-success'>🆕 New</span>" if is_new else ""

            content += f"""
                <li class='list-group-item d-flex justify-content-between align-items-center'>
                    <a href='/uploads/{file_name}' target='_blank'>{file_name}</a>{new_tag}
            """
            if session.get('admin'):
                content += f"""<a href='/delete_pdf/{heading}/{file_name}' class='text-danger'>(Delete)</a>"""
            content += "</li>"

        content += "</ul></div></div>"

    if session.get('admin'):
        content += """
        <hr>
        <h4 class='mt-4'>Upload New Policy Document</h4>
        <form method='post' enctype='multipart/form-data' class='w-50'>
            <input name='heading' class='form-control mb-2' placeholder='Policy Heading' required>
            <input name='file' type='file' class='form-control mb-2' required>
            <button class='btn btn-success'>Upload</button>
        </form>
        """

    return render_template_string(TEMPLATE, content=content)

@app.route('/delete_heading/<heading>')
def delete_heading(heading):
    if session.get('admin') and heading in pdfs:
        # Delete associated files
        for file in pdfs[heading]:
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, file))
            except:
                pass
        del pdfs[heading]
    return redirect(url_for('leave'))

@app.route('/delete_pdf/<heading>/<filename>')
def delete_pdf(heading, filename):
    if session.get('admin') and heading in pdfs and filename in pdfs[heading]:
        pdfs[heading].remove(filename)
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, filename))
        except:
            pass
    return redirect(url_for('leave'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    app.run(debug=True)