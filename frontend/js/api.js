class API {
    static async request(endpoint, method = 'GET', body = null, auth = true) {
        const headers = { 'Content-Type': 'application/json' };
        if (auth) {
            const token = Session.getToken();
            if (token) headers['Authorization'] = `Bearer ${token}`;
        }

        const options = { method, headers };
        if (body) options.body = JSON.stringify(body);

        const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, options);
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.message || 'Request failed');
        }
        return data;
    }

    // Auth
    static login(credentials) { return this.request('/auth/login', 'POST', credentials, false); }
    static register(data) { return this.request('/auth/register', 'POST', data, false); }
    static verifyEmail(token) { return this.request('/auth/verify-email', 'POST', { token }, false); }
    static changePassword(data) { return this.request('/auth/change-password', 'POST', data); }

    // Employee
    static getMe() { return this.request('/employees/me'); }
    static updateMe(data) { return this.request('/employees/me', 'PUT', data); }
    static getEmployees(params = '') { return this.request(`/employees${params}`); }
    static createEmployee(data) { return this.request('/employees', 'POST', data); }
    static getEmployee(id) { return this.request(`/employees/${id}`); }
    static updateEmployee(id, data) { return this.request(`/employees/${id}`, 'PUT', data); }

    // Attendance
    static checkIn() { return this.request('/attendance/check-in', 'POST'); }
    static checkOut() { return this.request('/attendance/check-out', 'POST'); }
    static getMyAttendance(params = '') { return this.request(`/attendance/me${params}`); }
    static getMyAttendanceSummary() { return this.request('/attendance/me/summary'); }
    static getAllAttendance(params = '') { return this.request(`/attendance${params}`); }
    static getEmployeeAttendance(employeeId, params = '') { return this.request(`/attendance/employee/${employeeId}${params}`); }

    // Leaves
    static applyLeave(data) { return this.request('/leaves', 'POST', data); }
    static getMyLeaves() { return this.request('/leaves/me'); }
    static getAllLeaves(params = '') { return this.request(`/leaves${params}`); }
    static getLeave(id) { return this.request(`/leaves/${id}`); }
    static approveLeave(id) { return this.request(`/leaves/${id}/approve`, 'PUT'); }
    static rejectLeave(id, comment) { return this.request(`/leaves/${id}/reject`, 'PUT', { admin_comment: comment }); }
    static getMyAllocations() { return this.request('/leave-allocations/me'); }
    static getAllAllocations() { return this.request('/leave-allocations'); }

    // Payroll
    static getMyPayroll() { return this.request('/payroll/me'); }
    static getAllPayroll(params = '') { return this.request(`/payroll${params}`); }
    static getEmployeePayroll(employeeId) { return this.request(`/payroll/${employeeId}`); }
    static updateEmployeePayroll(employeeId, data) { return this.request(`/payroll/${employeeId}`, 'PUT', data); }
    static getSalaryStructure(employeeId) { return this.request(`/salary-structure/${employeeId}`); }
    static updateSalaryStructure(employeeId, data) { return this.request(`/salary-structure/${employeeId}`, 'PUT', data); }
}