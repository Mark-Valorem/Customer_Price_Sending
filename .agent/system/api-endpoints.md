# API & Interface Documentation

**version: v1.0.0**

## Overview

The Customer Price Sheet Automation system is a desktop application with **no REST API**. Instead, it provides:
1. **Internal Python module interfaces** for programmatic access
2. **Microsoft Outlook COM interfaces** for email automation
3. **GUI event interfaces** for user interactions

This document details all available interfaces for extending or integrating with the system.

## Internal Module APIs

### email_generator Module

Located: `src/email_generator.py`

#### generate_single_draft()

Creates a single email draft for one customer.

**Signature:**
```python
def generate_single_draft(
    customer: dict,
    template: str,
    signature_html: str,
    sender_name: str,
    month: str,
    year: str
) -> dict
```

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `customer` | dict | Customer record from database |
| `template` | str | Email body template with placeholders |
| `signature_html` | str | HTML signature for sender |
| `sender_name` | str | Name of sender (for From field) |
| `month` | str | Target month for email (e.g., "September") |
| `year` | str | Target year for email (e.g., "2025") |

**Returns:**
```python
{
    "success": True/False,
    "customer": "Company Name",
    "error": "Error message" (if success=False),
    "draft_created": True/False
}
```

**Example Usage:**
```python
from src import email_generator

customer = {
    "company_name": "ACME Corp",
    "email_addresses": ["john@acme.com"],
    "file_generation": {
        "file_path": "C:\\...",
        "current_filename": "251001_Pricing_ACME.pdf"
    }
}

result = email_generator.generate_single_draft(
    customer=customer,
    template="Dear {{company_name}},\n\nYour monthly pricing...",
    signature_html="<p>Best regards,<br>Jason</p>",
    sender_name="Jason Najm",
    month="October",
    year="2025"
)

if result["success"]:
    print(f"Draft created for {result['customer']}")
else:
    print(f"Error: {result['error']}")
```

#### generate_all_drafts()

Creates drafts for multiple customers.

**Signature:**
```python
def generate_all_drafts(
    customers: list[dict],
    template: str,
    signature_html: str,
    sender_name: str,
    month: str,
    year: str
) -> dict
```

**Parameters:**
Same as `generate_single_draft()` but `customers` is a list.

**Returns:**
```python
{
    "total": 10,
    "successful": 9,
    "failed": 1,
    "results": [
        {"success": True, "customer": "Company A", ...},
        {"success": False, "customer": "Company B", "error": "..."},
        ...
    ]
}
```

### verification_system Module

Located: `src/verification_system.py`

#### MultiLayerVerificationSystem

Main verification class for customer data validation.

**Initialization:**
```python
from src.verification_system import MultiLayerVerificationSystem

verifier = MultiLayerVerificationSystem(database_file="data/customer_database.json")
```

**Methods:**

##### verify_single_customer()

```python
def verify_single_customer(customer: dict) -> dict
```

**Parameters:**
- `customer`: Customer record dictionary

**Returns:**
```python
{
    "customer_id": "atlantic_oils_20250916",
    "company_name": "Atlantic Oils",
    "domain_check": {
        "passed": True,
        "domain": "atlanticoil.com",
        "message": "Domain verified"
    },
    "file_check": {
        "passed": True,
        "file_path": "C:\\...",
        "message": "File exists"
    },
    "recipient_check": {
        "passed": True,
        "recipients": ["Arnie", "Steve"],
        "message": "All recipients authorized"
    },
    "overall_status": "PASS" | "WARN" | "FAIL"
}
```

##### verify_all_customers()

```python
def verify_all_customers() -> list[dict]
```

**Returns:** List of verification results for all customers.

#### CustomerDatabase

Database access class.

**Initialization:**
```python
from src.verification_system import CustomerDatabase

db = CustomerDatabase(database_file="data/customer_database.json")
```

**Methods:**

##### load_database()
```python
def load_database() -> dict
```
Returns full database dictionary.

##### get_all_customers()
```python
def get_all_customers() -> list[dict]
```
Returns list of customer records.

##### get_customer_by_id()
```python
def get_customer_by_id(customer_id: str) -> dict | None
```
Returns single customer or None.

##### save_database()
```python
def save_database(db: dict) -> bool
```
Saves database to disk. Returns success status.

### audit_logging Module

Located: `src/audit_logging.py`

#### log_event()

```python
def log_event(
    event_type: str,
    customer: str,
    status: str,
    details: dict = None
) -> None
```

**Parameters:**
- `event_type`: "draft_created", "verification", "error"
- `customer`: Company name
- `status`: "success", "failure", "warning"
- `details`: Additional event data

**Example:**
```python
from src.audit_logging import log_event

log_event(
    event_type="draft_created",
    customer="ACME Corp",
    status="success",
    details={"email_count": 3, "attachment": "pricing.pdf"}
)
```

## Microsoft Outlook COM Interface

### COM Object Hierarchy

```
Outlook.Application
    └── CreateItem(0)  → MailItem
            ├── Subject: str
            ├── Body: str
            ├── HTMLBody: str
            ├── To: str
            ├── CC: str
            ├── BCC: str
            ├── Attachments
            │   └── Add(filepath: str)
            └── Save()
```

