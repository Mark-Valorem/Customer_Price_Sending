# Database Schema

**version: v1.0.0**

## Overview

The Customer Price Sheet Automation system uses a JSON-based database stored in `data/customer_database.json`. The database contains customer records with contact information, file paths for price sheets, verification data, and pricing details.

## Database Format

**File**: `data/customer_database.json`
**Format**: JSON
**Encoding**: UTF-8
**Size**: ~50-100 KB (for 10-20 customers)

## Root Schema

```json
{
  "version": "string",              // Database version (semantic versioning)
  "created_date": "ISO 8601",       // Database creation timestamp
  "migrated_from": "string",        // Source of migration (e.g., "Python_CustomerPricing.xlsx")
  "verification_enabled": boolean,  // Whether verification is active
  "migration_stats": {...},         // Statistics from migration process
  "verification_errors": [...],     // Global verification errors
  "customers": [...]                // Array of customer objects
}
```

## Customer Object Schema

Each customer record in the `customers` array has the following structure:

### Core Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | Yes | Unique identifier (format: `{company_slug}_{date}`) |
| `company_name` | string | Yes | Official company name |
| `active` | boolean | Yes | Whether customer is active (default: true) |
| `created_date` | ISO 8601 | Yes | Record creation timestamp |
| `updated_at` | ISO 8601 | No | Last update timestamp |

### Contact Information

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `recipient_names` | array[string] | Yes | List of recipient names |
| `email_addresses` | array[string] | Yes | List of recipient email addresses |
| `email_domain` | string | Yes | Primary email domain (extracted from emails) |

**Note**: `recipient_names` and `email_addresses` arrays should have corresponding indices.

### File Generation

The `file_generation` object contains PDF file location and naming information:

