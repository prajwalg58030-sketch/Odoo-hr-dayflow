document.addEventListener('DOMContentLoaded', async () => {
    if (!Session.requireEmployee()) return;

    const employeeId = Session.getEmployeeId();
    const user = Session.getUser();
    document.getElementById('employeeName').textContent = user?.email?.split('@')[0] || 'Employee';
    document.getElementById('currentDate').textContent = new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    // Fetch attendance status
    try {
        const attendance = await API.getMyAttendance();
        const today = new Date().toISOString().split('T')[0];
        const todayRecord = attendance.data?.find(a => a.date === today);
        updateAttendanceStatus(todayRecord);
    } catch (error) {
        Notifications.show(error.message, 'error');
    }

    // Fetch summary
    try {
        const summary = await API.getMyAttendanceSummary();
        document.getElementById('workHours').textContent = Utils.formatHours(summary.data?.total_work_hours);
        document.getElementById('extraHours').textContent = Utils.formatHours(summary.data?.extra_hours);
    } catch (error) {
        console.error('Summary error:', error);
    }

    // Fetch leave balances
    try {
        const allocations = await API.getMyAllocations();
        const balanceHtml = allocations.data?.map(alloc => `
            <div class="balance-item">
                <span>${alloc.leave_type_name}</span>
                <span>${alloc.remaining_days} days</span>
            </div>
        `).join('') || 'No leave allocated';
        document.getElementById('leaveBalance').innerHTML = balanceHtml;
    } catch (error) {
        document.getElementById('leaveBalance').textContent = 'Unable to load';
    }

    // Recent activity placeholder
    document.getElementById('recentActivity').innerHTML = '<p>No recent activity</p>';
});

function updateAttendanceStatus(record) {
    const container = document.getElementById('attendanceStatusContent');
    if (!record) {
        container.innerHTML = `<span class="status-indicator"><span class="status-dot notmarked"></span> Not Checked In</span>`;
    } else if (record.check_in && !record.check_out) {
        container.innerHTML = `<span class="status-indicator"><span class="status-dot present"></span> Working</span>`;
    } else if (record.check_out) {
        container.innerHTML = `<span class="status-indicator"><span class="status-dot present"></span> Checked Out</span>`;
    }
}