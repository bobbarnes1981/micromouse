#define LED_L 11
#define LED_R 6

#define WALL_L A2
#define WALL_C A1
#define WALL_R A0

#define EMITTERS 12

#define BATTERY_VOLTS A7
#define FUNC_SELECT A6

#define WALL_MIN_L 120
#define WALL_MIN_C 120
#define WALL_MIN_R 120

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
}

unsigned long last_millis = 0;
unsigned long elapsed_millis = 0;

int wall_val_l = 0;
int wall_val_c = 0;
int wall_val_r = 0;

void loop() {
  unsigned long m = millis();
  elapsed_millis += m - last_millis;
  last_millis = m;
  
  if (elapsed_millis > 1000) {
    elapsed_millis = 0;
    
    int bat_volts = map(analogRead(BATTERY_VOLTS), 0, 1023, 0, 9);

    Serial.print("Batt: ");
    Serial.print(bat_volts);
    Serial.print("v ");

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
    int function_select = -1;
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
    Serial.print("Func: ");
    Serial.print(function_select);
    Serial.print(" ");
    
    digitalWrite(EMITTERS, HIGH);

    wall_val_l = analogRead(WALL_L);
    wall_val_c = analogRead(WALL_C);
    wall_val_r = analogRead(WALL_R);

    digitalWrite(EMITTERS, LOW);

    Serial.print("Walls: ");
    Serial.print(wall_val_l);
    Serial.print(" : ");
    Serial.print(wall_val_c);
    Serial.print(" : ");
    Serial.print(wall_val_r);
    Serial.println("");
  
  }

  digitalWrite(LED_L, wall_val_c > WALL_MIN_C || wall_val_l > WALL_MIN_L ? HIGH : LOW);
  digitalWrite(LED_R, wall_val_c > WALL_MIN_C || wall_val_r > WALL_MIN_R ? HIGH : LOW);
}
