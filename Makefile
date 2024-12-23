# Define reusable variables
CARGO = cargo
WORKSPACE_TEST = $(CARGO) test --workspace
BUILD = $(CARGO) build --workspace
CLEAN = $(CARGO) clean
FORMAT = $(CARGO) fmt --all
CLIPPY = $(CARGO) clippy --all -- -D warnings

# Default target
.PHONY: all
all: build

# Run tests for the entire workspace
.PHONY: test
test:
	$(WORKSPACE_TEST)

# Build the entire workspace
.PHONY: build
build:
	$(BUILD)

# Clean the project
.PHONY: clean
clean:
	$(CLEAN)

# Format code
.PHONY: format
format:
	$(FORMAT)

# Run Clippy linter
.PHONY: lint
lint:
	$(CLIPPY)
