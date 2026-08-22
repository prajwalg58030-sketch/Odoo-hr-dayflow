document.addEventListener('DOMContentLoaded', async () => {
    if (!Session.requireEmployee()) return;

    try {
        const salary = await API.getMyPayroll();
        const data = salary.data;
        document.getElementById('salaryDetails').innerHTML = `
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
                </div>
                <div class="salary-row total">
                    <span>Net Payable</span>
                    <span>₹${data.net_salary}</span>
                </div>
            </div>
        `;
    } catch (error) {
        document.getElementById('salaryDetails').innerHTML = `<p>Error loading salary: ${error.message}</p>`;
    }
});