class Validation {
    static isEmail(email) {
        const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return re.test(email);
    }

    static isPhone(phone) {
        const re = /^[+]?[\d\s-]{10,}$/;
        return re.test(phone);
    }

    static isRequired(value) {
        return value.trim().length > 0;
    }

    static isMinLength(value, min) {
        return value.length >= min;
    }

    static isDateBefore(startDate, endDate) {
        return new Date(startDate) <= new Date(endDate);
    }

    static validateForm(form) {
        let isValid = true;
        const fields = form.querySelectorAll('[required]');
        fields.forEach(field => {
            if (!Validation.isRequired(field.value)) {
                field.classList.add('error');
                isValid = false;
            } else {
                field.classList.remove('error');
            }
            if (field.type === 'email' && !Validation.isEmail(field.value)) {
                field.classList.add('error');
                isValid = false;
            }
        });
        return isValid;
    }
}