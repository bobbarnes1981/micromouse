
#define EMPTY -1
#define MAZE_X 16
#define MAZE_Y 16
#define MAX_QUEUE_LENGTH 256
#define MAX_ROUTE_LENGTH 256

#define DELAY 1000

enum ABS_DIR {
  NORTH = 0x01,
  EAST  = 0x02,
  SOUTH = 0x04,
  WEST  = 0x08
};

enum REL_DIR {
  NONE      = 0x00,
  FORWARD   = 0x01,
  RIGHT     = 0x02,
  BACKWARD  = 0x04,
  LEFT      = 0x08
};

struct Location {
  byte X;
  byte Y;
};

struct Step {
  int Value;
  Location Coord;
  ABS_DIR Abs;
  REL_DIR Rel;
};

// for debug
char buf[256];

unsigned long prevMillis = 0;

byte maze[MAZE_Y][MAZE_X] = {
    { 0x09, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x03 },
    { 0x0A, 0x09, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x01, 0x05, 0x05, 0x05, 0x05, 0x02 },
    { 0x0A, 0x0A, 0x09, 0x05, 0x05, 0x05, 0x01, 0x05, 0x07, 0x0D, 0x04, 0x01, 0x05, 0x05, 0x03, 0x0A },
    { 0x0A, 0x0A, 0x0A, 0x0B, 0x09, 0x03, 0x0C, 0x05, 0x03, 0x0B, 0x09, 0x06, 0x09, 0x05, 0x06, 0x0A },
    { 0x0A, 0x0A, 0x0A, 0x08, 0x06, 0x0A, 0x09, 0x03, 0x0C, 0x02, 0x0A, 0x0D, 0x04, 0x05, 0x03, 0x0A },
    { 0x0A, 0x0A, 0x0A, 0x0C, 0x03, 0x0A, 0x0A, 0x0C, 0x03, 0x0C, 0x06, 0x09, 0x05, 0x05, 0x06, 0x0A },
    { 0x0A, 0x0A, 0x0C, 0x05, 0x06, 0x0A, 0x0A, 0x0D, 0x04, 0x05, 0x03, 0x0C, 0x05, 0x03, 0x0B, 0x0A },
    { 0x0A, 0x0A, 0x09, 0x03, 0x0D, 0x02, 0x0A, 0x09, 0x01, 0x03, 0x0C, 0x05, 0x05, 0x06, 0x0A, 0x0A },
    { 0x0A, 0x0A, 0x0A, 0x0C, 0x03, 0x0A, 0x0A, 0x0C, 0x06, 0x0C, 0x01, 0x07, 0x09, 0x01, 0x02, 0x0A },
    { 0x0A, 0x0A, 0x0A, 0x09, 0x06, 0x08, 0x06, 0x0D, 0x01, 0x03, 0x0C, 0x03, 0x0A, 0x0E, 0x0A, 0x0A },
    { 0x0A, 0x0A, 0x0A, 0x0C, 0x05, 0x06, 0x09, 0x03, 0x0A, 0x0C, 0x03, 0x0C, 0x00, 0x05, 0x02, 0x0A },
    { 0x0A, 0x0A, 0x0C, 0x05, 0x05, 0x03, 0x0A, 0x0A, 0x0C, 0x03, 0x0C, 0x03, 0x0C, 0x03, 0x0A, 0x0A },
    { 0x0A, 0x0A, 0x09, 0x05, 0x05, 0x06, 0x0A, 0x0A, 0x0D, 0x04, 0x03, 0x0C, 0x03, 0x0C, 0x02, 0x0A },
    { 0x08, 0x02, 0x0A, 0x0D, 0x05, 0x05, 0x02, 0x0A, 0x0D, 0x05, 0x04, 0x03, 0x0C, 0x03, 0x0A, 0x0A },
    { 0x0A, 0x0A, 0x0C, 0x05, 0x05, 0x05, 0x06, 0x0C, 0x05, 0x05, 0x05, 0x06, 0x0D, 0x04, 0x06, 0x0A },
    { 0x0E, 0x0C, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x06 },
};

// byte maze[MAZE_Y][MAZE_X] = {
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
//   { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
// };

// byte is smaller but how would we represent EMPTY? 255? and hope we never need it for a flood value?
int flood[MAZE_Y][MAZE_X] = {
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
  { EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY },
};

int queueLength = 0;
Location queue[MAX_QUEUE_LENGTH];

