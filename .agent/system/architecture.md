# System Architecture

**version: v1.0.0**

## Overview

The Customer Price Sheet Automation system is a desktop Windows application built with Python that automates the creation of Outlook email drafts with customer-specific price sheet attachments. The system uses a GUI dashboard for user interaction and integrates with Microsoft Outlook via COM automation.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   GUI Layer (tkinter)                       │
│  ┌──────────────┐  ┌───────────────┐  ┌─────────────────┐ │
│  │ Email Draft  │  │   Customer    │  │    Settings     │ │
│  │     Tab      │  │  Management   │  │      Tab        │ │
│  └──────────────┘  └───────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                      │
│  ┌────────────────────┐  ┌──────────────────────────────┐  │
│  │ email_generator.py │  │ verification_system.py       │  │
│  │ - Draft creation   │  │ - Email validation          │  │
│  │ - Template merge   │  │ - File path verification    │  │
│  │ - COM interaction  │  │ - Recipient authorization   │  │
│  └────────────────────┘  └──────────────────────────────┘  │
│  ┌────────────────────┐                                    │
│  │ audit_logging.py   │                                    │
│  │ - Event tracking   │                                    │
│  │ - Error logging    │                                    │
│  └────────────────────┘                                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                              │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  │
│  │ customer_database.json  │  │ email_templates.json    │  │
│  │ - Customer records      │  │ - Email templates       │  │
│  │ - Contact information   │  │ - Signatures           │  │
│  │ - File paths           │  │ - Default values        │  │
│  └─────────────────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 External Integration Layer                  │
│  ┌──────────────────────┐  ┌──────────────────────────┐    │
│  │ Microsoft Outlook    │  │ File System             │    │
│  │ (COM Automation)     │  │ - PDF attachments       │    │
│  │ - Draft creation     │  │ - HTML signatures       │    │
│  │ - Email sending API  │  │ - Log files            │    │
│  └──────────────────────┘  └──────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. GUI Dashboard (`dashboard.py`)

The main application interface built with tkinter.

**Key Features:**
- Three-tab interface: Email Generation, Customer Management, Settings
- Real-time email preview with live signature integration
- 50/50 split layout for customer management and verification console
- User selection dropdown (Jason Najm / Mark Anderson)
- Debug mode toggle for troubleshooting
- Company logo branding

**Architecture Pattern**: MVC-inspired
- View: tkinter widgets and layout
- Controller: Event handlers and UI logic
- Model: Data access via backend modules

**Key Classes:**
- `CustomerManagementPanel`: Customer CRUD operations with verification
- `EmailDraftTab`: Template editor and email generation
- `SettingsTab`: Application configuration

### 2. Backend Modules (`src/`)

#### email_generator.py
**Purpose**: Core email draft generation logic

**Key Functions:**
- `generate_single_draft()`: Creates individual Outlook draft
- `generate_all_drafts()`: Batch processing for multiple customers
- Template variable replacement
- PDF attachment handling
- HTML signature injection

**COM Interaction:**
```python
outlook = win32com.client.Dispatch("Outlook.Application")
mail = outlook.CreateItem(0)  # 0 = MailItem
# Configure and save as draft
```

#### verification_system.py
**Purpose**: Multi-layer customer data verification

**Verification Layers:**
1. **Domain Verification**: Validates email domain existence
2. **File Path Verification**: Confirms PDF files exist at specified paths
3. **Recipient Authorization**: Checks authorized recipients list

**Key Classes:**
- `MultiLayerVerificationSystem`: Orchestrates verification process
- `CustomerDatabase`: Manages customer data access

#### audit_logging.py
**Purpose**: Event tracking and error logging

**Logged Events:**
- Email draft creation (success/failure)
- Verification results
- System errors and warnings
- User actions

## Data Flow

### Email Draft Creation Flow

