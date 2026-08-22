class Utils {
    static formatDate(dateString) {
        if (!dateString) return '-';
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
    }

    static formatTime(timeString) {
        if (!timeString) return '-';
        const date = new Date(timeString);
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }

    static formatHours(hours) {
        if (hours == null) return '-';
        return `${hours}h`;
    }

    static getStatusBadge(status) {
        const statusMap = {
            'PRESENT': 'present',
            'ABSENT': 'absent',
            'LATE': 'late',
            'LEAVE': 'leave',
            'NOT_MARKED': 'notmarked',
            'PENDING': 'pending',
            'APPROVED': 'approved',
            'REJECTED': 'rejected',
            'CHECKED_OUT': 'present'
        };
        const cssClass = statusMap[status] || 'neutral';
        const displayText = status.replace('_', ' ');
        return `<span class="status-badge status-${cssClass}">${displayText}</span>`;
    }

    static debounce(func, delay = 300) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    }

    static showLoading(element) {
        element.innerHTML = '<div class="spinner"></div>';
    }

    static getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }
}