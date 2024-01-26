KDOTOOL_SRC = externals/kdotool
KDOTOOL_BUILD_DIR = core/bin/kdotool
DEPENDENCY := 

ifeq ($(shell uname),Linux)
	DEPENDENCY := $(DEPENDENCY) kdotool
endif

all : $(DEPENDENCY)

kdotool : $(KDOTOOL_SRC)/src/$(wildcard *.rs)
	cargo build --release --manifest-path $(KDOTOOL_SRC)/Cargo.toml --target-dir $(KDOTOOL_BUILD_DIR)