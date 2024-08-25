
#define EMPTY -1
#define MAZE_X 16
#define MAZE_Y 16
#define MAX_QUEUE_LENGTH 256

enum ABS_DIR {
  NORTH = 0x01,
  EAST  = 0x02,
  SOUTH = 0x04,
  WEST  = 0x08
};

struct Location {
  byte X;
  byte Y;
};

unsigned long prevMillis = 0;

byte maze[MAZE_Y][MAZE_X] = {
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
  { 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00 },
};

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

Location dequeue() {
  // take item from front of queue
  Location location = queue[0];
  // move every item up the queue
  for (int i = 0; i < queueLength-1; i++) {
    queue[i] = queue[i+1];
  }
  // decrement the queue length
  queueLength -= 1;
  // return the location
  return location;
}

bool isWall(Location location, ABS_DIR dir) {
  return getMaze(location) & dir == dir;
}

void setup() {
  Serial.begin(115200, SERIAL_8N1);
}

void loop() {
  processFlood();
  serialFlood();
  delay(1000);
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
    int x, y;
    Location l = dequeue();
    int score = getFlood(l);
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

void serialFlood() {
  unsigned long m = millis();
  Serial.print("Flood ");
  Serial.println(m - prevMillis);
  prevMillis = m;
  for (int y = 0; y < MAZE_Y; y++) {
    for (int x = 0; x < MAZE_X; x++) {
      Serial.print(getFlood({x, y}));
      Serial.print(",");
    }
    Serial.println("");
  }
}
