#define L_LED 11
#define R_LED 6

#define L_WALL A2
#define C_WALL A1
#define R_WALL A0

#define EMITTERS 12

#define BATTERY_VOLTS A7
#define FUNC_SELECT A6

#define L_WALL_MIN 300
#define C_WALL_MIN 300
#define R_WALL_MIN 300

void setup() {
  Serial.begin(9600);
  
  pinMode(L_LED, OUTPUT);
  pinMode(R_LED, OUTPUT);

  pinMode(L_WALL, INPUT);
  pinMode(C_WALL, INPUT);
  pinMode(R_WALL, INPUT);

  pinMode(EMITTERS, OUTPUT);
  pinMode(BATTERY_VOLTS, INPUT);
  pinMode(FUNC_SELECT, INPUT);
}

unsigned long lastMillis = 0;
unsigned long elapsedMillis = 0;

int lWallVal = 0;
int cWallVal = 0;
int rWallVal = 0;

void loop() {
  unsigned long m = millis();
  elapsedMillis += m - lastMillis;
  lastMillis = m;
  
  if (elapsedMillis > 1000) {
    elapsedMillis = 0;
    
    int batVolts = map(analogRead(BATTERY_VOLTS), 0, 1023, 0, 9);

    Serial.print("Battery: ");
    Serial.print(batVolts);
    Serial.println("v");

    int funcSelect = analogRead(FUNC_SELECT);
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
    Serial.print("Func: ");
    Serial.println(funcSelect);
    
    digitalWrite(EMITTERS, HIGH);

    lWallVal = analogRead(L_WALL);
    cWallVal = analogRead(C_WALL);
    rWallVal = analogRead(R_WALL);
    Serial.print(lWallVal);
    Serial.print(" : ");
    Serial.print(cWallVal);
    Serial.print(" : ");
    Serial.println(rWallVal);

    digitalWrite(EMITTERS, LOW);
  
  }

  digitalWrite(L_LED, cWallVal > C_WALL_MIN || lWallVal > L_WALL_MIN ? HIGH : LOW);
  digitalWrite(R_LED, cWallVal > C_WALL_MIN || rWallVal > R_WALL_MIN ? HIGH : LOW);
}
