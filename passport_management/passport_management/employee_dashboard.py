"""Extend the Employee dashboard with a Passport Management section so
Passport Movement records appear under the Employee form's Connections
panel, linked via the `employee` field.

Wired via hooks.py -> override_doctype_dashboards.
"""

from frappe import _


def get_dashboard_data(data):
    transactions = data.setdefault("transactions", [])
    transactions.append({
        "label": _("Passport Management"),
        "items": ["Passport Movement"],
    })
    return data