void enqueue(Location location) {
  // if we haven't reached the max queue length
  if (queueLength < MAX_QUEUE_LENGTH) {
    // append item to queue
    queue[queueLength] = location;
    // increment queue length
    queueLength+=1;
  }
}

Location dequeue() {
  // take item from front of queue
  Location location = queue[0];
  // decrement the queue length
  queueLength -= 1;
  // move every item up the queue
  for (int i = 0; i < queueLength; i++) {
    queue[i] = queue[i+1];
  }
  // return the location
  return location;
}

int getFlood(Location l) {
  return flood[MAZE_Y-1-l.Y][l.X];
}

void setFlood(Location l, int value) {
  flood[MAZE_Y-1-l.Y][l.X] = value;
}

byte getMaze(Location l) {
  return maze[MAZE_Y-1-l.Y][l.X];
}

void setMaze(Location l, byte value) {
  maze[MAZE_Y-1-l.Y][l.X] = value;
}

bool isWall(Location location, ABS_DIR dir) {
  return (getMaze(location) & dir) == dir;
}

void setup() {
  Serial.begin(115200, SERIAL_8N1);
}

void loop() {
  unsigned long currMillis = millis();
  unsigned long elapMillis = currMillis - prevMillis;
  if (elapMillis >= DELAY) {
    Serial.println(elapMillis);

    unsigned long start, taken;

    start = millis();
    processFlood();
    taken = millis() - start;
    Serial.print("Flood: ");
    Serial.println(taken);

    start = millis();
    generateRoute({0,0}, NORTH, 0x00);
    taken = millis() - start;
    Serial.print("Generate: ");
    Serial.println(taken);

    serialFlood();

    prevMillis = currMillis;
  }
}

void processFlood() {
  // clear
  for (int y = 0; y < MAZE_Y; y++) {
    for (int x = 0; x < MAZE_X; x++) {
      setFlood({x, y}, EMPTY);
    }
  }
  // set goal
  setFlood({7, 7}, 0);
  enqueue({7,7});
  setFlood({7, 8}, 0);
  enqueue({7,8});
  setFlood({8, 7}, 0);
  enqueue({8,7});
  setFlood({8, 8}, 0);
  enqueue({8,8});
  // flood
  while(queueLength > 0) {
    Location l = dequeue();
    byte score = getFlood(l);
    Location n = { l.X, l.Y + 1 };
    if (n.X >= 0 && n.Y >= 0 && n.X < MAZE_X && n.Y < MAZE_Y && !isWall(l, NORTH)) {
      if (getFlood(n) == EMPTY) {
        setFlood(n, score+1);
        enqueue(n);
      }
    }
    Location e = { l.X + 1, l.Y };
    if (e.X >= 0 && e.Y >= 0 && e.X < MAZE_X && e.Y < MAZE_Y && !isWall(l, EAST)) {
      if (getFlood(e) == EMPTY) {
        setFlood(e, score+1);
        enqueue(e);
      }
    }
    Location s = { l.X, l.Y - 1 };
    if (s.X >= 0 && s.Y >= 0 && s.X < MAZE_X && s.Y < MAZE_Y && !isWall(l, SOUTH)) {
      if (getFlood(s) == EMPTY) {
        setFlood(s, score+1);
        enqueue(s);
      }
    }
    Location w = { l.X - 1, l.Y };
    if (w.X >= 0 && w.Y >= 0 && w.X < MAZE_X && w.Y < MAZE_Y && !isWall(l, WEST)) {
      if (getFlood(w) == EMPTY) {
        setFlood(w, score+1);
        enqueue(w);
      }
    }
  }
}

// TODO: get multiple routes and find the best

Step steps[4];

int routeLength;
int routeScore;

