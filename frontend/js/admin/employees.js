document.addEventListener('DOMContentLoaded', async () => {
    if (!Session.requireHR()) return;

    let employees = [];
    let filteredEmployees = [];

    const grid = document.getElementById('employeeGrid');
    const addBtn = document.getElementById('addEmployeeBtn');
    const modal = document.getElementById('addEmployeeModal');
    const credentialsModal = document.getElementById('credentialsModal');
    const form = document.getElementById('createEmployeeForm');
    const searchInput = document.getElementById('searchInput');
    const departmentFilter = document.getElementById('departmentFilter');
    const clearFiltersBtn = document.getElementById('clearFilters');

    // Modal handling
    addBtn.addEventListener('click', () => {
        modal.classList.add('open');
    });
    modal.querySelector('.modal-close').addEventListener('click', () => {
        modal.classList.remove('open');
    });
    credentialsModal.querySelector('.modal-close').addEventListener('click', () => {
        credentialsModal.classList.remove('open');
    });

    // Load employees
    async function loadEmployees() {
        grid.innerHTML = '<div class="spinner"></div>';
        try {
            const response = await API.getEmployees();
            employees = response.data;
            filteredEmployees = [...employees];
            renderEmployees();
            populateDepartmentFilter();
        } catch (error) {
            grid.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    }

    function renderEmployees() {
        if (filteredEmployees.length === 0) {
            grid.innerHTML = '<p>No employees found.</p>';
            return;
        }
        grid.innerHTML = filteredEmployees.map(emp => `
            <a href="employee-details.html?id=${emp.id}" class="employee-card">
                <div class="employee-card-header">
                    <div class="employee-avatar">${emp.first_name?.[0]}${emp.last_name?.[0]}</div>
                    <div class="employee-info">
                        <h3>${emp.first_name} ${emp.last_name}</h3>
                        <p>${emp.designation || 'No designation'}</p>
                    </div>
                </div>
                <div class="employee-card-body">
                    <span class="employee-login-id">${emp.employee_login_id}</span>
                    <p>${emp.department || 'No department'}</p>
                </div>
            </a>
        `).join('');
    }

    function populateDepartmentFilter() {
        const departments = [...new Set(employees.map(e => e.department).filter(Boolean))];
        departmentFilter.innerHTML = '<option value="">All Departments</option>' + departments.map(d => `<option value="${d}">${d}</option>`).join('');
    }

    // Search and filter
    searchInput.addEventListener('input', Utils.debounce(() => {
        const query = searchInput.value.toLowerCase();
        const dept = departmentFilter.value;
        filteredEmployees = employees.filter(emp => {
            const matchesSearch = !query || emp.first_name.toLowerCase().includes(query) || 
                                  emp.last_name.toLowerCase().includes(query) ||
                                  emp.employee_login_id.toLowerCase().includes(query);
            const matchesDept = !dept || emp.department === dept;
            return matchesSearch && matchesDept;
        });
        renderEmployees();
    }, 300));

    departmentFilter.addEventListener('change', () => {
        const query = searchInput.value.toLowerCase();
        const dept = departmentFilter.value;
        filteredEmployees = employees.filter(emp => {
            const matchesSearch = !query || emp.first_name.toLowerCase().includes(query) || 
                                  emp.last_name.toLowerCase().includes(query) ||
                                  emp.employee_login_id.toLowerCase().includes(query);
            const matchesDept = !dept || emp.department === dept;
            return matchesSearch && matchesDept;
        });
        renderEmployees();
    });

    clearFiltersBtn.addEventListener('click', () => {
        searchInput.value = '';
        departmentFilter.value = '';
        filteredEmployees = [...employees];
        renderEmployees();
    });

    // Create employee
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!Validation.validateForm(form)) return;
        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());
        try {
            const result = await API.createEmployee(data);
            modal.classList.remove('open');
            form.reset();
            // Show credentials
            document.getElementById('credLoginId').textContent = result.data.login_id;
            document.getElementById('credPassword').textContent = result.data.temp_password;
            credentialsModal.classList.add('open');
            loadEmployees();
        } catch (error) {
            Notifications.show(error.message, 'error');
        }
    });

    // Copy credentials
    document.getElementById('copyLoginId').addEventListener('click', () => {
        navigator.clipboard.writeText(document.getElementById('credLoginId').textContent);
        Notifications.show('Copied!', 'success');
    });
    document.getElementById('copyPassword').addEventListener('click', () => {
        navigator.clipboard.writeText(document.getElementById('credPassword').textContent);
        Notifications.show('Copied!', 'success');
    });

    // Initial load
    loadEmployees();
});