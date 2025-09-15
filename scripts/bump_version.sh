#!/bin/bash

# Customer Price Sheet Automation - Version Bump Script
# This script automates the version bumping process using bump2version
# and pushes the changes and tags to the remote repository.

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 <bump_type> [options]"
    echo ""
    echo "Bump types:"
    echo "  patch     Increment patch version (0.1.0 -> 0.1.1)"
    echo "  minor     Increment minor version (0.1.0 -> 0.2.0)"
    echo "  major     Increment major version (0.1.0 -> 1.0.0)"
    echo ""
    echo "Options:"
    echo "  --dry-run     Show what would be done without making changes"
    echo "  --no-push    Don't push changes to remote repository"
    echo "  --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 patch                    # Bump patch version and push"
    echo "  $0 minor --dry-run          # See what minor bump would do"
    echo "  $0 major --no-push          # Bump major version but don't push"
}

# Parse command line arguments
BUMP_TYPE=""
DRY_RUN=false
NO_PUSH=false

while [[ $# -gt 0 ]]; do
    case $1 in
        patch|minor|major)
            BUMP_TYPE="$1"
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --no-push)
            NO_PUSH=true
            shift
            ;;
        --help|-h)
            show_usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Validate arguments
if [[ -z "$BUMP_TYPE" ]]; then
    print_error "Bump type is required"
    show_usage
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository"
    exit 1
fi

# Check if working directory is clean
if [[ -n $(git status --porcelain) ]]; then
    print_error "Working directory is not clean. Please commit or stash changes first."
    git status --short
    exit 1
fi

# Check if bump2version is installed
if ! command -v bump2version &> /dev/null; then
    print_error "bump2version is not installed. Install it with: pip install bump2version"
    exit 1
fi

# Get current version
CURRENT_VERSION=$(python -c "import configparser; c = configparser.ConfigParser(); c.read('.bumpversion.cfg'); print(c['bumpversion']['current_version'])")
print_status "Current version: $CURRENT_VERSION"

# Dry run mode
if [[ "$DRY_RUN" == true ]]; then
    print_warning "DRY RUN MODE - No changes will be made"
    bump2version --dry-run --verbose "$BUMP_TYPE"
    exit 0
fi

# Confirm the action
echo ""
print_warning "This will:"
echo "  1. Bump the $BUMP_TYPE version"
echo "  2. Update version in pyproject.toml and src/__init__.py"
echo "  3. Create a git commit with the version change"
echo "  4. Create a git tag for the new version"
if [[ "$NO_PUSH" != true ]]; then
    echo "  5. Push changes and tags to the remote repository"
fi
echo ""

read -p "Do you want to continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_status "Operation cancelled"
    exit 0
fi

# Perform the version bump
print_status "Bumping $BUMP_TYPE version..."
bump2version "$BUMP_TYPE"

NEW_VERSION=$(python -c "import configparser; c = configparser.ConfigParser(); c.read('.bumpversion.cfg'); print(c['bumpversion']['current_version'])")
print_success "Version bumped: $CURRENT_VERSION -> $NEW_VERSION"

# Push changes if not disabled
if [[ "$NO_PUSH" != true ]]; then
    print_status "Pushing changes to remote repository..."

    # Push commits and tags
    git push
    git push --tags

    print_success "Changes and tags pushed to remote repository"
    print_status "GitHub Actions will now build and create a release for v$NEW_VERSION"
else
    print_warning "Changes not pushed (--no-push flag used)"
    print_status "To push manually, run:"
    echo "  git push"
    echo "  git push --tags"
fi

print_success "Version bump complete!"
print_status "New version: $NEW_VERSION"
print_status "Tag created: v$NEW_VERSION"