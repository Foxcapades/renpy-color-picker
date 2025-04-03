GIT_VERSION := $(shell git describe --tags | sed 's/v//g')
OPT_VERSION := $(shell grep 'config.version' game/options.rpy | cut -d '"' -f2)
BUILD_DIR   := "build"
PROJECT_ZIP := "$(BUILD_DIR)/color-picker-$(OPT_VERSION)-project.zip"
SLIM_ZIP    := "$(BUILD_DIR)/color-picker-$(OPT_VERSION)-slim.zip"

RENPY_VERSION := 8.3.7
RENPY_COMMAND := /opt/renpy/$(RENPY_VERSION)/renpy.sh

.PHONY: default
default:
	@echo "What are you doing?"


.PHONY: clean
clean:
	@echo "Cleaning directory."
	@rm -rf build/
	@find . -name '*.rpyc' -o -name '*.rpyb' -o -name '*.rpymc' | xargs -I'{}' rm '{}'


.PHONY: release
release: $(SLIM_ZIP) $(PROJECT_ZIP) build-distributions

.PHONY: versions
versions:
	@echo "Git: $(GIT_VERSION)"
	@echo "Opt: $(OPT_VERSION)"


##
## Build the slim zip.
##
$(SLIM_ZIP): clean
	@if [ '$(GIT_VERSION)' != '$(OPT_VERSION)' ]; then \
		echo "Refusing to release while the git tag does not match the option version."; \
		exit 1; \
	fi

	@echo "Packing slim zip"
	@mkdir -p $(BUILD_DIR)
	@cp license color-picker-license
	@cp docs/color-picker-readme-slim.txt color-picker-readme.txt
	@zip -q9r $(SLIM_ZIP) game/lib color-picker-license color-picker-readme.txt
	@rm color-picker-license color-picker-readme.txt


##
## Build the project zip.
##
$(PROJECT_ZIP): clean
	@if [ '$(GIT_VERSION)' != '$(OPT_VERSION)' ]; then \
		echo "Refusing to release while the git tag does not match the option version."; \
		exit 1; \
	fi

	@echo "Packing project zip"
	@mkdir -p $(BUILD_DIR)
	@cp license color-picker-license
	@cp docs/color-picker-readme-project.txt color-picker-readme.txt
	@zip -q9r $(PROJECT_ZIP) game color-picker-license color-picker-readme.txt -x game/saves/**\* -x game/cache/**\*
	@rm color-picker-license color-picker-readme.txt


##
## Build the Ren'Py Distributions
##
.PHONY: build-distributions
build-distributions: $(BUILD_DIR)/lib-color-picker-$(OPT_VERSION)-linux.tar.bz2 \
										 $(BUILD_DIR)/lib-color-picker-$(OPT_VERSION)-pc.zip \
										 $(BUILD_DIR)/lib-color-picker-$(OPT_VERSION)-mac.zip


$(BUILD_DIR)/lib-color-picker-$(OPT_VERSION)-linux.tar.bz2: clean
	@mkdir -p $(BUILD_DIR)
	@$(RENPY_COMMAND) /opt/renpy/$(RENPY_VERSION)/launcher distribute . --package=linux --dest=$(BUILD_DIR)


$(BUILD_DIR)/lib-color-picker-$(OPT_VERSION)-pc.zip: clean
	@mkdir -p $(BUILD_DIR)
	@$(RENPY_COMMAND) /opt/renpy/$(RENPY_VERSION)/launcher distribute . --package=pc --dest=$(BUILD_DIR)


$(BUILD_DIR)/lib-color-picker-$(OPT_VERSION)-mac.zip: clean
	@mkdir -p $(BUILD_DIR)
	@$(RENPY_COMMAND) /opt/renpy/$(RENPY_VERSION)/launcher distribute . --package=mac --dest=$(BUILD_DIR)
