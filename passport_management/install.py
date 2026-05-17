"""Installation hooks — ensure custom fields the app depends on exist.

Called from hooks.py on after_install (first install) and after_migrate
(every bench migrate). Idempotent: create_custom_fields skips fields
that already exist.
"""

from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


EMPLOYEE_CUSTOM_FIELDS = {
    "Employee": [
        {
            "fieldname": "passport_expiry_date",
            "label": "Passport Expiry Date",
            "fieldtype": "Date",
            "insert_after": "passport_number",
            "description": "Used by Passport Management to send expiry reminders.",
        },
    ],
}


def after_install():
    create_custom_fields(EMPLOYEE_CUSTOM_FIELDS, ignore_validate=True)


def after_migrate():
    create_custom_fields(EMPLOYEE_CUSTOM_FIELDS, ignore_validate=True)
