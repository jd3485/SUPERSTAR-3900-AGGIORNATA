# DFP_DIR indica la radice del PIC32MX_DFP scelto, contenente xc32/.
XC32_CC ?= xc32-gcc
HOST_CC ?= cc
BUILD_DIR ?= build
DEVICE_FLAGS := -mprocessor=32MX250F128B
ifneq ($(strip $(DFP_DIR)),)
DEVICE_FLAGS += -mdfp="$(DFP_DIR)/xc32"
endif
SOURCES := main.c pic32_iq.c iq_frame.c am_sync.c audio_decim.c
HEADERS := rx_profile.h pic32_iq.h iq_frame.h am_sync.h audio_decim.h
ELF := $(BUILD_DIR)/rx.elf

.PHONY: all host-check
all: $(ELF)

$(BUILD_DIR):
	mkdir -p "$@"

$(ELF): $(SOURCES) $(HEADERS) Makefile | $(BUILD_DIR)
	$(XC32_CC) $(CPPFLAGS) $(DEVICE_FLAGS) -std=gnu11 -O2 -Wall -Wextra $(SOURCES) -Wl,-Map,"$(BUILD_DIR)/rx.map" -o "$@"

$(BUILD_DIR)/iq_frame_test: iq_frame.c iq_frame.h ../../Verifiche/Firmware/iq_frame_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic iq_frame.c ../../Verifiche/Firmware/iq_frame_test.c -o "$@"

$(BUILD_DIR)/am_sync_test: am_sync.c am_sync.h iq_frame.h ../../Verifiche/Firmware/am_sync_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic am_sync.c ../../Verifiche/Firmware/am_sync_test.c -lm -o "$@"

$(BUILD_DIR)/audio_decim_test: audio_decim.c audio_decim.h ../../Verifiche/Firmware/audio_decim_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic audio_decim.c ../../Verifiche/Firmware/audio_decim_test.c -lm -o "$@"

$(BUILD_DIR)/rx_profile_test: rx_profile.h ../../Verifiche/Firmware/rx_profile_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic ../../Verifiche/Firmware/rx_profile_test.c -o "$@"

.PHONY: profile
profile:
	$(MAKE) BUILD_DIR="$(BUILD_DIR)/profile" CPPFLAGS="$(CPPFLAGS) -DRX_PROFILE" all

$(BUILD_DIR)/am_adjacent_test: am_sync.c am_sync.h iq_frame.h audio_decim.c audio_decim.h ../../Verifiche/Firmware/am_adjacent_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic am_sync.c audio_decim.c ../../Verifiche/Firmware/am_adjacent_test.c -lm -o "$@"

host-check: $(BUILD_DIR)/am_adjacent_test $(BUILD_DIR)/rx_profile_test $(BUILD_DIR)/iq_frame_test $(BUILD_DIR)/am_sync_test $(BUILD_DIR)/audio_decim_test
	"$(BUILD_DIR)/am_adjacent_test"
	"$(BUILD_DIR)/rx_profile_test"
	"$(BUILD_DIR)/audio_decim_test"
	"$(BUILD_DIR)/iq_frame_test"
	"$(BUILD_DIR)/am_sync_test"

.PHONY: verify
verify: $(ELF)
	python3 ../../Verifiche/Firmware/config_elf.py main.c "$(DFP_DIR)/xc32/32MX250F128B/configuration.data" "$(ELF)"
