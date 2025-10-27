# SOP: Database Schema Changes

**version: v1.0.0**

## When to Use

Use this SOP whenever you need to:
- Add new fields to customer records
- Modify existing field structures
- Update database version
- Migrate data formats
- Add new root-level database properties
- Change validation rules

## Prerequisites

- Backup of current database
- Understanding of database schema (see [database-schema.md](../system/database-schema.md))
- Clear requirements for changes needed
- Test plan for validating changes

## Critical Safety Rules

1. **ALWAYS backup before changes**
2. **NEVER edit database directly in production without testing**
3. **NEVER delete fields without migration plan**
4. **ALWAYS test with real data**
5. **ALWAYS update documentation**

## Step-by-Step Process

### 1. Create Backup

**Before ANY database changes:**

```bash
# Create timestamped backup
cp data/customer_database.json data/customer_database.backup_$(date +%Y%m%d_%H%M%S).json

# Or Windows:
copy data\customer_database.json data\customer_database.backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.json
```

**Verify backup:**
```bash
# Check backup exists and is valid JSON
python -c "import json; json.load(open('data/customer_database.backup_YYYYMMDD.json'))"
```

### 2. Plan the Change

**Document the change:**

```markdown
## Database Change: Add Email Preferences Field

### Current Structure
```json
{
  "company_name": "ACME Corp",
  "email_addresses": ["john@acme.com"]
}
```

### Proposed Structure
```json
{
  "company_name": "ACME Corp",
  "email_addresses": ["john@acme.com"],
  "email_preferences": {
    "format": "html",
    "frequency": "monthly",
    "notify_on_price_change": true
  }
}
```

### Migration Strategy
- Add field to all existing customers with default values
- Update schema validation
- Update GUI to allow editing
```

### 3. Create Migration Script

**Create:** `scripts/migrate_add_email_preferences.py`

```python
"""
Migration: Add email_preferences field
Date: 2025-10-26
Version: 2.0.0 -> 2.1.0
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def migrate_database(db_path: str, backup_path: str = None):
    """
    Add email_preferences field to all customers
    """
    # Create backup
    if backup_path is None:
        backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    print(f"Creating backup: {backup_path}")
    with open(db_path, 'r') as f:
        db = json.load(f)

    with open(backup_path, 'w') as f:
        json.dump(db, f, indent=2)

    # Perform migration
    print("Starting migration...")
    migrated_count = 0

    for customer in db['customers']:
        if 'email_preferences' not in customer:
            customer['email_preferences'] = {
                "format": "html",
                "frequency": "monthly",
                "notify_on_price_change": True
            }
            migrated_count += 1

    # Update database version
    old_version = db.get('version', '1.0.0')
    db['version'] = '2.1.0'
    db['last_migration'] = datetime.now().isoformat()
    db['migration_history'] = db.get('migration_history', [])
    db['migration_history'].append({
        "from_version": old_version,
        "to_version": "2.1.0",
        "date": datetime.now().isoformat(),
        "description": "Add email_preferences field",
        "customers_affected": migrated_count
    })

    # Save migrated database
    print(f"Saving migrated database...")
    with open(db_path, 'w') as f:
        json.dump(db, f, indent=2)

    print(f"✓ Migration complete!")
    print(f"  - Customers migrated: {migrated_count}")
    print(f"  - Database version: {old_version} → 2.1.0")
    print(f"  - Backup saved to: {backup_path}")

    return True

if __name__ == "__main__":
    db_path = "data/customer_database.json"

    # Confirm before proceeding
    response = input(f"Migrate {db_path}? (yes/no): ")
    if response.lower() != 'yes':
        print("Migration cancelled")
        sys.exit(0)

    try:
        migrate_database(db_path)
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        print("Database not modified. Check backup if needed.")
        sys.exit(1)
```

### 4. Test Migration on Copy

**Create test copy:**
```bash
cp data/customer_database.json data/customer_database.test.json
```

**Run migration on test:**
```python
# Modify script to use test database
python scripts/migrate_add_email_preferences.py
# (modify script to use customer_database.test.json)
```

**Verify test results:**
```python
# Verify migration succeeded
python -c "
import json
with open('data/customer_database.test.json', 'r') as f:
    db = json.load(f)

# Check version updated
assert db['version'] == '2.1.0'

# Check all customers have new field
for customer in db['customers']:
    assert 'email_preferences' in customer
    print(f\"✓ {customer['company_name']} has email_preferences\")

print('✓ All checks passed')
"
```

### 5. Update Schema Documentation

**Update:** `.agent/system/database-schema.md`

```markdown
### Email Preferences (NEW in v2.1.0)

The `email_preferences` object contains email delivery preferences:

| Field | Type | Description |
|-------|------|-------------|
| `format` | string | Email format: "html" or "text" |
| `frequency` | string | Delivery frequency: "monthly", "quarterly" |
| `notify_on_price_change` | boolean | Send notification on price changes |
```

### 6. Update Code to Use New Field

**Update verification system:**
```python
# src/verification_system.py

def verify_customer(customer: dict) -> dict:
    # ... existing verification ...

    # Add validation for new field
    email_prefs = customer.get('email_preferences', {})
    if not isinstance(email_prefs, dict):
        warnings.append("Invalid email_preferences format")

    return result
```

**Update GUI:**
```python
# dashboard.py

def display_customer_details(customer):
    # ... existing display code ...

    # Show email preferences
    prefs = customer.get('email_preferences', {})
    format_label = ttk.Label(frame, text=f"Email Format: {prefs.get('format', 'N/A')}")
    format_label.pack()
```

