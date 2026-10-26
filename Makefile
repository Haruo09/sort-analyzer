CC = gcc
CFLAGS = -Wall -Wextra -O3 -Iinclude -fPIC
LDFLAGS = -shared

SRC_DIR = src
APP_DIR = apps
BUILD_DIR = build
LIB_DIR = $(BUILD_DIR)/lib
BIN_DIR = $(BUILD_DIR)/bin
OBJ_DIR = $(BUILD_DIR)/obj

LIB_SRCS = $(wildcard $(SRC_DIR)/*.c)
LIB_OBJS = $(patsubst $(SRC_DIR)/%.c, $(OBJ_DIR)/%.o, $(LIB_SRCS))

# Handle Windows vs Linux/macOS extensions
ifeq ($(OS),Windows_NT)
	LIB_NAME = timsort.dll
	BIN_NAME = timsort_c_test.exe
else
	LIB_NAME = libtimsort.so
	BIN_NAME = timsort_c_test
endif

TARGET_LIB = $(LIB_DIR)/$(LIB_NAME)
TARGET_BIN = $(BIN_DIR)/$(BIN_NAME)

all: $(TARGET_LIB) $(TARGET_BIN)

# 1. Compile the shared library from src/
$(TARGET_LIB): $(LIB_OBJS) | $(LIB_DIR)
	$(CC) $(LDFLAGS) -o $@ $^

# 2. Compile the C executable runner from apps/
$(TARGET_BIN): $(APP_DIR)/main.c $(TARGET_LIB) | $(BIN_DIR)
	$(CC) $(CFLAGS) $< -o $@ -L$(LIB_DIR) -ltimsort -Wl,-rpath,$(LIB_DIR)

# Pattern rule for objects
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Create necessary directories
$(LIB_DIR) $(BIN_DIR) $(OBJ_DIR):
	mkdir -p $@

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all clean
