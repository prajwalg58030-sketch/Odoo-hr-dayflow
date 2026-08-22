-- Salaries table
CREATE TABLE IF NOT EXISTS salaries (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    monthly_wage NUMERIC(12,2) NOT NULL,
    basic_salary NUMERIC(12,2),
    hra NUMERIC(12,2),
    standard_allowance NUMERIC(12,2),
    performance_bonus NUMERIC(12,2),
    lta NUMERIC(12,2),
    fixed_allowance NUMERIC(12,2),
    pf NUMERIC(12,2),
    professional_tax NUMERIC(12,2),
    other_deductions NUMERIC(12,2),
    gross_salary NUMERIC(12,2),
    net_salary NUMERIC(12,2),
    effective_from DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_salaries_employee_id ON salaries(employee_id);
CREATE INDEX idx_salaries_effective_from ON salaries(effective_from);