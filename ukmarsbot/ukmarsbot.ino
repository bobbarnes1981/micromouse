#include "digitalWriteFast.h"

#define LED_L 11
#define LED_R 6

#define WALL_L A2
#define WALL_C A1
#define WALL_R A0

#define EMITTERS 12

#define BATTERY_VOLTS A7
#define FUNC_SELECT A6

#define BATTERY_DIVIDER_RATIO 2.0f

#define WALL_MIN_L 120
#define WALL_MIN_C 120
#define WALL_MIN_R 120

#define ENCODER_CLK_L 2
#define ENCODER_CLK_R 3
#define ENCODER_B_L 4
#define ENCODER_B_R 5
#define MOTOR_DIR_L 7
#define MOTOR_DIR_R 8
#define MOTOR_PWM_L 9
#define MOTOR_PWM_R 10

#define DELAY 100

//minicom --device /dev/ttyUSB0 --baudrate 9600
//minicom --device /dev/rfcomm0 --baudrate 9600
//HC06 pin 1234

unsigned long last_millis = 0;
unsigned long elapsed_millis = 0;

int wall_val_l = 0;
int wall_val_c = 0;
int wall_val_r = 0;

int function_select;
float battery_volts;

volatile int encoderCountL;
volatile int encoderCountR;

void setup() {
  Serial.begin(9600);
  
  pinMode(LED_L, OUTPUT);
  pinMode(LED_R, OUTPUT);

  pinMode(WALL_L, INPUT);
  pinMode(WALL_C, INPUT);
  pinMode(WALL_R, INPUT);

  pinMode(EMITTERS, OUTPUT);
  pinMode(BATTERY_VOLTS, INPUT);
  pinMode(FUNC_SELECT, INPUT);

  pinMode(ENCODER_CLK_L, INPUT);
  pinMode(ENCODER_CLK_R, INPUT);

  pinMode(ENCODER_B_L, INPUT);
  pinMode(ENCODER_B_R, INPUT);
  
  digitalWrite(EMITTERS, LOW);

  bitClear(EICRA, ISC01);
  bitSet(EICRA, ISC00);
  bitSet(EIMSK, INT0);
  encoderCountL = 0;
  
  bitClear(EICRA, ISC11);
  bitSet(EICRA, ISC10);
  bitSet(EIMSK, INT1);
  encoderCountR = 0;
}

ISR(INT0_vect) {
  static bool oldB = 0;
  bool newB = bool(digitalReadFast(ENCODER_B_L));
  bool newA = bool(digitalReadFast(ENCODER_CLK_L)) ^ newB;
  if (newA == oldB) {
    encoderCountL--;
  } else {
    encoderCountL++;
  }
  oldB = newB;
}

ISR(INT1_vect) {
  static bool oldB = 0;
  bool newB = bool(digitalReadFast(ENCODER_B_R));
  bool newA = bool(digitalReadFast(ENCODER_CLK_R)) ^ newB;
  if (newA == oldB) {
    encoderCountR++;
  } else {
    encoderCountR--;
  }
  oldB = newB;
}

void loop() {
  unsigned long m = millis();
  elapsed_millis += m - last_millis;
  last_millis = m;
  
  if (elapsed_millis > DELAY) {
    elapsed_millis = 0;
    
    read_battery_volts();
    Serial.print("Batt: ");
    Serial.print(battery_volts);
    Serial.print("v ");

    read_function_select();
    Serial.print("Func: ");
    Serial.print(function_select);
    Serial.print(" ");

    read_sensors();
    Serial.print("Walls: ");
    Serial.print(wall_val_l);
    Serial.print(" : ");
    Serial.print(wall_val_c);
    Serial.print(" : ");
    Serial.print(wall_val_r);
    Serial.print(" ");

    Serial.print("EncL: ");
    Serial.print(encoderCountL);
    Serial.print(" ");
    Serial.print("EncR: ");
    Serial.print(encoderCountR);
    Serial.println("");
  }

  digitalWrite(LED_L, wall_val_c > WALL_MIN_C || wall_val_l > WALL_MIN_L ? HIGH : LOW);
  digitalWrite(LED_R, wall_val_c > WALL_MIN_C || wall_val_r > WALL_MIN_R ? HIGH : LOW);
}

void read_battery_volts() {
  int battery_volts_raw = analogRead(BATTERY_VOLTS);
  battery_volts = battery_volts_raw * (5.0f * BATTERY_DIVIDER_RATIO / 1023.0f);
}

void read_function_select() {
  int function_select_read = analogRead(FUNC_SELECT);
  // button 1023
  // Draws a curve...
  // 4321   val   diff  diff
  // 0000   663   
  // 1000   649   14    
  // 0100   632   17    2
  // 1100   617   15    -2
  // 0010   591   26    11
  // 1010   571   20    -6
  // 0110   546   25    5
  // 1110   523   23    -2
  // 0001   466   57    34
  // 1001   434   32    25
  // 0101   390   44    12
  // 1101   348   42    -2
  // 0011   273   75    33
  // 1011   214   59    16
  // 0111   130   84    -25
  // 1111   044   86    2
  function_select = -1;
  if (function_select_read > (663+((1023-663)/2))) {
    function_select = 16;
  } else {
    int dip_vals[] = { 663, 649, 632, 617, 591, 571, 546, 523, 466, 434, 390, 348, 273, 214, 130, 44, 0 };
    for (int i = 0; i < 16; i++) {
      if (function_select_read > (dip_vals[i+1]+((dip_vals[i]-dip_vals[i+1])/2))) {
        function_select = i;
        break;
      }
    }
  }
}

void read_sensors() {
  int wall_dark_l = analogRead(WALL_L);
  int wall_dark_c = analogRead(WALL_C);
  int wall_dark_r = analogRead(WALL_R);
  
  digitalWrite(EMITTERS, HIGH);

  delayMicroseconds(50);

  int wall_light_l = analogRead(WALL_L);
  int wall_light_c = analogRead(WALL_C);
  int wall_light_r = analogRead(WALL_R);
  
  digitalWrite(EMITTERS, LOW);

  wall_val_l = wall_light_l - wall_dark_l;
  wall_val_c = wall_light_c - wall_dark_c;
  wall_val_r = wall_light_r - wall_dark_r;
}
