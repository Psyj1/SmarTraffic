int verdeA = 9;
int amareloA = 10;
int vermelhoA = 11;

int verdeB = 3;
int amareloB = 5;
int vermelhoB = 6;

int botao = 12;

bool semaforoALivre = true; 

void setup() {
  Serial.begin(9600);
  
  pinMode(verdeA, OUTPUT);
  pinMode(amareloA, OUTPUT);
  pinMode(vermelhoA, OUTPUT);
  pinMode(verdeB, OUTPUT);
  pinMode(amareloB, OUTPUT);
  pinMode(vermelhoB, OUTPUT);
  pinMode(botao, INPUT_PULLUP);
  
  limparTodosLeds();
  
  digitalWrite(verdeA, LOW);
  digitalWrite(vermelhoB, LOW);
}

void limparTodosLeds() {
  digitalWrite(verdeA, HIGH);
  digitalWrite(amareloA, HIGH);
  digitalWrite(vermelhoA, HIGH);
  digitalWrite(verdeB, HIGH);
  digitalWrite(amareloB, HIGH);
  digitalWrite(vermelhoB, HIGH);
}

void loop() {
  if (digitalRead(botao) == LOW) {
    delay(50);
    if (digitalRead(botao) == LOW) {
      
      Serial.println("Botão pressionado!");
      
      if (semaforoALivre) {
        Serial.println("Fechando semáforo A...");
        
       
        digitalWrite(verdeA, HIGH); 
        digitalWrite(amareloA, LOW);  
        delay(2000);
        
        digitalWrite(amareloA, HIGH); 
        digitalWrite(vermelhoA, LOW); 
        
        
        digitalWrite(vermelhoB, HIGH); 
        digitalWrite(verdeB, LOW);
        
        semaforoALivre = false;
        Serial.println("Semáforo B liberado!");
      }
      else {
        Serial.println("Fechando semáforo B...");
        
        
        digitalWrite(verdeB, HIGH);
        digitalWrite(amareloB, LOW);
        delay(2000);
        
        
        digitalWrite(amareloB, HIGH); 
        digitalWrite(vermelhoB, LOW); 
        
      
        digitalWrite(vermelhoA, HIGH); 
        digitalWrite(verdeA, LOW); 
        
        semaforoALivre = true;
        Serial.println("Semáforo A liberado!");
      }
      
      
      digitalWrite(amareloA, HIGH);
      digitalWrite(amareloB, HIGH);
      
      while(digitalRead(botao) == LOW);
      delay(50);
    }
  }
}