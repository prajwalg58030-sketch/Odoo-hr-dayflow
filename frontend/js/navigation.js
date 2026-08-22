document.addEventListener('DOMContentLoaded', () => {
    // Check authentication for protected pages
    const path = window.location.pathname;
    const isProtected = path.includes('/admin/') || path.includes('/employee/');
    if (isProtected) {
        if (!Session.requireAuth()) return;
        const user = Session.getUser();
        if (path.includes('/admin/') && user.role !== 'HR') {
            window.location.href = '../employee/dashboard.html';
            return;
        }
        if (path.includes('/employee/') && user.role !== 'EMPLOYEE') {
            window.location.href = '../admin/dashboard.html';
            return;
        }
    }

    // Build sidebar
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        const user = Session.getUser();
        if (user) {
            buildSidebar(user.role);
        }
    }

    // Build navbar
    const navbar = document.getElementById('navbar');
    if (navbar) {
        buildNavbar();
    }

    // Sidebar toggle for mobile
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', () => {
            document.getElementById('sidebar').classList.toggle('open');
            document.getElementById('sidebarOverlay').classList.toggle('open');
        });
    }
});

function buildSidebar(role) {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;
    const hrLinks = [
        { href: '../admin/dashboard.html', text: 'Dashboard', icon: '📊' },
        { href: '../admin/employees.html', text: 'Employees', icon: '👥' },
        { href: '../admin/attendance.html', text: 'Attendance', icon: '🕒' },
        { href: '../admin/leave-requests.html', text: 'Time Off', icon: '🏖️' },
        { href: '../admin/payroll.html', text: 'Payroll', icon: '💰' },
        { href: '../admin/salary-structure.html', text: 'Salary Structure', icon: '📋' }
    ];
    const employeeLinks = [
        { href: '../employee/dashboard.html', text: 'Dashboard', icon: '📊' },
        { href: '../employee/profile.html', text: 'My Profile', icon: '👤' },
        { href: '../employee/attendance.html', text: 'Attendance', icon: '🕒' },
        { href: '../employee/leave.html', text: 'Time Off', icon: '🏖️' },
        { href: '../employee/apply-leave.html', text: 'Apply Leave', icon: '📝' },
        { href: '../employee/salary.html', text: 'My Salary', icon: '💰' }
    ];
    const links = role === 'HR' ? hrLinks : employeeLinks;
    const currentPath = window.location.pathname.split('/').pop();
    sidebar.innerHTML = `
        <div class="sidebar-brand">
            <span>📊</span>
            <span>DAYFLOW</span>
        </div>
        <nav class="sidebar-nav">
            ${links.map(link => `
                <a href="${link.href}" class="sidebar-link ${currentPath === link.href.split('/').pop() ? 'active' : ''}">
                    <span class="sidebar-icon">${link.icon}</span>
                    <span class="sidebar-text">${link.text}</span>
                </a>
            `).join('')}
        </nav>
        <button class="sidebar-toggle" id="sidebarToggle">☰</button>
        <div class="sidebar-overlay" id="sidebarOverlay"></div>
    `;
}

function buildNavbar() {
    const navbar = document.getElementById('navbar');
    if (!navbar) return;
    const user = Session.getUser();
    const initial = user?.email?.[0].toUpperCase() || 'U';
    navbar.innerHTML = `
        <div class="navbar-right">
            <div class="profile-dropdown">
                <div class="profile-trigger" id="profileTrigger">
                    <div class="avatar">${initial}</div>
                    <span>${user?.email || 'User'}</span>
                </div>
                <div class="dropdown-menu" id="profileDropdown">
                    <a href="../employee/profile.html" class="dropdown-item">My Profile</a>
                    <a href="#" class="dropdown-item" id="logoutBtn">Logout</a>
                </div>
            </div>
        </div>
    `;

    const trigger = navbar.querySelector('#profileTrigger');
    const dropdown = navbar.querySelector('#profileDropdown');
    trigger.addEventListener('click', () => {
        dropdown.classList.toggle('open');
    });
    document.addEventListener('click', (e) => {
        if (!trigger.contains(e.target) && !dropdown.contains(e.target)) {
            dropdown.classList.remove('open');
        }
    });
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') dropdown.classList.remove('open');
    });

    const logoutBtn = navbar.querySelector('#logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            Session.clear();
            window.location.href = '../login.html';
        });
    }
}