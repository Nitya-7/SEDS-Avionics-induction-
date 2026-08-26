#include <LiquidCrystal.h>

const int LCD_RS = 12;
const int LCD_EN = 11;
const int LCD_D4 = 5;
const int LCD_D5 = 4;
const int LCD_D6 = 3;
const int LCD_D7 = 2;

LiquidCrystal lcd(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7);

const int LDR_PIN = A0;
const int TRIG_PIN = 9;
const int ECHO_PIN = 10;
const int BUTTON_PIN = 7;
const int LED_PIN = 8;
const int BUZZER_PIN = 6;

const int LIGHT_THRESHOLD = 512;
const int DISTANCE_THRESHOLD_CM = 100;
const unsigned long WRECK_TIME_MS = 5000;

const int OPEN_SEA = 0;
const int ANCHOR_DROPPED = 1;
const int STORM = 2;
const int CHARYBDIS = 3;
const int WRECKED = 4;

int currentState = OPEN_SEA;

bool anchorDown = false;

bool lastButtonReading = HIGH;
unsigned long lastDebounceTime = 0;
const unsigned long DEBOUNCE_MS = 50;

unsigned long dangerStartTime = 0;

unsigned long lastBlinkTime = 0;
bool ledOn = false;
const unsigned long BLINK_INTERVAL_MS = 300;


void setup() {
  lcd.begin(16, 2);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  Serial.begin(9600);

  showState();
}


void loop() {

  if (currentState == WRECKED) {
    digitalWrite(LED_PIN, LOW);
    noTone(BUZZER_PIN);
    return;
  }

  handleButton();

  int lightLevel = analogRead(LDR_PIN);
  long distanceCm = readDistanceCm();

  bool stormCondition = lightLevel < LIGHT_THRESHOLD;

  bool charybdisCondition =
    distanceCm > 0 &&
    distanceCm < DISTANCE_THRESHOLD_CM;

  if (anchorDown) {

    digitalWrite(LED_PIN, LOW);
    noTone(BUZZER_PIN);

  } else {

    updateDangerState(stormCondition, charybdisCondition);
  }

  showState();

  delay(100);
}


void handleButton() {

  bool reading = digitalRead(BUTTON_PIN);

  if (reading != lastButtonReading) {
    lastDebounceTime = millis();
  }

  if ((millis() - lastDebounceTime) > DEBOUNCE_MS) {

    static bool stableState = HIGH;

    if (reading != stableState) {

      stableState = reading;

      if (stableState == LOW) {
        toggleAnchor();
      }
    }
  }

  lastButtonReading = reading;
}


void toggleAnchor() {

  anchorDown = !anchorDown;

  if (anchorDown) {
    currentState = ANCHOR_DROPPED;
  } else {
    currentState = OPEN_SEA;
  }
}


void updateDangerState(
  bool stormCondition,
  bool charybdisCondition
) {

  bool inStorm = (currentState == STORM);
  bool inCharybdis = (currentState == CHARYBDIS);

  if (!inStorm && !inCharybdis) {

    if (stormCondition) {

      enterDanger(STORM);

    } else if (charybdisCondition) {

      enterDanger(CHARYBDIS);

    } else {

      currentState = OPEN_SEA;
    }

    return;
  }

  bool stillActive;

  if (inStorm) {
    stillActive = stormCondition;
  } else {
    stillActive = charybdisCondition;
  }

  if (!stillActive) {

    currentState = OPEN_SEA;

    digitalWrite(LED_PIN, LOW);
    noTone(BUZZER_PIN);

    return;
  }

  if (millis() - dangerStartTime >= WRECK_TIME_MS) {

    currentState = WRECKED;

    return;
  }

  if (inStorm) {

    blinkLed();
    noTone(BUZZER_PIN);

  } else {

    digitalWrite(LED_PIN, LOW);
    tone(BUZZER_PIN, 1000);
  }
}


void enterDanger(int newState) {

  currentState = newState;
  dangerStartTime = millis();
}


void blinkLed() {

  if (millis() - lastBlinkTime >= BLINK_INTERVAL_MS) {

    lastBlinkTime = millis();

    ledOn = !ledOn;

    digitalWrite(
      LED_PIN,
      ledOn ? HIGH : LOW
    );
  }
}


long readDistanceCm() {

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);

  digitalWrite(TRIG_PIN, LOW);

  long duration = pulseIn(
    ECHO_PIN,
    HIGH,
    30000
  );

  if (duration == 0) {
    return -1;
  }

  return duration * 0.034 / 2;
}


void showState() {

  static int lastShown = -1;

  if (currentState == lastShown) {
    return;
  }

  lastShown = currentState;

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print("State:");

  lcd.setCursor(0, 1);

  if (currentState == OPEN_SEA) {

    lcd.print("OPEN SEA");

  } else if (currentState == ANCHOR_DROPPED) {

    lcd.print("ANCHOR DROPPED");

  } else if (currentState == STORM) {

    lcd.print("STORM");

  } else if (currentState == CHARYBDIS) {

    lcd.print("CHARYBDIS");

  } else if (currentState == WRECKED) {

    lcd.print("WRECKED");
  }
}