### Creating Email Drafts

**Step-by-step COM workflow:**

```python
import win32com.client
import pythoncom

# 1. Initialize COM
pythoncom.CoInitialize()

try:
    # 2. Get Outlook application
    outlook = win32com.client.Dispatch("Outlook.Application")

    # 3. Create mail item
    mail = outlook.CreateItem(0)  # 0 = olMailItem

    # 4. Set properties
    mail.Subject = "Monthly Price Sheet - October 2025"
    mail.To = "john@acme.com; jane@acme.com"
    mail.CC = "support@valorem.com.au; jasonn@valorem.com.au"
    mail.HTMLBody = "<html><body><p>Dear ACME Corp,</p>...</body></html>"

    # 5. Add attachments
    mail.Attachments.Add("C:\\path\\to\\pricing.pdf")

    # 6. Save as draft (DO NOT SEND)
    mail.Save()

    print("Draft created successfully")

except Exception as e:
    print(f"Error: {e}")

finally:
    # 7. Uninitialize COM
    pythoncom.CoUninitialize()
```

### COM Constants

```python
# Item types
olMailItem = 0
olAppointmentItem = 1
olContactItem = 2
olTaskItem = 3

# Importance
olImportanceLow = 0
olImportanceNormal = 1
olImportanceHigh = 2

# Sensitivity
olNormal = 0
olPersonal = 1
olPrivate = 2
olConfidential = 3
```

## GUI Event Interface

### tkinter Event Handlers

The dashboard uses tkinter event bindings:

```python
# Button click
button = ttk.Button(root, text="Generate", command=on_generate_click)

def on_generate_click():
    # Handle button click
    pass

# Treeview selection
tree.bind("<<TreeviewSelect>>", on_customer_select)

def on_customer_select(event):
    selected = tree.selection()
    # Handle selection
    pass

# Text editor changes
editor.bind("<<Modified>>", on_text_changed)

def on_text_changed(event):
    # Handle text modification
    pass
```

### Custom Events

Dashboard fires custom events for integration:

| Event | Trigger | Data |
|-------|---------|------|
| `<<DraftGenerated>>` | Email draft created | Customer ID |
| `<<VerificationComplete>>` | Verification finished | Results dict |
| `<<CustomerSelected>>` | Customer clicked | Customer object |
| `<<TemplateChanged>>` | Template edited | Template text |

## File System Interface

### JSON Database Access

**Direct file access (not recommended):**
```python
import json

# Read
with open("data/customer_database.json", "r") as f:
    db = json.load(f)

# Write
with open("data/customer_database.json", "w") as f:
    json.dump(db, f, indent=2)
```

**Recommended (via CustomerDatabase class):**
```python
from src.verification_system import CustomerDatabase

db = CustomerDatabase("data/customer_database.json")
customers = db.get_all_customers()
```

### Email Templates

**Location:** `email_templates.json`

**Structure:**
```json
{
  "templates": {
    "default": "Email body with {{placeholders}}",
    "price_increase": "..."
  },
  "signature": {
    "jason_najm": "<html>...",
    "mark_anderson": "<html>..."
  },
  "default_values": {
    "company_name": "Customer",
    "month": "Current Month"
  }
}
```

## Extension Points

### Adding New Verification Layers

Extend `MultiLayerVerificationSystem`:

```python
class CustomVerificationSystem(MultiLayerVerificationSystem):
    def verify_custom_check(self, customer):
        # Custom verification logic
        return {
            "passed": True/False,
            "message": "Check result"
        }
```

### Adding New Email Templates

Add to `email_templates.json`:

```json
{
  "templates": {
    "custom_template": "Your custom email body with {{variables}}"
  }
}
```

### Custom Logging

Extend audit logging:

```python
from src.audit_logging import log_event

log_event(
    event_type="custom_event",
    customer="Customer Name",
    status="success",
    details={"custom_field": "value"}
)
```

## Error Handling

All public functions return structured error information:

```python
try:
    result = email_generator.generate_single_draft(...)
    if not result["success"]:
        print(f"Error: {result['error']}")
        # Handle error
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle exception
```

## Thread Safety

**Important:** Outlook COM automation is **NOT thread-safe**. All COM operations must run on the same thread:

```python
# ❌ WRONG - will fail
import threading

def create_draft():
    outlook = win32com.client.Dispatch("Outlook.Application")
    # This will fail in new thread

thread = threading.Thread(target=create_draft)
thread.start()

# ✅ CORRECT - run in main thread
pythoncom.CoInitialize()
outlook = win32com.client.Dispatch("Outlook.Application")
# COM operations here
pythoncom.CoUninitialize()
```

## Rate Limiting

No built-in rate limiting. For bulk operations:

```python
import time

for customer in customers:
    result = email_generator.generate_single_draft(...)
    time.sleep(0.5)  # Add delay between drafts
```

---

**Related Documentation:**
- [Architecture](architecture.md)
- [Tech Stack](tech-stack.md)
- [Adding Features SOP](../sops/adding-feature.md)
