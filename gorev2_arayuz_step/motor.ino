#include<AccelStepper.h>

//Tum pinler, spd rastgele deger icin sayi secmesi adina rastgele bir analog pine atandi,
//pinden gelen noise sayi uretimini sagliyor
int PULpin = 2;
int DIRpin = 3;
int spd = A0;

int pd = 500;
int spr = 1600;
int rpm = 10;

//python koduyla iletisim
const unsigned long RAPOR_PERIYODU = 100;
unsigned long son = 0;

String girdisatiri = "";

enum Mod {DUR, SERBEST, HEDEF};

Mod mod = DUR;

AccelStepper stepper(AccelStepper::DRIVER, PULpin, DIRpin);


boolean setdir = LOW;

void setdir_change(){
    setdir = !setdir;
}

//rastgele hizlanma saglamak adina fonksiyon
void random_yon(){
    int dir = random(0, 2) == 0 ? 1 : -1;
    float rev_saniye = random(25, 150) / 100.0;
    long hiz = dir * (rev_saniye * spr);
    stepper.setSpeed(hiz);
    mod = SERBEST;
}


//Pythondan gelen komutlarin taninmasi ve gorev secimi
void komutIsle(String komut){
    komut.trim();
    if(komut == "BASLA"){
        random_yon();
    }
    else if(komut == "DUR"){
        motoruDurdur();
    }
    else if(komut.startsWith("GIT ")){
        long hedef = komut.substring(4).toInt();
        hedefeGit(hedef);
    }
    else if(komut.startsWith("KONUM ")){
        long konum = komut.substring(6).toInt();
        stepper.setCurrentPosition(konum);
        durumYolla();
    }


}


//MOTOR GOREVLERI
void motoruDurdur(){
    stepper.setSpeed(0);
    stepper.stop();
    mod = DUR;
    durumYolla();
}

void hedefeGit(long hedef){
    stepper.setMaxSpeed(1600);
    stepper.setAcceleration(200);
    stepper.moveTo(hedef);
    mod = HEDEF;
}


//arayuz icin bilgi
void durumYolla(){
    Serial.print("KONUM: ");
    Serial.println(stepper.currentPosition());
    Serial.print("DURUM: ");
    Serial.println(mod == DUR ? "DURUYOR" : "AKTIF");
}

void setup() {
    Serial.begin(115200);
    randomSeed(analogRead(A0));
    stepper.setMaxSpeed(1000);
    stepper.setAcceleration(200);
}

void loop(){ 
    while (Serial.available()){
        char c = Serial.read();
        if (c == '\n'){
            komutIsle(girdisatiri);
            girdisatiri = "";
        }else if(c != '\r'){
            girdisatiri += c;
        }
    }
    if(mod == SERBEST){
        stepper.runSpeed();
    }
    else if(mod == HEDEF){
        if (stepper.distanceToGo() != 0) {
            stepper.run();
        } else {
            mod = DUR;
            durumYolla();
        }
    }

    unsigned long now = millis();
    if (now - son >= RAPOR_PERIYODU){
        durumYolla();
        son = now;
    }
}