void generateRoute(Location origin, ABS_DIR abs, REL_DIR rel) {
  REL_DIR route[MAX_ROUTE_LENGTH];
  int currentVal = 0;
  Location currentLocation = origin;
  ABS_DIR currentAbs = abs;
  REL_DIR currentRel = rel;

  int targetVal = getFlood(origin);
  int currentLength = 0;
  int currentScore = 0;

  while (currentVal != -1) {
    route[currentLength] = currentRel;
    switch (currentRel) {
      case FORWARD:
        Serial.print("F");
        break;
      case RIGHT:
        Serial.print("R");
        break;
      case BACKWARD:
        Serial.print("B");
        break;
      case LEFT:
        Serial.print("L");
        break;
    }
    currentLength += 1;
    targetVal -= 1;
    int count = getSteps(currentLocation, currentAbs, targetVal);
    switch (count) {
      case 0:
        // no routes
        //Serial.println("No route");
        currentVal = -1;
        routeLength = currentLength;
        routeScore = currentScore;
        break;
      case 1:
        // one route
        //Serial.println("Single route");
        if (steps[0].Value == targetVal) {
          // found step with correct value
          if (currentAbs != steps[0].Abs) {
            currentScore += 1;
          }
          currentVal = steps[0].Value;
          currentLocation = steps[0].Coord;
          currentAbs = steps[0].Abs;
          currentRel = steps[0].Rel;
        } else {
          // step doesn't have correct value
          currentVal = -1;
          routeLength = currentLength;
          routeScore = currentScore;
        }
        break;
      default:
        // multiple routes
        //Serial.println("Multiple routes");
        // just select the first result, TODO: we should explore all routes? we should pick the best route
        if (steps[0].Value == targetVal) {
          // found step with correct value
          if (currentAbs != steps[0].Abs) {
            currentScore += 1;
          }
          currentVal = steps[0].Value;
          currentLocation = steps[0].Coord;
          currentAbs = steps[0].Abs;
          currentRel = steps[0].Rel;
        } else {
          // step doesn't have correct value
          currentVal = -1;
          routeLength = currentLength;
          routeScore = currentScore;
        }
        break;
    }
  }
  Serial.println("");
}

int getSteps(Location l, ABS_DIR facing, int requiredValue) {
  int count = 0;

  Step s;

  s = getAccessibleStep(l, NORTH, facing);
  if (s.Value != -1 && s.Value == requiredValue) {
    steps[count] = s;
    count++;
  }
  s = getAccessibleStep(l, EAST, facing);
  if (s.Value != -1 && s.Value == requiredValue) {
    steps[count] = s;
    count++;
  }
  s = getAccessibleStep(l, SOUTH, facing);
  if (s.Value != -1 && s.Value == requiredValue) {
    steps[count] = s;
    count++;
  }
  s = getAccessibleStep(l, WEST, facing);
  if (s.Value != -1 && s.Value == requiredValue) {
    steps[count] = s;
    count++;
  }

  return count;
}

Step getAccessibleStep(Location l, ABS_DIR dir, ABS_DIR facing) {
  Location neighbour = getNeighbour(l, dir);
  if (neighbour.X != -1 && neighbour.Y != -1) {
    if (!isWall(l, dir)) {
      int num = getFlood(neighbour);
      return { num, neighbour, dir, getRelDir(dir, facing)};
    }
  }
  return { -1, {0,0}, NORTH, NONE };
}

REL_DIR getRelDir(ABS_DIR dir, ABS_DIR facing) {
  switch (facing) {
    case NORTH:
      switch (dir) {
        case NORTH:
          return FORWARD;
        case EAST:
          return RIGHT;
        case SOUTH:
          return BACKWARD;
        case WEST:
          return LEFT;
      }
    case EAST:
      switch(dir) {
        case NORTH:
          return LEFT;
        case EAST:
          return FORWARD;
        case SOUTH:
          return RIGHT;
        case WEST:
          return BACKWARD;
      }
    case SOUTH:
      switch (dir) {
        case NORTH:
          return BACKWARD;
        case EAST:
          return LEFT;
        case SOUTH:
          return FORWARD;
        case WEST:
          return RIGHT;
      }
    case WEST:
      switch (dir) {
        case NORTH:
          return RIGHT;
        case EAST:
          return BACKWARD;
        case SOUTH:
          return LEFT;
        case WEST:
          return FORWARD;
      }
  }
  return NONE;
}

Location getNeighbour(Location l, ABS_DIR dir) {
  Location n;
  if (dir == NORTH) {
    n = { l.X, l.Y + 1 };
  }
  if (dir == EAST) {
    n = { l.X + 1, l.Y };
  }
  if (dir == SOUTH) {
    n = { l.X, l.Y - 1 };
  }
  if (dir == WEST) {
    n = { l.X - 1, l.Y };
  }
  if (n.X >= 0 && n.Y >= 0 && n.X < MAZE_X && n.Y < MAZE_Y) {
    return n;
  }
  return { -1, -1 };
}

void serialFlood() {
  for (int y = 0; y < MAZE_Y; y++) {
    for (int x = 0; x < MAZE_X; x++) {
      int val = getFlood({x, MAZE_Y-1-y});
      sprintf(buf, "%03d", val);
      Serial.print(buf);
      Serial.print(",");
    }
    Serial.println("");
  }
}
