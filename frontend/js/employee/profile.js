document.addEventListener('DOMContentLoaded', async () => {
    if (!Session.requireEmployee()) return;

    try {
        const response = await API.getMe();
        const employee = response.data;
        document.getElementById('profileDetails').innerHTML = `
            <div class="profile-info-item">
                <div class="profile-info-label">Full Name</div>
                <div class="profile-info-value">${employee.first_name} ${employee.last_name}</div>
            </div>
            <div class="profile-info-item">
                <div class="profile-info-label">Employee ID</div>
                <div class="profile-info-value">${employee.employee_login_id}</div>
            </div>
            <div class="profile-info-item">
                <div class="profile-info-label">Email</div>
                <div class="profile-info-value">${employee.email}</div>
            </div>
            <div class="profile-info-item">
                <div class="profile-info-label">Phone</div>
                <div class="profile-info-value">${employee.phone || '-'}</div>
            </div>
            <div class="profile-info-item">
                <div class="profile-info-label">Department</div>
                <div class="profile-info-value">${employee.department || '-'}</div>
            </div>
            <div class="profile-info-item">
                <div class="profile-info-label">Designation</div>
                <div class="profile-info-value">${employee.designation || '-'}</div>
            </div>
            <div class="profile-info-item">
                <div class="profile-info-label">Joining Date</div>
                <div class="profile-info-value">${Utils.formatDate(employee.joining_date)}</div>
            </div>
        `;

        // Populate edit form
        document.getElementById('phone').value = employee.phone || '';
        document.getElementById('address').value = employee.address || '';
    } catch (error) {
        Notifications.show(error.message, 'error');
    }

    const form = document.getElementById('profileForm');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                phone: document.getElementById('phone').value,
                address: document.getElementById('address').value
            };
            try {
                await API.updateMe(data);
                Notifications.show('Profile updated', 'success');
            } catch (error) {
                Notifications.show(error.message, 'error');
            }
        });
    }
});