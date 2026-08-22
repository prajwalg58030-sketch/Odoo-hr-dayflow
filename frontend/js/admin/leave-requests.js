document.addEventListener('DOMContentLoaded', async () => {
    if (!Session.requireHR()) return;

    const container = document.getElementById('leaveRequestsTable');
    const statusFilter = document.getElementById('statusFilter');
    const leaveTypeFilter = document.getElementById('leaveTypeFilter');
    const rejectModal = document.getElementById('rejectModal');
    const rejectForm = document.getElementById('rejectForm');
    const rejectLeaveId = document.getElementById('rejectLeaveId');
    const adminComment = document.getElementById('adminComment');

    let allLeaves = [];

    // Load leave types for filter (hardcoded for demo)
    const leaveTypes = [
        { id: 1, name: 'Paid Time Off' },
        { id: 2, name: 'Sick Leave' },
        { id: 3, name: 'Unpaid Leave' }
    ];
    leaveTypeFilter.innerHTML = '<option value="">All Types</option>' + leaveTypes.map(t => `<option value="${t.id}">${t.name}</option>`).join('');

    async function loadLeaves() {
        container.innerHTML = '<div class="spinner"></div>';
        let params = '?';
        if (statusFilter.value) params += `status=${statusFilter.value}&`;
        if (leaveTypeFilter.value) params += `leave_type_id=${leaveTypeFilter.value}&`;
        try {
            const response = await API.getAllLeaves(params);
            allLeaves = response.data;
            if (allLeaves.length === 0) {
                container.innerHTML = '<p>No leave requests found.</p>';
                return;
            }
            const rows = allLeaves.map(leave => `
                <tr>
                    <td>${leave.employee_name || 'Unknown'}</td>
                    <td>${leave.leave_type_name}</td>
                    <td>${Utils.formatDate(leave.start_date)}</td>
                    <td>${Utils.formatDate(leave.end_date)}</td>
                    <td>${leave.days}</td>
                    <td>${Utils.getStatusBadge(leave.status)}</td>
                    <td class="table-actions">
                        ${leave.status === 'PENDING' ? `
                            <button class="btn btn-sm btn-success" onclick="approveLeave(${leave.id})">Approve</button>
                            <button class="btn btn-sm btn-danger" onclick="openReject(${leave.id})">Reject</button>
                        ` : '-'}
                    </td>
                </tr>
            `).join('');
            container.innerHTML = `
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Type</th>
                                <th>Start</th>
                                <th>End</th>
                                <th>Days</th>
                                <th>Status</th>
                                <th>Actions</th>
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

    window.approveLeave = async (id) => {
        try {
            await API.approveLeave(id);
            Notifications.show('Leave approved', 'success');
            loadLeaves();
        } catch (error) {
            Notifications.show(error.message, 'error');
        }
    };

    window.openReject = (id) => {
        rejectLeaveId.value = id;
        rejectModal.classList.add('open');
    };

    rejectModal.querySelector('.modal-close').addEventListener('click', () => {
        rejectModal.classList.remove('open');
    });

    rejectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = rejectLeaveId.value;
        const comment = adminComment.value;
        try {
            await API.rejectLeave(id, comment);
            rejectModal.classList.remove('open');
            adminComment.value = '';
            Notifications.show('Leave rejected', 'success');
            loadLeaves();
        } catch (error) {
            Notifications.show(error.message, 'error');
        }
    });

    statusFilter.addEventListener('change', loadLeaves);
    leaveTypeFilter.addEventListener('change', loadLeaves);

    await loadLeaves();
});