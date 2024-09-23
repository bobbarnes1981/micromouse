#define MAX_MOTOR_VOLTS 6.0f

#define MOTOR_DIR_L 7
#define MOTOR_DIR_R 8
#define MOTOR_PWM_L 9
#define MOTOR_PWM_R 10

void set_motor_pwm_l(int pwm) {
  // basic example without battery
  pwm = constrain(pwm, -255, 255);
  if (pwm < 0) {
    digitalWrite(MOTOR_DIR_L, LOW);
    analogWrite(MOTOR_PWM_L, -pwm);
  } else {
    digitalWrite(MOTOR_DIR_L, HIGH);
    analogWrite(MOTOR_PWM_L, pwm);
  }
}

void set_motor_pwm_r(int pwm) {
  pwm = constrain(pwm, -255, 255);
  if (pwm < 0) {
    digitalWrite(MOTOR_DIR_R, HIGH);
    analogWrite(MOTOR_PWM_R, -pwm);
  } else {
    digitalWrite(MOTOR_DIR_R, LOW);
    analogWrite(MOTOR_PWM_R, pwm);
  }
}

void set_motor_pwm(int l, int r) {
  set_motor_pwm_l(l);
  set_motor_pwm_r(r);
}

void set_motor_volts_l(float battery_volts, float v) {
  v = constrain(v, -MAX_MOTOR_VOLTS, MAX_MOTOR_VOLTS);
  int motor_pwm = (int)((255.0f * v) / battery_volts);
  set_motor_pwm_l(motor_pwm);
}

void set_motor_volts_r(float battery_volts, float v) {
  v = constrain(v, -MAX_MOTOR_VOLTS, MAX_MOTOR_VOLTS);
  int motor_pwm = (int)((255.0f * v) / battery_volts);
  set_motor_pwm_r(motor_pwm);
}

void set_motor_volts(float battery_volts, float l, float r) {
  set_motor_volts_l(battery_volts, l);
  set_motor_volts_r(battery_volts, r);
}
