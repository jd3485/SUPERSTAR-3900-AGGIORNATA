# DFP_DIR indica la radice del PIC32MX_DFP scelto, contenente xc32/.
XC32_CC ?= xc32-gcc
HOST_CC ?= cc
BUILD_DIR ?= build
DEVICE_FLAGS := -mprocessor=32MX250F128B
ifneq ($(strip $(DFP_DIR)),)
DEVICE_FLAGS += -mdfp="$(DFP_DIR)/xc32"
endif
SOURCES := main.c pic32_iq.c iq_frame.c am_sync.c audio_decim.c
SOURCES += $(EXTRA_SOURCES)
HEADERS := audio_monitor.h audio_level.h audio_gate.h audio_pwm.h iq_iir.h rx_profile.h pic32_iq.h iq_frame.h am_sync.h audio_decim.h
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

.PHONY: profile-audio
profile-audio:
	$(MAKE) BUILD_DIR="$(BUILD_DIR)/profile-audio" CPPFLAGS="$(CPPFLAGS) -DRX_AUDIO_MONITOR -DRX_PROFILE -DRX_IQ_IIR -DRX_SPI_OVERLAP" EXTRA_SOURCES="iq_iir.c audio_monitor.c audio_gate.c audio_level.c audio_pwm.c" all

.PHONY: profile-overlap
profile-overlap:
	$(MAKE) BUILD_DIR="$(BUILD_DIR)/profile-overlap" CPPFLAGS="$(CPPFLAGS) -DRX_PROFILE -DRX_IQ_IIR -DRX_SPI_OVERLAP" EXTRA_SOURCES=iq_iir.c all

.PHONY: profile-iir
profile-iir:
	$(MAKE) BUILD_DIR="$(BUILD_DIR)/profile-iir" CPPFLAGS="$(CPPFLAGS) -DRX_PROFILE -DRX_IQ_IIR" EXTRA_SOURCES=iq_iir.c all

$(BUILD_DIR)/am_adjacent_test: iq_iir.c iq_iir.h am_sync.c am_sync.h iq_frame.h audio_decim.c audio_decim.h ../../Verifiche/Firmware/am_adjacent_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic iq_iir.c am_sync.c audio_decim.c ../../Verifiche/Firmware/am_adjacent_test.c -lm -o "$@"

$(BUILD_DIR)/iq_schedule_test: iq_frame.c iq_frame.h ../../Verifiche/Firmware/iq_schedule_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic iq_frame.c ../../Verifiche/Firmware/iq_schedule_test.c -o "$@"

$(BUILD_DIR)/overlap_test: main.c $(HEADERS) am_sync.c audio_decim.c iq_iir.c ../../Verifiche/Firmware/overlap_test.c ../../Verifiche/Firmware/mock/xc.h | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic -Wno-unknown-pragmas -DRX_PROFILE -DRX_IQ_IIR -DRX_SPI_OVERLAP -I../../Verifiche/Firmware/mock am_sync.c audio_decim.c iq_iir.c ../../Verifiche/Firmware/overlap_test.c -o "$@"

$(BUILD_DIR)/profile_audio_test: main.c $(HEADERS) audio_monitor.c audio_gate.c audio_level.c audio_pwm.c am_sync.c audio_decim.c iq_iir.c ../../Verifiche/Firmware/overlap_test.c ../../Verifiche/Firmware/mock/xc.h | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic -Wno-unknown-pragmas -DRX_AUDIO_MONITOR -DRX_PROFILE -DRX_IQ_IIR -DRX_SPI_OVERLAP -I../../Verifiche/Firmware/mock audio_monitor.c audio_gate.c audio_level.c audio_pwm.c am_sync.c audio_decim.c iq_iir.c ../../Verifiche/Firmware/overlap_test.c -o "$@"

$(BUILD_DIR)/audio_pwm_test: audio_pwm.c audio_pwm.h ../../Verifiche/Firmware/audio_pwm_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic audio_pwm.c ../../Verifiche/Firmware/audio_pwm_test.c -o "$@"

$(BUILD_DIR)/audio_level_test: audio_level.c audio_level.h audio_pwm.c audio_pwm.h ../../Verifiche/Firmware/audio_level_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic audio_level.c audio_pwm.c ../../Verifiche/Firmware/audio_level_test.c -lm -o "$@"

$(BUILD_DIR)/audio_gate_test: audio_gate.c audio_gate.h audio_level.c audio_level.h audio_pwm.c audio_pwm.h am_sync.c am_sync.h iq_frame.h audio_decim.c audio_decim.h ../../Verifiche/Firmware/audio_gate_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic audio_gate.c audio_level.c audio_pwm.c am_sync.c audio_decim.c ../../Verifiche/Firmware/audio_gate_test.c -lm -o "$@"

$(BUILD_DIR)/squelch_fading_test: iq_iir.c iq_iir.h audio_gate.c audio_gate.h audio_level.c audio_level.h audio_pwm.c audio_pwm.h am_sync.c am_sync.h iq_frame.h audio_decim.c audio_decim.h ../../Verifiche/Firmware/squelch_fading_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic iq_iir.c audio_gate.c audio_level.c audio_pwm.c am_sync.c audio_decim.c ../../Verifiche/Firmware/squelch_fading_test.c -lm -o "$@"

$(BUILD_DIR)/audio_monitor_test: $(HEADERS) audio_monitor.c audio_gate.c audio_level.c audio_pwm.c ../../Verifiche/Firmware/audio_monitor_test.c | $(BUILD_DIR)
	$(HOST_CC) -std=c11 -O2 -Wall -Wextra -Werror -pedantic audio_monitor.c audio_gate.c audio_level.c audio_pwm.c ../../Verifiche/Firmware/audio_monitor_test.c -o "$@"

host-check: $(BUILD_DIR)/profile_audio_test $(BUILD_DIR)/audio_monitor_test $(BUILD_DIR)/squelch_fading_test $(BUILD_DIR)/audio_gate_test $(BUILD_DIR)/audio_level_test $(BUILD_DIR)/audio_pwm_test $(BUILD_DIR)/overlap_test $(BUILD_DIR)/iq_schedule_test $(BUILD_DIR)/am_adjacent_test $(BUILD_DIR)/rx_profile_test $(BUILD_DIR)/iq_frame_test $(BUILD_DIR)/am_sync_test $(BUILD_DIR)/audio_decim_test
	"$(BUILD_DIR)/profile_audio_test"
	"$(BUILD_DIR)/audio_monitor_test"
	"$(BUILD_DIR)/squelch_fading_test"
	"$(BUILD_DIR)/audio_gate_test"
	"$(BUILD_DIR)/audio_level_test"
	"$(BUILD_DIR)/audio_pwm_test"
	"$(BUILD_DIR)/overlap_test"
	"$(BUILD_DIR)/iq_schedule_test"
	"$(BUILD_DIR)/am_adjacent_test"
	"$(BUILD_DIR)/rx_profile_test"
	"$(BUILD_DIR)/audio_decim_test"
	"$(BUILD_DIR)/iq_frame_test"
	"$(BUILD_DIR)/am_sync_test"

.PHONY: verify
verify: $(ELF)
	python3 ../../Verifiche/Firmware/config_elf.py main.c "$(DFP_DIR)/xc32/32MX250F128B/configuration.data" "$(ELF)"
