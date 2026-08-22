class Session {
    static setToken(token) {
        localStorage.setItem('dayflow_token', token);
    }

    static getToken() {
        return localStorage.getItem('dayflow_token');
    }

    static setUser(user) {
        localStorage.setItem('dayflow_user', JSON.stringify(user));
    }

    static getUser() {
        const user = localStorage.getItem('dayflow_user');
        return user ? JSON.parse(user) : null;
    }

    static clear() {
        localStorage.removeItem('dayflow_token');
        localStorage.removeItem('dayflow_user');
    }

    static isAuthenticated() {
        return !!this.getToken();
    }

    static isHR() {
        const user = this.getUser();
        return user?.role === 'HR';
    }

    static isEmployee() {
        const user = this.getUser();
        return user?.role === 'EMPLOYEE';
    }

    static getEmployeeId() {
        return this.getUser()?.employee_id;
    }

    static requireAuth() {
        if (!this.isAuthenticated()) {
            window.location.href = '../login.html';
            return false;
        }
        return true;
    }

    static requireHR() {
        if (!this.requireAuth() || !this.isHR()) {
            window.location.href = '../employee/dashboard.html';
            return false;
        }
        return true;
    }

    static requireEmployee() {
        if (!this.requireAuth() || !this.isEmployee()) {
            window.location.href = '../admin/dashboard.html';
            return false;
        }
        return true;
    }
}