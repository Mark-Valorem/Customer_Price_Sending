# Update Documentation Command

**version: v1.0.0**

This command automates the maintenance of the .agent documentation system.

## Description

The `/update-doc` command helps maintain documentation hygiene by:
- Updating documentation versions
- Creating task records for completed features
- Generating SOPs for new processes
- Archiving outdated files
- Committing and pushing changes to git

## Usage

### Update After Feature Implementation

```
/update-doc
```

**What it does:**
1. Reviews recent conversation for completed work
2. If implementation plan exists, saves to `.agent/tasks/[feature-name].md`
3. Identifies repeatable processes, creates/updates SOPs in `.agent/sops/`
4. Updates `.agent/README.md` and increments version
5. Archives unused/deprecated files to `Archive/`
6. Commits and pushes changes to GitHub

**Example workflow:**
```
User: "I just added email validation feature"
Assistant: [performs /update-doc]
- Creates .agent/tasks/email-validation.md
- Updates .agent/README.md (increments version)
- Commits: "docs: update documentation system to v1.1.0"
- Pushes to origin/main
```

### Generate Specific SOP

```
/update-doc generate SOP for [process name]
```

**What it does:**
1. Creates SOP document in `.agent/sops/[process-name].md`
2. Includes step-by-step instructions, examples, and pitfalls
3. Updates `.agent/README.md` index
4. Increments README version
5. Archives any deprecated docs
6. Commits and pushes changes

**Example:**
```
/update-doc generate SOP for troubleshooting Outlook errors
```

Creates: `.agent/sops/troubleshooting-outlook-errors.md`

## Automation Details

### Task Documentation Structure

When creating task records in `.agent/tasks/`:

```markdown
# Task: [Feature Name]

**Completed**: YYYY-MM-DD
**Version**: X.Y.Z
**Related Issues**: #123

## Summary
Brief description of what was implemented

## Implementation Details
- Key changes made
- Files modified
- New dependencies added

## Technical Decisions
- Why certain approaches were chosen
- Alternatives considered
- Trade-offs made

## Challenges Encountered
- Problems faced during implementation
- How they were resolved

## Testing
- Test coverage added
- Manual testing performed

## Documentation Updates
- Files updated
- New documentation created

## Lessons Learned
- What went well
- What could be improved
- Best practices identified
```

### SOP Document Structure

When generating SOPs in `.agent/sops/`:

```markdown
# SOP: [Process Name]

**version: v1.0.0**

## When to Use
Describe when this SOP applies

## Prerequisites
What needs to be in place before starting

## Step-by-Step Process

### 1. First Step
Instructions...

### 2. Second Step
Instructions...

## Common Pitfalls

### Problem 1
**Symptom**: What you'll see
**Solution**: How to fix it

## Quick Reference
Summary of key commands/steps

---

**Related Documentation:**
- [Link to related docs]
```

### Version Increment Rules

Documentation versions follow semantic versioning:

**README.md and Documentation Index:**
- **MAJOR (v1.0.0 → v2.0.0)**: Complete restructure or major content overhaul
- **MINOR (v1.0.0 → v1.1.0)**: New documents added (tasks, SOPs)
- **PATCH (v1.0.0 → v1.0.1)**: Updates to existing docs, corrections

**Individual Documents:**
- Update version when content changes significantly
- Add changelog section for major updates

### Git Commit Format

```bash
git commit -m "docs: update documentation system to v${version}

- Add task documentation for [feature]
- Create SOP for [process]
- Update .agent/README.md index
- Archive deprecated files

[Optional: Additional details]"
```

### Archive Strategy

Files to consider archiving:
- Deprecated scripts (moved to `Archive/legacy_*/`)
- Old test files (moved to `Archive/development_tests/`)
- Outdated documentation (moved to `Archive/documentation/`)
- Unused utilities
- Old version backups

**Archive structure:**
```
Archive/
├── legacy_cli_scripts/       # Old CLI versions
├── legacy_dashboards/        # Old GUI versions
├── legacy_launchers/         # Outdated launchers
├── development_tests/        # Dev-phase test files
├── unused_web_interface/     # Placeholder files
├── documentation/            # Old docs
├── generated_files/          # Build artifacts
└── v{version}_backup/        # Version snapshots
```

## Rules for AI Agents

When using this command, Claude Code should:

1. **Always read recent context** - Review last 10-20 messages to understand what was implemented

2. **Be selective** - Not every change needs a task document. Create tasks for:
   - New features (substantial additions)
   - Major bug fixes
   - Architecture changes
   - Complex implementations

3. **Identify patterns** - If you solved a problem that might recur, create an SOP

4. **Update existing docs** - Don't always create new files, update existing when appropriate

5. **Maintain cross-references** - Link related documentation

6. **Archive thoughtfully** - Only archive truly unused files, not temporarily inactive ones

7. **Commit atomically** - One commit per documentation update cycle

8. **Push automatically** - Always push after committing (unless explicitly told not to)

## Example Invocations

### After Implementing New Feature

```
User: The bulk email validation feature is complete. Update the docs.
Assistant: I'll update the documentation system.

[Creates .agent/tasks/bulk-email-validation.md]
[Updates .agent/README.md with new task link]
[Increments version v1.0.0 → v1.1.0]
[Commits: "docs: update documentation system to v1.1.0"]
[Pushes to origin/main]

✓ Documentation updated:
  - Created task record: bulk-email-validation.md
  - Updated README index
  - Version: v1.0.0 → v1.1.0
  - Committed and pushed to GitHub
```

### Generating New SOP

```
User: /update-doc generate SOP for resolving merge conflicts

[Creates .agent/sops/resolving-merge-conflicts.md]
[Updates .agent/README.md index]
[Increments version v1.1.0 → v1.2.0]
[Commits and pushes]

✓ SOP created:
  - File: .agent/sops/resolving-merge-conflicts.md
  - Added to README index
  - Version: v1.1.0 → v1.2.0
```

## Manual Override

Users can skip automation with flags:

```
/update-doc --no-commit     # Create docs but don't commit
/update-doc --no-push       # Commit but don't push
/update-doc --dry-run       # Show what would be done
```

## Integration with Development Workflow

**Recommended workflow:**

1. Plan feature → Read `.agent/README.md` and relevant SOPs
2. Implement feature → Follow SOPs, refer to system docs
3. Test feature → Use `running-tests.md` SOP
4. Complete feature → Run `/update-doc` to create task record
5. Encounter new pattern → Run `/update-doc generate SOP for [pattern]`

## Maintenance Schedule

**Weekly:**
- Review task documents for completeness
- Check for outdated SOPs
- Archive unused files

**Monthly:**
- Review all documentation for accuracy
- Update version numbers where needed
- Clean up Archive/ structure

**Quarterly:**
- Major documentation review
- Consider MAJOR version bump if significant changes
- Generate summary of documentation changes

---

**Related Documentation:**
- [.agent/README.md](../.agent/README.md) - Documentation index
- [Adding Features SOP](../.agent/sops/adding-feature.md)
- [Database Changes SOP](../.agent/sops/database-changes.md)
