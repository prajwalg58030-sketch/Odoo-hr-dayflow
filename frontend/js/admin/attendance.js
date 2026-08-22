//frontend/js/admin/attendance.js
document.addEventListener('DOMContentLoaded', async () => {
    if (!Session.requireHR()) return;

    const container = document.getElementById('attendanceTableContainer');
    const searchInput = document.getElementById('searchInput');
    const fromDate = document.getElementById('fromDate');
    const toDate = document.getElementById('toDate');
    const departmentFilter = document.getElementById('departmentFilter');
    const clearBtn = document.getElementById('clearFilters');

    let allEmployees = [];

    async function loadEmployees() {
        try {
            const response = await API.getEmployees();
            allEmployees = response.data;
            const departments = [...new Set(allEmployees.map(e => e.department).filter(Boolean))];
            departmentFilter.innerHTML = '<option value="">All Departments</option>' + departments.map(d => `<option value="${d}">${d}</option>`).join('');
        } catch (error) {
            console.error('Employees load error:', error);
        }
    }

    async function loadAttendance() {
        container.innerHTML = '<div class="spinner"></div>';
        let params = '?';
        if (fromDate.value) params += `from=${fromDate.value}&`;
        if (toDate.value) params += `to=${toDate.value}&`;
        if (searchInput.value) params += `employee_id=${searchInput.value}&`;
        // In real implementation, we'd filter by department through employee list
        try {
            const attendance = await API.getAllAttendance(params);
            if (attendance.data.length === 0) {
                container.innerHTML = '<p>No attendance records found.</p>';
                return;
            }
            // Map employee names
            const empMap = {};
            allEmployees.forEach(e => empMap[e.id] = e);
            const rows = attendance.data.map(a => {
                const emp = empMap[a.employee_id];
                const name = emp ? `${emp.first_name} ${emp.last_name}` : 'Unknown';
                if (departmentFilter.value && emp?.department !== departmentFilter.value) return '';
                return `<tr>
                    <td>${name}</td>
                    <td>${Utils.formatDate(a.date)}</td>
                    <td>${Utils.formatTime(a.check_in)}</td>
                    <td>${Utils.formatTime(a.check_out)}</td>
                    <td>${Utils.formatHours(a.work_hours)}</td>
                    <td>${Utils.formatHours(a.extra_hours)}</td>
                    <td>${Utils.getStatusBadge(a.status)}</td>
                </tr>`;
            }).join('');
            container.innerHTML = `
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Date</th>
                                <th>Check In</th>
                                <th>Check Out</th>
                                <th>Work Hours</th>
                                <th>Extra Hours</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>${rows}</tbody>
                    </table>
                </div>
            `;
        } catch (error) {
            container.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    }

    searchInput.addEventListener('input', Utils.debounce(loadAttendance, 300));
    fromDate.addEventListener('change', loadAttendance);
    toDate.addEventListener('change', loadAttendance);
    departmentFilter.addEventListener('change', loadAttendance);
    clearBtn.addEventListener('click', () => {
        searchInput.value = '';
        fromDate.value = '';
        toDate.value = '';
        departmentFilter.value = '';
        loadAttendance();
    });

    await loadEmployees();
    await loadAttendance();
});