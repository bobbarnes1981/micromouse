#include "encoders.h"
#include "digitalWriteFast.h"

#include <Arduino.h>

#define ENCODER_CLK_L 2
#define ENCODER_CLK_R 3
#define ENCODER_B_L 4
#define ENCODER_B_R 5

volatile int encoder_count_l;
volatile int encoder_count_r;

void setup_encoders() {
  pinMode(ENCODER_CLK_L, INPUT);
  pinMode(ENCODER_CLK_R, INPUT);

  pinMode(ENCODER_B_L, INPUT);
  pinMode(ENCODER_B_R, INPUT);

  bitClear(EICRA, ISC01);
  bitSet(EICRA, ISC00);
  bitSet(EIMSK, INT0);
  encoder_count_l = 0;

  bitClear(EICRA, ISC11);
  bitSet(EICRA, ISC10);
  bitSet(EIMSK, INT1);
  encoder_count_r = 0;
}

ISR(INT0_vect) {
  static bool oldB = 0;
  bool newB = bool(digitalReadFast(ENCODER_B_L));
  bool newA = bool(digitalReadFast(ENCODER_CLK_L)) ^ newB;
  if (newA == oldB) {
    encoder_count_l--;
  } else {
    encoder_count_l++;
  }
  oldB = newB;
}

ISR(INT1_vect) {
  static bool oldB = 0;
  bool newB = bool(digitalReadFast(ENCODER_B_R));
  bool newA = bool(digitalReadFast(ENCODER_CLK_R)) ^ newB;
  if (newA == oldB) {
    encoder_count_r++;
  } else {
    encoder_count_r--;
  }
  oldB = newB;
}

int get_encoder_count_l() {
  return encoder_count_l;
}

int get_encoder_count_r() {
  return encoder_count_r;
}
