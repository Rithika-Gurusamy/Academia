const API_URL = "https://academia-ci0l.onrender.com";
let recoveryType = 'password'; // 'password' or 'username'
let countdownTimer;

function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const toggle = input.nextElementSibling;
    if (input.type === "password") {
        input.type = "text";
        toggle.innerText = "🔒";
    } else {
        input.type = "password";
        toggle.innerText = "👁️";
    }
}

function showLogin() {
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('signupForm').classList.add('hidden');
    document.getElementById('recoveryForm').classList.add('hidden');
    document.getElementById('authTabs').classList.remove('hidden');
    document.getElementById('authSubtitle').innerText = "Welcome to your student portal";
    document.getElementById('authToggleText').innerHTML = 'Need an account? <a href="#" onclick="showSignup()">Sign Up</a>';
    document.querySelectorAll('.tab')[0].classList.add('active');
    document.querySelectorAll('.tab')[1].classList.remove('active');
}

function showSignup() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('signupForm').classList.remove('hidden');
    document.getElementById('recoveryForm').classList.add('hidden');
    document.getElementById('authTabs').classList.remove('hidden');
    document.getElementById('authSubtitle').innerText = "Join Academia today";
    document.getElementById('authToggleText').innerHTML = 'Already have an account? <a href="#" onclick="showLogin()">Login</a>';
    document.querySelectorAll('.tab')[0].classList.remove('active');
    document.querySelectorAll('.tab')[1].classList.add('active');
}

function showRecovery(type) {
    recoveryType = type;
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('signupForm').classList.add('hidden');
    document.getElementById('authTabs').classList.add('hidden');
    document.getElementById('recoveryForm').classList.remove('hidden');
    document.getElementById('recoveryStep1').classList.remove('hidden');
    document.getElementById('recoveryStep2').classList.add('hidden');
    document.getElementById('recoveryStep3').classList.add('hidden');

    document.getElementById('authSubtitle').innerText = type === 'password' ? "Reset Your Password" : "Recover Your Username";
    document.getElementById('recoveryText').innerText = `Enter your registered email to receive a 6-digit OTP for ${type} recovery.`;
    document.getElementById('authToggleText').innerHTML = 'Remembered? <a href="#" onclick="showLogin()">Go back to Login</a>';
}

// Handle Login
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const role = document.getElementById('loginRole').value;

    try {
        const response = await fetch(`${API_URL}/login?username=${username}&password=${password}&role=${role}`, {
            method: 'POST'
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('username', username);
            localStorage.setItem('role', data.role);
            localStorage.setItem('user_id', data.user_id);
            if (data.register_no) {
                localStorage.setItem('tempRegNo', data.register_no);
            }
            alert("Login Successful!");

            if (data.role === 'faculty') {
                window.location.href = "faculty_dashboard.html";
            } else {
                window.location.href = "dashboard.html";
            }
        } else {
            alert(data.detail || "Login failed");
        }
    } catch (err) {
        alert("Server error. Make sure backend is running.");
    }
});

// Handle Signup
document.getElementById('signupForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('signupUsername').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirm = document.getElementById('signupConfirm').value;
    const role = document.getElementById('signupRole').value;

    if (password !== confirm) {
        alert("Passwords do not match!");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/signup`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password, role })
        });

        const data = await response.json();

        if (response.ok) {
            alert("Account created successfully! Please login.");
            showLogin();
        } else {
            alert(data.detail || "Signup failed");
        }
    } catch (err) {
        alert("Server error. Make sure backend is running.");
    }
});

// Recovery Logic
async function handleSendOTP() {
    const email = document.getElementById('recoveryEmail').value;
    if (!email) { alert("Please enter your email"); return; }

    const endpoint = recoveryType === 'password' ? '/forgot-password' : '/forgot-username';

    try {
        const response = await fetch(`${API_URL}${endpoint}?email=${email}`, { method: 'POST' });
        const data = await response.json();

        if (response.ok) {
            alert("OTP sent to your email!");
            document.getElementById('recoveryStep1').classList.add('hidden');
            document.getElementById('recoveryStep2').classList.remove('hidden');
            startTimer(300); // 5 minutes
        } else {
            alert(data.detail || "Failed to send OTP");
        }
    } catch (err) {
        alert("Error connecting to server");
    }
}

async function handleVerifyOTP() {
    const email = document.getElementById('recoveryEmail').value;
    const otp = document.getElementById('recoveryOTP').value;

    try {
        const response = await fetch(`${API_URL}/verify-otp?email=${email}&otp_code=${otp}`, { method: 'POST' });
        const data = await response.json();

        if (response.ok) {
            document.getElementById('recoveryStep2').classList.add('hidden');
            document.getElementById('recoveryStep3').classList.remove('hidden');

            if (recoveryType === 'password') {
                document.getElementById('resetPasswordGroup').classList.remove('hidden');
                document.getElementById('retrieveUsernameGroup').classList.add('hidden');
            } else {
                handleRetrieveUsername();
            }
        } else {
            alert(data.detail || "Invalid OTP");
        }
    } catch (err) {
        alert("Error verifying OTP");
    }
}

async function handleRetrieveUsername() {
    const email = document.getElementById('recoveryEmail').value;
    const otp = document.getElementById('recoveryOTP').value;

    try {
        const response = await fetch(`${API_URL}/retrieve-username?email=${email}&otp_code=${otp}`, { method: 'POST' });
        const data = await response.json();

        if (response.ok) {
            document.getElementById('retrieveUsernameGroup').classList.remove('hidden');
            document.getElementById('resetPasswordGroup').classList.add('hidden');
            document.getElementById('displayUsername').innerText = data.username;
        }
    } catch (err) {
        alert("Error retrieving username");
    }
}

async function handleResetPassword() {
    const email = document.getElementById('recoveryEmail').value;
    const otp = document.getElementById('recoveryOTP').value;
    const newPassword = document.getElementById('newPassword').value;
    const confirm = document.getElementById('confirmNewPassword').value;

    if (newPassword !== confirm) { alert("Passwords do not match"); return; }

    try {
        const response = await fetch(`${API_URL}/reset-password?email=${email}&otp_code=${otp}&new_password=${newPassword}`, { method: 'POST' });
        if (response.ok) {
            alert("Password reset successful! You can now login.");
            showLogin();
        } else {
            const data = await response.json();
            alert(data.detail || "Reset failed");
        }
    } catch (err) {
        alert("Error resetting password");
    }
}

function startTimer(duration) {
    clearInterval(countdownTimer);
    let timer = duration, minutes, seconds;
    const display = document.getElementById('timeLeft');

    countdownTimer = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            clearInterval(countdownTimer);
            alert("OTP Expired. Please request a new one.");
            showRecovery(recoveryType);
        }
    }, 1000);
}
