try:
    from periphery import PWM
    import time
    pwm = PWM(2, 0)
    pwm.frequency = 1e3
    pwm.duty_cycle = 0.9
    def enable_buzzer():
        pwm.enable()
    def disable_buzzer():
        pwm.disable()
    def set_freq(freq):
        pwm.frequency = freq
    def cooltone():
        enable_buzzer()
        for x in [587.330, 793.989, 880, 1174.66]:
            pwm.frequency = x
            time.sleep(0.3)
        disable_buzzer()

except:
    print("Could not import periphery lib.")