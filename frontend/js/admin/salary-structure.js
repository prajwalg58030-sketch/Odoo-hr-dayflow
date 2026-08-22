document.addEventListener('DOMContentLoaded', async () => {
    if (!Session.requireHR()) return;

    const employeeSelect = document.getElementById('employeeSelect');
    const body = document.getElementById('salaryStructureBody');

    // Load employees
    try {
        const employees = await API.getEmployees();
        employeeSelect.innerHTML = '<option value="">Select Employee</option>' + employees.data.map(e => `<option value="${e.id}">${e.first_name} ${e.last_name} (${e.employee_login_id})</option>`).join('');
    } catch (error) {
        console.error('Employees load error:', error);
    }

    employeeSelect.addEventListener('change', async () => {
        const employeeId = employeeSelect.value;
        if (!employeeId) {
            body.innerHTML = '<p>Select an employee to view salary structure.</p>';
            return;
        }
        body.innerHTML = '<div class="spinner"></div>';
        try {
            const response = await API.getSalaryStructure(employeeId);
            const data = response.data;
            body.innerHTML = `
                <div class="salary-breakdown">
                    <div class="salary-row">
                        <span>Monthly Wage</span>
                        <span>₹${data.monthly_wage}</span>
                    </div>
                    <div class="earnings-section">
                        <h4>Earnings</h4>
                        <div class="salary-row"><span>Basic Salary</span><span>₹${data.basic_salary}</span></div>
                        <div class="salary-row"><span>HRA</span><span>₹${data.hra}</span></div>
                        <div class="salary-row"><span>Standard Allowance</span><span>₹${data.standard_allowance}</span></div>
                        <div class="salary-row"><span>Performance Bonus</span><span>₹${data.performance_bonus}</span></div>
                        <div class="salary-row"><span>LTA</span><span>₹${data.lta}</span></div>
                        <div class="salary-row"><span>Fixed Allowance</span><span>₹${data.fixed_allowance}</span></div>
                    </div>
                    <div class="deductions-section">
                        <h4>Deductions</h4>
                        <div class="salary-row"><span>PF</span><span>₹${data.pf}</span></div>
                        <div class="salary-row"><span>Professional Tax</span><span>₹${data.professional_tax}</span></div>
                        <div class="salary-row"><span>Other</span><span>₹${data.other_deductions}</span></div>
                    </div>
                    <div class="salary-row total">
                        <span>Net Payable</span>
                        <span>₹${data.net_salary}</span>
                    </div>
                </div>
            `;
        } catch (error) {
            body.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    });
});