/* PIC32MX250F128B. Startup: SYSCLK=PBCLK=36,864 MHz, 
   JTAG disabilitato. Servizio esclusivo di Timer2 e SPI1/2, non rientrante. */
#include <xc.h>
#include "pic32_iq.h"

#define ADC_SELECT (1u << 4)
#define SLAVE_SELECT (1u << 7)

static void select_frame(bool active)
{
    if (active) {
        LATBCLR = SLAVE_SELECT;
        LATBSET = ADC_SELECT;
    } else {
        LATBCLR = ADC_SELECT;
        LATBSET = SLAVE_SELECT;
    }
}

static void reset_spi(void)
{
    select_frame(false);
    SPI1CON = 0;
    SPI2CON = 0;
    (void)SPI1BUF;
    (void)SPI2BUF;
    SPI1STATCLR = _SPI1STAT_SPIROV_MASK;
    SPI2STATCLR = _SPI2STAT_SPIROV_MASK;
    SPI1BRG = 15;
    SPI2CON = _SPI2CON_MODE16_MASK | _SPI2CON_CKE_MASK | _SPI2CON_SSEN_MASK |
              _SPI2CON_DISSDO_MASK | _SPI2CON_ON_MASK;
    SPI1CON = _SPI1CON_MODE16_MASK | _SPI1CON_CKE_MASK | _SPI1CON_MSTEN_MASK |
              _SPI1CON_DISSDO_MASK | _SPI1CON_ON_MASK;
}

static struct iq_snapshot status(void)
{
    unsigned master = SPI1STAT, slave = SPI2STAT;
    struct iq_snapshot s = {
        .tick = TMR2,
        .ready_i = (master & _SPI1STAT_SPIRBF_MASK) != 0,
        .ready_q = (slave & _SPI2STAT_SPIRBF_MASK) != 0,
        .busy = (master & _SPI1STAT_SPIBUSY_MASK) != 0,
        .overrun = (master & _SPI1STAT_SPIROV_MASK) || (slave & _SPI2STAT_SPIROV_MASK)
    };
    s.invalid_slot = IFS0bits.T2IF || OSCCONbits.CF || OSCCONbits.COSC != 3;
    return s;
}

static void launch(void)
{
    SPI1BUF = 0;
#ifdef RX_SPI_OVERLAP
    rx_process_pending();
#endif
}
static void read_pair(uint16_t *i, uint16_t *q) { *i = SPI1BUF; *q = SPI2BUF; }
static const struct iq_port port = {status, select_frame, launch, read_pair, reset_spi};
static bool skip_slot;

static bool pins_mapped(void)
{
#ifdef RX_AUDIO_OC1
    if (RPA0R != 5)
        return false;
#endif
    return SDI1R == 4 && SDI2R == 3 && SS2R == 4;
}

bool pic32_iq_init(void)
{
    IEC0CLR = _IEC0_T2IE_MASK;       /* Il servizio usa polling del flag latched. */
    T2CON = 0;
    select_frame(false);
    ANSELBCLR = (1u << 13) | (1u << 14) | (1u << 15);
    LATBCLR = 1u << 14;
    TRISBSET = (1u << 8) | (1u << 9) | (1u << 13) | (1u << 15);
    TRISBCLR = ADC_SELECT | SLAVE_SELECT | (1u << 14);
    if (!pins_mapped()) {
        /* Inizializzazione prima del DMA. Con IOL1WAY basta uno sblocco. */
        unsigned previous_status = __builtin_disable_interrupts();
        SYSKEY = 0;
        SYSKEY = 0xaa996655u;
        SYSKEY = 0x556699aau;
        CFGCONbits.IOLOCK = 0;
        SDI1R = 4;                  /* RB8, pin 17 */
        SDI2R = 3;                  /* RB13, pin 24 */
        SS2R = 4;                   /* RB9, pin 18, da RB7 */
#ifdef RX_AUDIO_OC1
        RPA0R = 5;                  /* OC1, RA0, pin 2 */
#endif
        CFGCONbits.IOLOCK = 1;
        SYSKEY = 0;
        if (previous_status & 1u)
            __builtin_enable_interrupts();
    }
    if (!pins_mapped() || OSCCONbits.PBDIV != 0 ||
        OSCCONbits.COSC != 3 || OSCCONbits.CF || !OSCCONbits.SLOCK) {
        SPI1CON = 0;
        SPI2CON = 0;
        IFS0CLR = _IFS0_T2IF_MASK;
        return false;
    }
#ifdef RX_AUDIO_OC1
    T3CON = 0;
    OC1CON = 0;
    ANSELACLR = 1u;
    LATACLR = 1u;
    TRISACLR = 1u;
    TMR3 = 0;
    PR3 = 255;
    OC1R = 128;
    OC1RS = 128;
    OC1CON = _OC1CON_ON_MASK | _OC1CON_OCTSEL_MASK | 6u;
#endif
    reset_spi();
    PR2 = 767;
    TMR2 = 0;
    IFS0CLR = _IFS0_T2IF_MASK;
    skip_slot = true;
#ifdef RX_AUDIO_OC1
    T3CONSET = _T3CON_ON_MASK;
#endif
    T2CONSET = _T2CON_ON_MASK;
    return true;
}

enum iq_status pic32_iq_poll(struct iq_pair *out)
{
    if (!IFS0bits.T2IF)
        return IQ_IDLE;
    IFS0CLR = _IFS0_T2IF_MASK;
#ifdef RX_AUDIO_OC1
    OC1RS = rx_audio_slot(_CP0_GET_COUNT());
#endif
    if (skip_slot) {
        skip_slot = false;
        return IQ_IDLE;
    }
    enum iq_status result = iq_capture(&port, out);
    skip_slot = result != IQ_OK;
    return result;
}
