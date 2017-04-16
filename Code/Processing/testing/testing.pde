PGraphics screen;
PImage track;
Data data = new Data();

float x = -110.789387;
float y = 32.036847;

float[] a = new float[30];
float[] b = new float[30];
float[] c = new float[30];
float[] d = new float[3];

int j = 0;
int imgWidth;
int imgHeight;

void setup() {
  track=loadImage("track.PNG");
  imgWidth = track.width;
  imgHeight = track.height;
  String lines[] = loadStrings("gps.txt");
  
  data.carSize = 50;
  data.gpsSize = 250;
  data.zoomLevel = 4;
  //size(1920, 1080);
  fullScreen();
  translate(width/2, height - 100);
  screen = createGraphics(40, 40);
  drawScreen();
  
  
  for (int i = 0 ; i < lines.length; i++) {
    d = float(split(lines[i], ','));
    a[i] = d[0];
    b[i] = d[1];
    c[i] = d[2];
  }
}

void draw() {
  translate(width/2, height - 100);
  background(51);
  drawMap(a[j],b[j],radians(c[j]));
  //drawMap(32.036707,-110.789200,radians(-320));
  drawScreen();
  j = (j + 1)%30;
}

void drawScreen(){
  screen.beginDraw();
  fill(0,0,255);
  drawTriangle(0,0,data.carSize);
  drawSpeed(35);
  screen.endDraw();
  image(screen,0,0);
}

void drawTriangle(float x,float y,float d){
  triangle(x,y-d,x+d,y+d,x-d,y+d);  
}

void drawSpeed(int speed){
  textSize(data.gpsSize);
  textAlign(RIGHT, TOP);
  fill(255);  
  for(int x = -1; x < 2; x++){
    text(speed,width/2+4*x,-height+100);
    text(speed,width/2,0-height+100+4*x);
  }
  fill(0);
  text(speed,width/2,-height+80);
}

void drawMap(float y, float x, float heading){
  float xCord;
  float yCord;
  
  yCord = map(y,32.038455,32.036126,0,1284* data.zoomLevel);
  xCord = map(x,-110.790496,-110.787323,0,1474* data.zoomLevel); 
  track.resize(int(imgWidth * data.zoomLevel), int(imgHeight * data.zoomLevel));
  rotate(heading);
  image(track, -xCord,-yCord);
  rotate(-heading);
}