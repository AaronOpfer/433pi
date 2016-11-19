import time
import sys
import gc
import RPi.GPIO as GPIO

NUM_ATTEMPTS = 8
TRANSMIT_PIN = 24

class GPIOSetup:
    def __enter__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

    def __exit__(self, a, b, c):
        GPIO.cleanup()


class Control:
    @staticmethod
    def _sleep(amount):
        start = time.time()
        while time.time() - start < amount:
            pass

    @classmethod
    def _pulse(cls, hi_time, total_time):
        GPIO.output(TRANSMIT_PIN, 1)
        cls._sleep(hi_time)
        GPIO.output(TRANSMIT_PIN, 0)
        cls._sleep(total_time - hi_time)

    def do_cmd(self, cmd_name):
        for _ in range(NUM_ATTEMPTS):
            cmd = self.cmds[cmd_name]
            for pulse_name in cmd:
                self._pulse(*self.pulses[pulse_name])
            for pulse in self.suffix:
                self._pulse(*pulse)

class Lights(Control):
    pulses = {
        'S': (0.00012, 0.00075),
        'L': (0.00051, 0.00075),
    }

    suffix = [(0.00012, 0.006)]

    cmds = dict(
    a_on  = 'SLSSSSSLSLSLSLSLSSLLSSLL',
    a_off = 'SLSSSSSLSLSLSLSLSSLLLLSS',
    b_on  = 'SLSSSSSLSLSLSLSLLLSSSSLL',
    b_off = 'SLSSSSSLSLSLSLSLLLSSLLSS',
    c_on  = 'SLSSSSSLSLSLSLLLSSSSSSLL',
    c_off = 'SLSSSSSLSLSLSLLLSSSSLLSS'
    )


if __name__ == '__main__':
    control = globals()[sys.argv[1]]()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)

    with GPIOSetup():
        for argument in sys.argv[2:]:
            control.do_cmd(argument)

