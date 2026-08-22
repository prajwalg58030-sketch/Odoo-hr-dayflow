//frontend/js/admin/employee-details.js

document.addEventListener('DOMContentLoaded', async () => {
    if (!Session.requireHR()) return;

    const employeeId = Utils.getQueryParam('id');
    if (!employeeId) {
        window.location.href = 'employees.html';
        return;
    }

    try {
        const response = await API.getEmployee(employeeId);
        const emp = response.data;
        document.getElementById('employeeName').textContent = `${emp.first_name} ${emp.last_name}`;
        document.getElementById('profileSection').innerHTML = `
            <p><strong>Employee ID:</strong> ${emp.employee_login_id}</p>
            <p><strong>Email:</strong> ${emp.email}</p>
            <p><strong>Phone:</strong> ${emp.phone || '-'}</p>
            <p><strong>Address:</strong> ${emp.address || '-'}</p>
        `;
        document.getElementById('workInfoSection').innerHTML = `
            <p><strong>Department:</strong> ${emp.department || '-'}</p>
            <p><strong>Designation:</strong> ${emp.designation || '-'}</p>
            <p><strong>Joining Date:</strong> ${Utils.formatDate(emp.joining_date)}</p>
        `;

        // Load attendance
        const attendance = await API.getEmployeeAttendance(employeeId);
        const attContainer = document.getElementById('attendanceSection');
        if (attendance.data.length === 0) {
            attContainer.innerHTML = '<p>No attendance records.</p>';
        } else {
            const rows = attendance.data.slice(0, 5).map(a => `
                <tr><td>${Utils.formatDate(a.date)}</td><td>${Utils.formatTime(a.check_in)}</td><td>${Utils.formatTime(a.check_out)}</td><td>${Utils.getStatusBadge(a.status)}</td></tr>
            `).join('');
            attContainer.innerHTML = `<div class="table-container"><table class="table"><thead><tr><th>Date</th><th>In</th><th>Out</th><th>Status</th></tr></thead><tbody>${rows}</tbody></table></div>`;
        }

        // Load leaves
        const leaves = await API.getAllLeaves(`?employee_id=${employeeId}`);
        const leaveContainer = document.getElementById('leaveSection');
        if (leaves.data.length === 0) {
            leaveContainer.innerHTML = '<p>No leave requests.</p>';
        } else {
            const rows = leaves.data.slice(0, 5).map(l => `
                <tr><td>${l.leave_type_name}</td><td>${Utils.formatDate(l.start_date)}</td><td>${l.days}</td><td>${Utils.getStatusBadge(l.status)}</td></tr>
            `).join('');
            leaveContainer.innerHTML = `<div class="table-container"><table class="table"><thead><tr><th>Type</th><th>Start</th><th>Days</th><th>Status</th></tr></thead><tbody>${rows}</tbody></table></div>`;
        }

        // Documents placeholder
        document.getElementById('documentsSection').innerHTML = '<p>No documents uploaded.</p>';
    } catch (error) {
        Notifications.show(error.message, 'error');
    }
});