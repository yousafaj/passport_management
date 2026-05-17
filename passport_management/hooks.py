app_name = "passport_management"
app_title = "Passport Management"
app_publisher = "Your Organization"
app_description = "Centralized passport movement and tracking for ERPNext"
app_email = "admin@yourorg.com"
app_license = "MIT"

# App icon shown in the Desk
app_logo_url = "/assets/passport_management/images/passport_logo.svg"

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
        "doctype": "Custom Field",
        "filters": [["dt", "=", "Employee"], ["fieldname", "=", "passport_number"]]
    },
    {
        "doctype": "Role",
        "filters": [["name", "in", ["PRO"]]]
    },
]
