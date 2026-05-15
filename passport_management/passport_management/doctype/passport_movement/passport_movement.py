import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today, getdate


class PassportMovement(Document):

    # ── Lifecycle hooks ───────────────────────────────────────────────────────

    def validate(self):
        self._set_defaults()
        self._sync_naming_series()
        self._validate_no_duplicate_active_in()
        self._validate_out_requires_active_in()
        self._validate_return_dates()

    def on_submit(self):
        if self.movement_type == "In":
            frappe.db.set_value("Passport Movement", self.name, "is_active_record", 1)
            self.is_active_record = 1
        elif self.movement_type == "Out":
            self._deactivate_corresponding_in_record()
            frappe.db.set_value("Passport Movement", self.name, "actual_return_date", today())
            self.actual_return_date = today()

    def on_cancel(self):
        if self.movement_type == "In":
            frappe.db.set_value("Passport Movement", self.name, "is_active_record", 0)
            self.is_active_record = 0
        elif self.movement_type == "Out":
            self._reactivate_in_record()

    # ── Private helpers ───────────────────────────────────────────────────────

    def _set_defaults(self):
        if not self.transaction_date:
            self.transaction_date = today()
        if not self.received_by:
            self.received_by = frappe.session.user

    def _sync_naming_series(self):
        """Keep naming_series aligned with movement_type for Document Naming Rules."""
        series_map = {"In": "PM-IN-.YYYY.-.#####", "Out": "PM-OUT-.YYYY.-.#####"}
        if self.movement_type in series_map:
            self.naming_series = series_map[self.movement_type]

    def _validate_no_duplicate_active_in(self):
        """Prevent a second active IN record for the same employee."""
        if self.movement_type != "In":
            return
        existing = frappe.db.get_value(
            "Passport Movement",
            {
                "employee": self.employee,
                "movement_type": "In",
                "is_active_record": 1,
                "docstatus": 1,
                "name": ["!=", self.name],
            },
            "name",
        )
        if existing:
            frappe.throw(
                _(
                    "An active Passport IN record {0} already exists for {1}. "
                    "Please process an OUT movement before creating a new IN record."
                ).format(frappe.bold(existing), frappe.bold(self.employee_name)),
                title=_("Duplicate Active Record"),
            )

    def _validate_out_requires_active_in(self):
        """An OUT can only be created when an active IN record exists."""
        if self.movement_type != "Out":
            return
        active_in = frappe.db.get_value(
            "Passport Movement",
            {
                "employee": self.employee,
                "movement_type": "In",
                "is_active_record": 1,
                "docstatus": 1,
            },
            "name",
        )
        if not active_in:
            frappe.throw(
                _(
                    "No active Passport IN record found for {0}. "
                    "Cannot create an OUT movement without a prior submitted IN record."
                ).format(frappe.bold(self.employee_name)),
                title=_("Missing IN Record"),
            )

    def _validate_return_dates(self):
        if self.expected_return_date and getdate(self.expected_return_date) < getdate(
            self.transaction_date
        ):
            frappe.throw(
                _("Expected Return Date cannot be before Transaction Date."),
                title=_("Invalid Date"),
            )
        if (
            self.actual_return_date
            and self.transaction_date
            and getdate(self.actual_return_date) < getdate(self.transaction_date)
        ):
            frappe.throw(
                _("Actual Return Date cannot be before Transaction Date."),
                title=_("Invalid Date"),
            )

    def _deactivate_corresponding_in_record(self):
        """Mark the employee's active IN record as inactive when OUT is submitted."""
        active_in = frappe.db.get_value(
            "Passport Movement",
            {
                "employee": self.employee,
                "movement_type": "In",
                "is_active_record": 1,
                "docstatus": 1,
            },
            "name",
        )
        if active_in:
            frappe.db.set_value("Passport Movement", active_in, "is_active_record", 0)

    def _reactivate_in_record(self):
        """When an OUT is cancelled, restore the most recent IN record as active."""
        in_record = frappe.db.sql(
            """
            SELECT name FROM `tabPassport Movement`
            WHERE employee = %(employee)s
              AND movement_type = 'In'
              AND is_active_record = 0
              AND docstatus = 1
            ORDER BY transaction_date DESC
            LIMIT 1
            """,
            {"employee": self.employee},
            as_dict=True,
        )
        if in_record:
            frappe.db.set_value(
                "Passport Movement", in_record[0].name, "is_active_record", 1
            )


# ── Whitelisted API endpoints ─────────────────────────────────────────────────

@frappe.whitelist()
def get_active_in_record(employee):
    """Return the active IN record for an employee (used by client script)."""
    return frappe.db.get_value(
        "Passport Movement",
        {"employee": employee, "movement_type": "In", "is_active_record": 1, "docstatus": 1},
        ["name", "transaction_date", "passport_number"],
        as_dict=True,
    )


# ── Standalone event handlers (called from hooks.py doc_events) ───────────────

def validate(doc, method=None):
    doc.validate()


def on_submit(doc, method=None):
    doc.on_submit()


def on_cancel(doc, method=None):
    doc.on_cancel()
