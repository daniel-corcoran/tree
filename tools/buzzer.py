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
        for x in range(10):
            pwm.frequency = (x * 100) + 100
            time.sleep(0.15)
        disable_buzzer()

except:
    print("Could not import periphery lib.")