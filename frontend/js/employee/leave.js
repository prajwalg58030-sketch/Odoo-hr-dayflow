// This file is used for both leave.html and apply-leave.html
document.addEventListener('DOMContentLoaded', async () => {
    // Common functions
    const loadLeaveTypes = async () => {
        const response = await API.getLeaveTypes();
        return response.data;
    };

    // For apply-leave.html
    const applyForm = document.getElementById('applyLeaveForm');
    if (applyForm) {
        const leaveTypeSelect = document.getElementById('leaveType');
        const startDate = document.getElementById('startDate');
        const endDate = document.getElementById('endDate');
        const daysInput = document.getElementById('days');

        const types = await loadLeaveTypes();
        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type.id;
            option.textContent = type.name;
            leaveTypeSelect.appendChild(option);
        });

        startDate.addEventListener('change', calculateDays);
        endDate.addEventListener('change', calculateDays);

        function calculateDays() {
            if (startDate.value && endDate.value) {
                const start = new Date(startDate.value);
                const end = new Date(endDate.value);
                const diff = (end - start) / (1000 * 60 * 60 * 24) + 1;
                daysInput.value = diff > 0 ? diff : 0;
            }
        }

        applyForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (!Validation.validateForm(applyForm)) return;
            const data = {
                leave_type_id: parseInt(leaveTypeSelect.value),
                start_date: startDate.value,
                end_date: endDate.value,
                remarks: document.getElementById('remarks').value
            };
            // Handle attachment if present
            const attachment = document.getElementById('attachment').files[0];
            if (attachment) {
                // In production, upload file first and get path
                // For now, just send filename
                data.attachment_path = attachment.name;
            }
            try {
                await API.applyLeave(data);
                Notifications.show('Leave application submitted', 'success');
                setTimeout(() => window.location.href = 'leave.html', 1500);
            } catch (error) {
                Notifications.show(error.message, 'error');
            }
        });
    }

    // For leave.html
    const balanceContainer = document.getElementById('leaveBalanceCards');
    if (balanceContainer) {
        try {
            const allocations = await API.getMyAllocations();
            if (allocations.data.length === 0) {
                balanceContainer.innerHTML = '<p>No leave allocations found.</p>';
            } else {
                balanceContainer.innerHTML = allocations.data.map(alloc => `
                    <div class="balance-card">
                        <div class="leave-type">${alloc.leave_type_name}</div>
                        <div class="available-days">${alloc.remaining_days}</div>
                        <div class="balance-progress">
                            <div class="balance-progress-bar" style="width: ${(alloc.remaining_days / (alloc.allocated_days || 1)) * 100}%"></div>
                        </div>
                        <small>Used: ${alloc.used_days} / ${alloc.allocated_days}</small>
                    </div>
                `).join('');
            }
        } catch (error) {
            balanceContainer.innerHTML = '<p>Error loading leave balances.</p>';
        }

        // Load leave requests
        try {
            const leaves = await API.getMyLeaves();
            const container = document.getElementById('leaveRequestsContainer');
            if (leaves.data.length === 0) {
                container.innerHTML = '<p>No time-off requests yet.</p>';
            } else {
                const rows = leaves.data.map(leave => `
                    <tr>
                        <td>${leave.leave_type_name}</td>
                        <td>${Utils.formatDate(leave.start_date)}</td>
                        <td>${Utils.formatDate(leave.end_date)}</td>
                        <td>${leave.days}</td>
                        <td>${Utils.getStatusBadge(leave.status)}</td>
                    </tr>
                `).join('');
                container.innerHTML = `
                    <div class="table-container">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Type</th>
                                    <th>Start</th>
                                    <th>End</th>
                                    <th>Days</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>${rows}</tbody>
                        </table>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Leave requests error:', error);
        }

        // Load calendar (simplified)
        const calendarContainer = document.getElementById('leaveCalendar');
        calendarContainer.innerHTML = '<p>Calendar view coming soon.</p>';
    }
});