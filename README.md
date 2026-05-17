# Passport Management

A Frappe/ERPNext app for centralized passport movement and tracking within an organization.

## Features

- Passport collection (IN) and return (OUT) tracking
- Auto-fetch of employee details (name, passport number, department, designation)
- Dynamic naming series: `PM-IN-YYYY-#####` / `PM-OUT-YYYY-#####`
- Approval workflow (Draft → Pending Approval → Approved → Collected/Returned)
- Duplicate prevention: blocks second active IN for same employee
- Business rule enforcement: OUT requires a prior submitted IN
- Audit trail via track_changes
- 5 built-in reports
- Daily overdue email alerts
- Passport expiry reminders (30/60/90 days)

## Installation

```bash
bench get-app https://github.com/yousafaj/passport_management
bench --site your-site install-app passport_management
bench migrate
```

## License

MIT

