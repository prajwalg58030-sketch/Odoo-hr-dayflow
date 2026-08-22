document.addEventListener('DOMContentLoaded', () => {
    // Password strength indicator
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', () => {
            const strength = calculatePasswordStrength(passwordInput.value);
            displayPasswordStrength(strength);
        });
    }

    // Toggle password visibility
    document.querySelectorAll('.toggle-password').forEach(btn => {
        btn.addEventListener('click', () => {
            const input = btn.closest('.password-field').querySelector('input');
            input.type = input.type === 'password' ? 'text' : 'password';
            btn.textContent = input.type === 'password' ? '👁' : '🙈';
        });
    });

    // Login form
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const identifier = document.getElementById('identifier').value;
            const password = document.getElementById('password').value;
            const btn = document.getElementById('loginBtn');
            btn.disabled = true;
            btn.textContent = 'Signing in...';
            try {
                const response = await API.login({ login_id: identifier, password });
                Session.setToken(response.data.access_token);
                Session.setUser(response.data.user);
                if (response.data.user.must_change_password) {
                    window.location.href = '../change-password.html';
                } else {
                    window.location.href = response.data.user.role === 'HR' ? '../admin/dashboard.html' : '../employee/dashboard.html';
                }
            } catch (error) {
                Notifications.show(error.message, 'error');
                btn.disabled = false;
                btn.textContent = 'Sign In';
            }
        });
    }

    // Register form
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (!Validation.validateForm(registerForm)) {
                Notifications.show('Please fix the errors', 'error');
                return;
            }
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            if (password !== confirmPassword) {
                Notifications.show('Passwords do not match', 'error');
                return;
            }
            const btn = document.getElementById('registerBtn');
            btn.disabled = true;
            btn.textContent = 'Creating account...';
            const data = {
                company_name: document.getElementById('companyName').value,
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                password: password
                // logo is not sent in JSON; would need FormData for file upload
            };
            try {
                await API.register(data);
                Notifications.show('Registration successful! Please check your email to verify.', 'success');
                setTimeout(() => window.location.href = 'verify-email.html', 2000);
            } catch (error) {
                Notifications.show(error.message, 'error');
                btn.disabled = false;
                btn.textContent = 'Create Account';
            }
        });
    }

    // Verify email page
    const verifyMessage = document.getElementById('verifyMessage');
    if (verifyMessage) {
        const token = Utils.getQueryParam('token');
        const spinner = document.getElementById('verifySpinner');
        const continueBtn = document.getElementById('continueBtn');
        if (!token) {
            verifyMessage.textContent = 'No verification token provided.';
            if (spinner) spinner.style.display = 'none';
            if (continueBtn) continueBtn.style.display = 'inline-block';
            return;
        }
        API.verifyEmail(token)
            .then(() => {
                verifyMessage.textContent = 'Email verified successfully! You can now login.';
                if (spinner) spinner.style.display = 'none';
                if (continueBtn) continueBtn.style.display = 'inline-block';
            })
            .catch(error => {
                verifyMessage.textContent = error.message;
                if (spinner) spinner.style.display = 'none';
                if (continueBtn) continueBtn.style.display = 'inline-block';
            });
    }
});

function calculatePasswordStrength(password) {
    let score = 0;
    if (password.length >= 8) score++;
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) score++;
    if (password.match(/\d/)) score++;
    if (password.match(/[^a-zA-Z\d]/)) score++;
    return score;
}

function displayPasswordStrength(score) {
    const container = document.getElementById('passwordStrength');
    if (!container) return;
    const colors = ['#ef4444', '#f59e0b', '#eab308', '#22c55e'];
    const widths = ['25%', '50%', '75%', '100%'];
    container.innerHTML = '';
    const bar = document.createElement('div');
    bar.className = 'password-strength-bar';
    bar.style.width = widths[Math.min(score, 3)];
    bar.style.background = colors[Math.min(score, 3)];
    container.appendChild(bar);
}