### 7. Run Migration on Production Database

**Final checks:**
- [ ] Backup created and verified
- [ ] Migration tested on copy
- [ ] Code updated to handle new field
- [ ] Documentation updated
- [ ] Team notified (if applicable)

**Execute migration:**
```bash
python scripts/migrate_add_email_preferences.py
```

**Verify production migration:**
```python
python -c "
import json
with open('data/customer_database.json', 'r') as f:
    db = json.load(f)
    print(f'Version: {db[\"version\"]}')
    print(f'Customers: {len(db[\"customers\"])}')
    print(f'Last migration: {db.get(\"last_migration\", \"N/A\")}')

    # Spot check
    customer = db['customers'][0]
    print(f'Sample customer has email_preferences: {\"email_preferences\" in customer}')
"
```

### 8. Test Application

**Launch and test:**
```bash
python dashboard.py
```

**Verify:**
- [ ] Application launches without errors
- [ ] Customer data loads correctly
- [ ] New field visible in GUI (if applicable)
- [ ] Existing functionality works
- [ ] No validation errors

### 9. Commit Changes

```bash
# Stage all changes
git add data/customer_database.json \
        scripts/migrate_add_email_preferences.py \
        .agent/system/database-schema.md \
        src/verification_system.py \
        dashboard.py

# Commit with migration message
git commit -m "feat(database): add email_preferences field

- Create migration script for email_preferences
- Update database to version 2.1.0
- Update schema documentation
- Add GUI display for preferences
- Migrate all 11 customer records

Migration tested on copy before production.
Backup created: customer_database.backup_20251026.json"

# Push changes
git push origin main
```

## Common Database Changes

### Adding a Simple Field

```python
# Add field with default value
for customer in db['customers']:
    if 'new_field' not in customer:
        customer['new_field'] = "default_value"
```

### Renaming a Field

```python
# Rename field safely
for customer in db['customers']:
    if 'old_name' in customer:
        customer['new_name'] = customer.pop('old_name')
```

### Changing Field Type

```python
# Convert string to list
for customer in db['customers']:
    if isinstance(customer.get('recipient_names'), str):
        customer['recipient_names'] = [customer['recipient_names']]
```

### Removing a Field

```python
# Remove deprecated field
for customer in db['customers']:
    if 'deprecated_field' in customer:
        customer.pop('deprecated_field')
```

### Adding Nested Object

```python
# Add nested structure
for customer in db['customers']:
    if 'settings' not in customer:
        customer['settings'] = {
            "active": True,
            "priority": "normal"
        }
```

## Rollback Procedure

**If migration causes problems:**

### Option 1: Restore from Backup

```bash
# Stop application
# Restore backup
cp data/customer_database.backup_20251026.json data/customer_database.json

# Verify restoration
python -c "import json; json.load(open('data/customer_database.json'))"

# Restart application
python dashboard.py
```

### Option 2: Reverse Migration

Create reverse migration script:

```python
def rollback_migration(db_path: str):
    """Remove email_preferences field"""
    with open(db_path, 'r') as f:
        db = json.load(f)

    for customer in db['customers']:
        if 'email_preferences' in customer:
            customer.pop('email_preferences')

    db['version'] = '2.0.0'

    with open(db_path, 'w') as f:
        json.dump(db, f, indent=2)
```

## Data Validation

### Validate Database Structure

```python
def validate_database(db_path: str) -> bool:
    """Validate database structure and required fields"""
    with open(db_path, 'r') as f:
        db = json.load(f)

    # Check root structure
    required_root = ['version', 'customers']
    for field in required_root:
        assert field in db, f"Missing root field: {field}"

    # Check each customer
    required_customer = ['id', 'company_name', 'email_addresses']
    for i, customer in enumerate(db['customers']):
        for field in required_customer:
            assert field in customer, f"Customer {i} missing field: {field}"

    print("✓ Database validation passed")
    return True
```

### Run Validation

```bash
python -c "from scripts.validate_db import validate_database; validate_database('data/customer_database.json')"
```

## Version Management

Database versions should follow semantic versioning:

- **Major (2.0.0 → 3.0.0)**: Breaking changes, requires migration
- **Minor (2.0.0 → 2.1.0)**: New fields, backward compatible
- **Patch (2.1.0 → 2.1.1)**: Data fixes, no schema changes

**Update version in:**
1. Database `version` field
2. `database-schema.md` documentation
3. Migration script comments

## Common Pitfalls

### 1. Forgetting Backup
**Always create backup before ANY changes**

### 2. Not Testing on Copy
**Always test migration on copy first**

### 3. Breaking Existing Code
**Check all code that reads the modified fields**

### 4. Not Updating Documentation
**Update schema docs immediately after migration**

### 5. Partial Migration
**Ensure ALL customers are migrated, not just some**

## Quick Reference

**Pre-migration checklist:**
- [ ] Backup created
- [ ] Migration script written
- [ ] Tested on copy
- [ ] Code updated
- [ ] Documentation updated
- [ ] Validation tests pass

**Migration command:**
```bash
python scripts/migrate_<description>.py
```

**Rollback command:**
```bash
cp data/customer_database.backup_YYYYMMDD.json data/customer_database.json
```

---

**Related Documentation:**
- [Database Schema](../system/database-schema.md)
- [Architecture](../system/architecture.md)
- [Adding Features SOP](adding-feature.md)
