document.addEventListener('DOMContentLoaded', async () => {
    if (!Session.requireEmployee()) return;

    const checkInBtn = document.getElementById('checkInBtn');
    const checkOutBtn = document.getElementById('checkOutBtn');
    let currentMonth = new Date();
    let currentMonthStr = currentMonth.toISOString().slice(0, 7);

    // Check current attendance status
    try {
        const attendance = await API.getMyAttendance(`?from=${currentMonthStr}-01&to=${currentMonthStr}-31`);
        const today = new Date().toISOString().split('T')[0];
        const todayRecord = attendance.data?.find(a => a.date === today);
        if (todayRecord?.check_in && !todayRecord?.check_out) {
            checkInBtn.style.display = 'none';
            checkOutBtn.style.display = 'inline-block';
        } else if (todayRecord?.check_out) {
            checkInBtn.style.display = 'none';
            checkOutBtn.style.display = 'none';
        }
    } catch (error) {
        console.error('Status check error:', error);
    }

    // Check-in
    checkInBtn.addEventListener('click', async () => {
        try {
            await API.checkIn();
            Notifications.show('Check-in successful', 'success');
            checkInBtn.style.display = 'none';
            checkOutBtn.style.display = 'inline-block';
            loadAttendance();
        } catch (error) {
            Notifications.show(error.message, 'error');
        }
    });

    // Check-out
    checkOutBtn.addEventListener('click', async () => {
        try {
            await API.checkOut();
            Notifications.show('Check-out successful', 'success');
            checkOutBtn.style.display = 'none';
            loadAttendance();
        } catch (error) {
            Notifications.show(error.message, 'error');
        }
    });

    // Summary
    async function loadSummary() {
        try {
            const summary = await API.getMyAttendanceSummary();
            document.getElementById('attendanceSummary').innerHTML = `
                <div class="summary-card">
                    <div class="summary-value">${summary.data.present_days}</div>
                    <div class="summary-label">Present</div>
                </div>
                <div class="summary-card">
                    <div class="summary-value">${summary.data.absent_days}</div>
                    <div class="summary-label">Absent</div>
                </div>
                <div class="summary-card">
                    <div class="summary-value">${summary.data.total_work_hours}</div>
                    <div class="summary-label">Work Hours</div>
                </div>
                <div class="summary-card">
                    <div class="summary-value">${summary.data.extra_hours}</div>
                    <div class="summary-label">Extra Hours</div>
                </div>
            `;
        } catch (error) {
            console.error('Summary error:', error);
        }
    }

    // Load attendance table
    async function loadAttendance() {
        const container = document.getElementById('attendanceTableContainer');
        container.innerHTML = '<div class="spinner"></div>';
        try {
            const attendance = await API.getMyAttendance(`?from=${currentMonthStr}-01&to=${currentMonthStr}-31`);
            if (attendance.data.length === 0) {
                container.innerHTML = '<p>No attendance records for this period.</p>';
                return;
            }
            const rows = attendance.data.map(record => `
                <tr>
                    <td>${Utils.formatDate(record.date)}</td>
                    <td>${Utils.formatTime(record.check_in)}</td>
                    <td>${Utils.formatTime(record.check_out)}</td>
                    <td>${Utils.formatHours(record.work_hours)}</td>
                    <td>${Utils.formatHours(record.extra_hours)}</td>
                    <td>${Utils.getStatusBadge(record.status)}</td>
                </tr>
            `).join('');
            container.innerHTML = `
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
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
            container.innerHTML = `<p>Error loading attendance: ${error.message}</p>`;
        }
    }

    // Month navigation
    document.getElementById('prevMonth').addEventListener('click', () => {
        currentMonth.setMonth(currentMonth.getMonth() - 1);
        currentMonthStr = currentMonth.toISOString().slice(0, 7);
        document.getElementById('currentMonthLabel').textContent = currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
        loadAttendance();
        loadSummary();
    });

    document.getElementById('nextMonth').addEventListener('click', () => {
        currentMonth.setMonth(currentMonth.getMonth() + 1);
        currentMonthStr = currentMonth.toISOString().slice(0, 7);
        document.getElementById('currentMonthLabel').textContent = currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
        loadAttendance();
        loadSummary();
    });

    // Initial load
    document.getElementById('currentMonthLabel').textContent = currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
    loadAttendance();
    loadSummary();
});