app_name = "passport_management"
app_title = "Passport Management"
app_publisher = "Your Organization"
app_description = "Centralized passport movement and tracking for ERPNext"
app_email = "admin@yourorg.com"
app_license = "MIT"

# App icon shown in the Desk
app_logo_url = "/assets/passport_management/images/passport_logo.svg"

# Installation / migration hooks — ensure required custom fields exist
after_install = "passport_management.install.after_install"
after_migrate = "passport_management.install.after_migrate"

# Add a "Passport Management" section to the Employee form's Connections panel
override_doctype_dashboards = {
    "Employee": "passport_management.passport_management.employee_dashboard.get_dashboard_data"
}

# Scheduled Tasks
scheduler_events = {
    "daily": [
        "passport_management.tasks.send_overdue_passport_alerts"
    ],
    "daily_long": [
        "passport_management.tasks.send_expiry_reminders"
    ],
}

# Fixtures — export these when running bench export-fixtures
fixtures = [
    {
        "doctype": "Role",
        "filters": [["name", "in", ["PRO"]]]
    },
]
