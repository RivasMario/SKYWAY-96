#include "skyway96.h"

void keyboard_post_init_kb(void) {
    gpio_set_pin_output(GP26);
    gpio_write_pin_high(GP26);
}
