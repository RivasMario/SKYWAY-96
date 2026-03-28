
#include "ahsan96.h"

void keyboard_post_init_kb(void) {
    setPinOutput(GP26);
    writePinHigh(GP26);
}
