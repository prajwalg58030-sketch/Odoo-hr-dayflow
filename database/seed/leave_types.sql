INSERT INTO leave_types (name, description, active)
SELECT 'Paid Time Off', 'Paid leave for vacation', TRUE
WHERE NOT EXISTS (
	SELECT 1 FROM leave_types WHERE name = 'Paid Time Off'
);

INSERT INTO leave_types (name, description, active)
SELECT 'Sick Leave', 'Sick leave with certificate', TRUE
WHERE NOT EXISTS (
	SELECT 1 FROM leave_types WHERE name = 'Sick Leave'
);

INSERT INTO leave_types (name, description, active)
SELECT 'Unpaid Leave', 'Unpaid leave', TRUE
WHERE NOT EXISTS (
	SELECT 1 FROM leave_types WHERE name = 'Unpaid Leave'
);