```
1. User selects email template and customizes content
   ↓
2. User selects sender (Jason/Mark) - signature auto-loaded
   ↓
3. User clicks "Generate Drafts"
   ↓
4. Dashboard calls email_generator.generate_all_drafts()
   ↓
5. For each customer in database:
   a. Load customer record from customer_database.json
   b. Replace template variables ({{company_name}}, etc.)
   c. Inject sender's HTML signature
   d. Find PDF file (YYMMDD_*.pdf pattern)
   e. Create Outlook draft via COM
   f. Attach PDF file
   g. Set recipients, CC, subject
   h. Save as draft (DO NOT send)
   i. Log result to audit log
   ↓
6. Display summary: X drafts created, Y failed
   ↓
7. User reviews drafts in Outlook before sending
```

### Customer Verification Flow

```
1. User clicks "Verify All" in Customer Management tab
   ↓
2. verification_system.MultiLayerVerificationSystem initialized
   ↓
3. For each customer in database:
   ↓
   Layer 1: Email Domain Verification
   - Extract domain from email addresses
   - Check DNS MX records
   - Result: Valid / Invalid domain
   ↓
   Layer 2: File Path Verification
   - Build file path from file_generation field
   - Check if PDF file exists
   - Result: File found / File not found
   ↓
   Layer 3: Recipient Authorization
   - Check recipient_names against authorized list
   - Result: Authorized / Unauthorized
   ↓
4. Aggregate results and display in console:
   - Green: All checks passed
   - Yellow: Warnings (non-critical)
   - Red: Errors (critical failures)
   ↓
5. Display summary statistics
```

## Module Interaction Diagram

```
dashboard.py
    │
    ├─► src.email_generator
    │       │
    │       ├─► win32com.client (Outlook COM)
    │       ├─► customer_database.json (read)
    │       ├─► email_templates.json (read)
    │       └─► PDF files (attach)
    │
    ├─► src.verification_system
    │       │
    │       ├─► customer_database.json (read)
    │       └─► DNS resolution (validate)
    │
    └─► src.audit_logging
            │
            └─► logs/audit_log.json (write)
```

## Design Patterns

### 1. Factory Pattern
Used in Outlook COM object creation:
```python
outlook = win32com.client.Dispatch("Outlook.Application")
mail = outlook.CreateItem(0)
```

### 2. Template Method Pattern
Email generation follows template method:
1. Load template
2. Replace variables
3. Inject signature
4. Attach files
5. Create draft

### 3. Observer Pattern
GUI uses event-driven architecture with tkinter callbacks

### 4. Singleton Pattern
Logging system maintains single instance for consistency

## Security Considerations

1. **No Automatic Sending**: Drafts are created but never sent automatically
2. **Data Privacy**: Customer data excluded from git via .gitignore
3. **Input Validation**: All email addresses and file paths validated
4. **Error Handling**: Comprehensive try-catch with logging
5. **Audit Trail**: All actions logged for accountability

## Performance Characteristics

- **Startup Time**: 2-3 seconds (load GUI + initialize COM)
- **Draft Creation**: ~1-2 seconds per customer
- **Verification**: ~500ms per customer (network dependent)
- **Memory Usage**: ~50-100 MB (Python + tkinter + COM)

## Scalability Considerations

**Current Limits:**
- Customer database: ~100-200 customers (JSON-based)
- Concurrent processing: Sequential (one draft at a time)

**Future Enhancements:**
- SQLite database for larger customer base
- Async/threading for parallel draft creation
- Batch processing with progress resumption

## Error Handling Strategy

1. **User-Facing Errors**: Display in GUI with actionable messages
2. **Background Errors**: Log to file, continue processing
3. **Critical Errors**: Stop processing, display detailed error dialog
4. **Validation Errors**: Highlight in verification console with color coding

---

**Related Documentation:**
- [Database Schema](database-schema.md)
- [Tech Stack](tech-stack.md)
- [API Endpoints](api-endpoints.md)
