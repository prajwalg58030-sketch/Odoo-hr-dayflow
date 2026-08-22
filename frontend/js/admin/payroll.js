//frontend/js/admin/payroll.js

document.addEventListener('DOMContentLoaded', async () => {
    if (!Session.requireHR()) return;

    const container = document.getElementById('payrollTable');
    const monthFilter = document.getElementById('monthFilter');
    const departmentFilter = document.getElementById('departmentFilter');

    // Populate month filter
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    monthFilter.innerHTML = '<option value="">All Months</option>' + months.map((m, i) => `<option value="${i+1}">${m}</option>`).join('');

    async function loadPayroll() {
        container.innerHTML = '<div class="spinner"></div>';
        try {
            const payroll = await API.getAllPayroll();
            if (payroll.data.length === 0) {
                container.innerHTML = '<p>No payroll records found.</p>';
                return;
            }
            // Map employee names (assume employee data available in each record)
            const rows = payroll.data.map(p => `
                <tr>
                    <td>${p.employee_name || 'Unknown'}</td>
                    <td>₹${p.monthly_wage}</td>
                    <td>₹${p.gross_salary}</td>
                    <td>₹${p.net_salary}</td>
                    <td>₹${p.pf + p.professional_tax}</td>
                    <td>${p.effective_from}</td>
                </tr>
            `).join('');
            container.innerHTML = `
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Employee</th>
                                <th>Monthly Wage</th>
                                <th>Gross</th>
                                <th>Net Payable</th>
                                <th>Deductions</th>
                                <th>Effective From</th>
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

    monthFilter.addEventListener('change', loadPayroll);
    departmentFilter.addEventListener('change', loadPayroll);

    await loadPayroll();
});