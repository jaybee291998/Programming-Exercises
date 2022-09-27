Population pop;
PFont f;
String target;
int popmax;
float mutationRate;
int i;
void setup(){
  size(640, 360);
  f = createFont("Courier", 32, true);
  
  target = "to be or not to be";
  popmax = 150;
  mutationRate = 0.01;
  
  pop = new Population(target, mutationRate, popmax);
  i = 0;
  
}

void draw(){
   pop.calcFitness();
   pop.createMatingPool();
   pop.reproduce();
   displayInfo();
}

void displayInfo(){
  background(255);
  
  String answer = pop.getBest().toString();
  textFont(f);
  textAlign(LEFT);
  fill(0);
  
  textSize(24);
  text("Best phrase:",20,30);
  textSize(40);
  text(answer, 20, 100);
  
  textSize(18);
  text("total generations:  " + pop.getGenerations(), 20, 160);
  text("average fitness:    " + nf(pop.getAverageFitness(), 0, 2), 20, 180);
  text("total population:   " + popmax, 20, 200);
  text("mutation rate:      " + int(mutationRate * 100) + "%", 20, 220);
  
  textSize(10);
  text("All phrases:\n" + pop.allPhrases(), 500, 10);
}
