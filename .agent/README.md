# .agent Documentation Index

**version: v1.0.0**

## Purpose

This directory contains AI-optimized documentation for the Customer Price Sheet Automation system. The documentation is structured to provide efficient context management for AI agents (Claude Code, GitHub Copilot, etc.) while maintaining comprehensive technical reference for human developers.

## Documentation Structure

```
.agent/
├── README.md           # This file - documentation index
├── tasks/             # Feature implementation plans and task records
├── system/            # System architecture and technical documentation
│   ├── architecture.md       # System architecture overview
│   ├── database-schema.md    # Database structure and schema
│   ├── tech-stack.md        # Technology stack details
│   └── api-endpoints.md     # API/Interface documentation
└── sops/              # Standard Operating Procedures
    ├── adding-feature.md     # How to add new features
    ├── running-tests.md      # Testing procedures
    ├── database-changes.md   # Database modification workflow
    └── deployment.md         # Deployment and distribution
```

## Quick Reference

### System Documentation
- **[Architecture](system/architecture.md)**: GUI dashboard, backend modules, data flow
- **[Database Schema](system/database-schema.md)**: JSON database structure and fields
- **[Tech Stack](system/tech-stack.md)**: Python, tkinter, pywin32, Outlook COM
- **[API/Interfaces](system/api-endpoints.md)**: COM interfaces and module APIs

### Standard Operating Procedures
- **[Adding Features](sops/adding-feature.md)**: Step-by-step feature development workflow
- **[Running Tests](sops/running-tests.md)**: pytest, Playwright, manual testing
- **[Database Changes](sops/database-changes.md)**: Modifying customer database safely
- **[Deployment](sops/deployment.md)**: Desktop application distribution

### Task Records
The `tasks/` folder contains records of completed feature implementations and ongoing work. Each task document includes:
- Implementation plan
- Technical decisions made
- Challenges encountered
- Solutions applied

## Usage Guidelines

### For AI Agents
1. **Always read this README first** when starting a new task or session
2. **Reference system docs** before proposing architectural changes
3. **Follow SOPs** when implementing features or making changes
4. **Update task docs** after completing significant work
5. **Generate new SOPs** when establishing new patterns or fixing repeated mistakes

### For Developers
1. **Start here** to understand project structure
2. **Reference SOPs** for standard workflows
3. **Update docs** when adding features or changing architecture
4. **Version all changes** using semantic versioning
5. **Use `/update-doc` command** to automate documentation maintenance

## Version Management

All documentation files include version tracking:
- **Semantic versioning**: v1.0.0 format (MAJOR.MINOR.PATCH)
- **Increment rules**:
  - MAJOR: Breaking changes or complete rewrites
  - MINOR: New sections or significant additions
  - PATCH: Corrections, clarifications, minor updates

## Automation Commands

- **`/update-doc`**: Update documentation after implementing features
- **`/update-doc generate SOP for [process]`**: Create new SOP document

See [.claude/commands/update-doc.md](../.claude/commands/update-doc.md) for details.

---

**Last Updated**: 2025-10-26
**Total Documents**: 9 files (1 index + 4 system + 4 SOPs)
**Maintained By**: Claude Code v4.0.0
