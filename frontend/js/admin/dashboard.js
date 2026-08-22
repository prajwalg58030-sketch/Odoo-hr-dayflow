//frontend/js/admin/dashboard.js

document.addEventListener('DOMContentLoaded', async () => {
    if (!Session.requireHR()) return;

    // Load metrics (mock data for demo, would come from API)
    const metrics = [
        { label: 'Total Employees', value: 12, icon: '👥' },
        { label: 'Present Today', value: 8, icon: '✅' },
        { label: 'On Leave', value: 2, icon: '🏖️' },
        { label: 'Absent', value: 2, icon: '❌' },
        { label: 'Pending Requests', value: 3, icon: '⏳' }
    ];
    document.getElementById('metricGrid').innerHTML = metrics.map(metric => `
        <div class="metric-card">
            <div class="metric-icon">${metric.icon}</div>
            <div class="metric-info">
                <h3>${metric.label}</h3>
                <div class="metric-value">${metric.value}</div>
            </div>
        </div>
    `).join('');

    // Charts
    const attendanceCtx = document.getElementById('attendanceChart').getContext('2d');
    new Chart(attendanceCtx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            datasets: [{
                label: 'Attendance',
                data: [10, 11, 9, 12, 10],
                borderColor: '#6366f1',
                tension: 0.3
            }]
        },
        options: { responsive: true }
    });

    const deptCtx = document.getElementById('departmentChart').getContext('2d');
    new Chart(deptCtx, {
        type: 'doughnut',
        data: {
            labels: ['Engineering', 'Sales', 'HR', 'Marketing'],
            datasets: [{
                data: [5, 3, 2, 2],
                backgroundColor: ['#6366f1', '#a855f7', '#22c55e', '#f59e0b']
            }]
        },
        options: { responsive: true }
    });

    // Pending leaves table
    try {
        const leaves = await API.getAllLeaves('?status=PENDING');
        const container = document.getElementById('pendingLeavesTable');
        if (leaves.data.length === 0) {
            container.innerHTML = '<p>No pending leave requests.</p>';
        } else {
            const rows = leaves.data.map(leave => `
                <tr>
                    <td>${leave.employee_name}</td>
                    <td>${leave.leave_type_name}</td>
                    <td>${Utils.formatDate(leave.start_date)}</td>
                    <td>${leave.days}</td>
                    <td><button class="btn btn-sm btn-success" onclick="approveLeave(${leave.id})">Approve</button></td>
                </tr>
            `).join('');
            container.innerHTML = `<div class="table-container"><table class="table"><thead><tr><th>Employee</th><th>Type</th><th>Start</th><th>Days</th><th>Action</th></tr></thead><tbody>${rows}</tbody></table></div>`;
        }
    } catch (error) {
        console.error('Pending leaves error:', error);
    }
});

function approveLeave(id) {
    API.approveLeave(id)
        .then(() => {
            Notifications.show('Leave approved', 'success');
            location.reload();
        })
        .catch(error => Notifications.show(error.message, 'error'));
}