```json
"file_generation": {
  "filename_pattern": "{month}_{file_body}",
  "file_body": "_Pricing_{CompanyName}.pdf",
  "file_path": "C:\\Users\\...\\CompanyName\\Pricing\\",
  "month_prefix": "250901",
  "current_filename": "250901_Pricing_{CompanyName}.pdf"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `filename_pattern` | string | Yes | Template for filename generation |
| `file_body` | string | Yes | Static part of filename |
| `file_path` | string | Yes | Full directory path to PDF files |
| `month_prefix` | string | Yes | Current month prefix (YYMMDD format) |
| `current_filename` | string | Yes | Fully resolved filename for current month |

**File Path Format**: Windows-style paths with escaped backslashes (`\\`)

### Pricing Details

Tracks pricing changes for the customer:

```json
"pricing_details": {
  "has_fx_change": boolean,
  "fx_direction": "up" | "down" | null,
  "has_price_change": boolean,
  "price_direction": "up" | "down" | null
}
```

| Field | Type | Description |
|-------|------|-------------|
| `has_fx_change` | boolean | Whether FX rate has changed |
| `fx_direction` | string\|null | Direction of FX change (up/down) |
| `has_price_change` | boolean | Whether prices have changed |
| `price_direction` | string\|null | Direction of price change (up/down) |

### Verification Status

Multi-layer verification tracking:

```json
"verification_status": {
  "domain_verified": boolean,
  "file_path_verified": boolean,
  "filename_verified": boolean,
  "recipients_verified": boolean,
  "file_paths_verified": boolean,
  "last_verification": "ISO 8601",
  "last_check": "ISO 8601"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `domain_verified` | boolean | Email domain DNS verification passed |
| `file_path_verified` | boolean | PDF file path exists |
| `filename_verified` | boolean | PDF filename matches pattern |
| `recipients_verified` | boolean | Recipients are authorized |
| `file_paths_verified` | boolean | All file paths accessible |
| `last_verification` | ISO 8601 | Timestamp of last full verification |
| `last_check` | ISO 8601 | Timestamp of most recent check |

### Metadata Fields

| Field | Type | Description |
|-------|------|-------------|
| `last_verified` | YYYY-MM-DD | Date string of last verification |
| `migration_source` | string | Source row/sheet from migration |
| `notes` | string | Human-readable notes |

## Complete Example Record

```json
{
  "id": "atlantic_performance_oils_20250916",
  "company_name": "Atlantic Performance Oils",
  "recipient_names": [
    "Arnie",
    "Steve",
    "Pares"
  ],
  "email_addresses": [
    "arnulfoc@atlanticoil.com",
    "steve@atlanticoil.com",
    "parest@atlanticoil.com"
  ],
  "email_domain": "atlanticoil.com",
  "file_generation": {
    "filename_pattern": "{month}_{file_body}",
    "file_body": "_Pricing_Atlantic Performance Oils.pdf",
    "file_path": "C:\\Users\\MarkAnderson\\Valorem\\Customer Hub - Documents\\Atlantic Performance Oils\\Pricing\\",
    "month_prefix": "250901",
    "current_filename": "250901_Pricing_Atlantic Performance Oils.pdf"
  },
  "pricing_details": {
    "has_fx_change": true,
    "fx_direction": null,
    "has_price_change": true,
    "price_direction": null
  },
  "verification_status": {
    "domain_verified": true,
    "file_path_verified": true,
    "filename_verified": true,
    "recipients_verified": true,
    "file_paths_verified": true,
    "last_verification": "2025-09-16T15:28:34.438915",
    "last_check": "2025-10-22T19:11:20.841450"
  },
  "active": true,
  "last_verified": "2025-10-22",
  "created_date": "2025-09-16T15:28:34.438919",
  "updated_at": "2025-10-23T09:18:00.320084",
  "migration_source": "Excel row 0",
  "notes": "Migrated from Excel CustomerDetails worksheet on 2025-09-16"
}
```

## Data Validation Rules

### Email Validation
- Must be valid email format: `user@domain.com`
- Domain must have MX records (verified during verification)
- Multiple emails allowed per customer

### File Path Validation
- Must be absolute Windows path
- Directory must exist and be accessible
- PDF file must exist at specified path
- Month prefix format: `YYMMDD` (e.g., "250901" = September 1, 2025)

### ID Generation
- Format: `{company_slug}_{creation_date}`
- Company slug: lowercase, spaces replaced with underscores
- Date: `YYYYMMDD` format

### Company Name Rules
- Required field, cannot be empty
- Used for display and file naming
- Should match official company name

## Database Operations

### Read Operations
```python
# Load database
with open("data/customer_database.json", "r") as f:
    db = json.load(f)
    customers = db["customers"]
```

### Write Operations
```python
# Update database
db["updated_at"] = datetime.now().isoformat()
with open("data/customer_database.json", "w") as f:
    json.dump(db, f, indent=2)
```

### Query Operations
```python
# Find customer by ID
customer = next((c for c in db["customers"] if c["id"] == customer_id), None)

# Find active customers
active = [c for c in db["customers"] if c.get("active", True)]

# Find customers with verification errors
errors = [c for c in db["customers"]
          if not c["verification_status"]["domain_verified"]]
```

## Migration History

**Version 1.0.0**: Excel-based (Python_CustomerPricing.xlsx)
- Headers on row 4 (0-indexed row 3)
- Manual data entry
- No verification system

**Version 2.0.0**: JSON-based (Current)
- Automated migration from Excel
- Built-in verification system
- Structured schema with validation
- Timestamp tracking
- Metadata support

## Backup Strategy

1. **Pre-Migration Backups**: Original Excel file preserved
2. **Git Versioning**: Database excluded from git (contains sensitive data)
3. **Manual Backups**: Users should manually backup before bulk changes
4. **Recovery**: Can re-migrate from Excel if needed

## Security Considerations

1. **Data Privacy**: Database excluded from git via `.gitignore`
2. **Email Protection**: Real email addresses - handle with care
3. **File Paths**: Contain user paths - system-specific
4. **Access Control**: Desktop application - local access only

## Performance Characteristics

- **Read Speed**: < 1ms for full database (typical size)
- **Write Speed**: ~5-10ms for full database save
- **Search**: Linear O(n) - acceptable for 10-100 customers
- **Memory**: ~1-2 MB in memory (typical size)

## Future Enhancements

1. **SQLite Migration**: For larger customer base (100+)
2. **Indexed Search**: For faster queries
3. **Encryption**: For sensitive data at rest
4. **Cloud Sync**: Optional cloud backup
5. **Multi-User**: Locking mechanism for concurrent access

---

**Related Documentation:**
- [Architecture](architecture.md)
- [Database Changes SOP](../sops/database-changes.md)
- [Tech Stack](tech-stack.md)
