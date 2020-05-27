try:
    from periphery import PWM
    pwm = PWM(2, 0)
    def enable_buzzer():
        pwm.enable()
    def disable_buzzer():
        pwm.disable()
    def set_freq(freq):
        pwm.frequency = freq

except:
    print("Could not import periphery lib.")