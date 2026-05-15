import frappe
from frappe.utils import today, add_days, formatdate


def send_overdue_passport_alerts():
    """Daily: notify HR and PRO about passports not returned past expected date."""
    overdue = frappe.db.sql(
        """
        SELECT name, employee, employee_name, passport_number,
               expected_return_date, department
        FROM `tabPassport Movement`
        WHERE movement_type = 'In'
          AND is_active_record = 1
          AND docstatus = 1
          AND expected_return_date IS NOT NULL
          AND expected_return_date < %(today)s
        ORDER BY expected_return_date ASC
        """,
        {"today": today()},
        as_dict=True,
    )

    if not overdue:
        return

    hr_managers = frappe.get_all(
        "Has Role", filters={"role": "HR Manager"}, fields=["parent"], pluck="parent"
    )
    pros = frappe.get_all(
        "Has Role", filters={"role": "PRO"}, fields=["parent"], pluck="parent"
    )
    recipients = list(set(hr_managers + pros))

    rows = "".join(
        f"<tr><td>{r.employee_name}</td><td>{r.passport_number}</td>"
        f"<td>{r.department}</td><td>{formatdate(r.expected_return_date)}</td>"
        f"<td><a href='/app/passport-movement/{r.name}'>{r.name}</a></td></tr>"
        for r in overdue
    )

    message = f"""
    <p>The following passports are overdue for return:</p>
    <table border="1" cellpadding="4" cellspacing="0">
      <thead>
        <tr>
          <th>Employee</th><th>Passport No.</th><th>Department</th>
          <th>Expected Return</th><th>Record</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
    """

    frappe.sendmail(
        recipients=recipients,
        subject=f"[Passport Management] {len(overdue)} Overdue Passport(s) — {formatdate(today())}",
        message=message,
        delayed=False,
    )


def send_expiry_reminders():
    """Daily: warn about passports expiring within 90 days."""
    alert_days = [90, 60, 30]
    for days in alert_days:
        target_date = add_days(today(), days)
        expiring = frappe.db.sql(
            """
            SELECT e.name AS employee, e.employee_name, e.passport_number,
                   e.passport_expiry_date, e.department
            FROM `tabEmployee` e
            WHERE e.passport_expiry_date = %(target)s
              AND e.status = 'Active'
            """,
            {"target": target_date},
            as_dict=True,
        )
        if not expiring:
            continue

        for emp in expiring:
            user_id = frappe.db.get_value("Employee", emp.employee, "user_id")
            if user_id:
                frappe.sendmail(
                    recipients=[user_id],
                    subject=f"Passport Expiry Reminder — {days} days remaining",
                    message=(
                        f"<p>Dear {emp.employee_name},</p>"
                        f"<p>Your passport <b>{emp.passport_number}</b> expires on "
                        f"<b>{formatdate(emp.passport_expiry_date)}</b> "
                        f"({days} days from today). Please initiate renewal.</p>"
                    ),
                    delayed=False,
                )
