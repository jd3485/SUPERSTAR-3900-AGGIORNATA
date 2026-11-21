#ifndef RX_TEST_XC_H
#define RX_TEST_XC_H
#include <stdint.h>
uint32_t mock_cp0_count(void);
#define _CP0_GET_COUNT() mock_cp0_count()
#endif
