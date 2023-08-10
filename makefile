.PHONY: default
default:
	@echo "What are you doing?"

.PHONY: clean
clean:
	@echo "Cleaning directory."
	@find . -name '*.rpyc' -o -name '*.rpyb' -o -name '*.rpymc' | xargs -I'{}' rm '{}'
