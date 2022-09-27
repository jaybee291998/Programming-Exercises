public class Population{
  private DNA[] population;
  private ArrayList<DNA> matingPool = new ArrayList<DNA>();
  private int generations = 0;
  private String target;
  private float mutationRate;

  public Population(String target, float mutationRate, int size){
    population = new DNA[size];
    this.target = target;
    this.mutationRate = mutationRate;
    for(int i = 0; i < population.length; i++){
      population[i] = new DNA(target.length());
    }
  }
  public void calcFitness(){
    for(DNA member : population){
      member.fitness(target);
    }
  }
  public void createMatingPool(){
    matingPool.clear();
    float maxFitness = getBest().getFitness();
    for(DNA member : population){
      float fitness = map(member.getFitness(),0,maxFitness,0,1);
      int n = int (fitness*100);
      for(int i = 0; i < n; i++)
        matingPool.add(member);
    }
  }
  
  public void reproduce(){
    // choose the parents
    for(int i = 0; i < population.length; i++){
      DNA parent1 = matingPool.get(int (random(matingPool.size())));  // choose a random parent from the matingpool
      DNA parent2 = matingPool.get(int (random(matingPool.size())));
      DNA child = parent1.crossover(parent2);
      child.mutate(mutationRate);
      population[i] = child;
    }
    generations++;
  }
  
  public DNA getBest(){
    DNA best = population[0];
    for(int i = 1; i < population.length; i++){
      if(population[i].getFitness() > best.getFitness()) best = population[i];
    }
    return best;
  }
  
  public DNA getMember(int index){
    if(index < 0 || index >= population.length) throw new IllegalArgumentException("Index not found");
    return population[index];
  }
  
  public int getSize(){
    return population.length;
  }
  
  public int getGenerations(){
    return generations;
  }
  
  public float getAverageFitness(){
    float total = 0;
    for(DNA member : population){
      total += member.getFitness();
    }
    
    return total / (population.length);
  }
  
  public String allPhrases(){
    String everything = "";
    
    int displayLimit = min(population.length, 50);
    
    for(int i = 0; i < displayLimit; i++){
      everything += population[i].toString() + "\n";
    }
    
    return everything;
  }
  
  public String toString(){
    String str = "";
    for(DNA member : population){
      str += String.format("%s\tfitness: %.02f\n", member.toString(), member.getFitness());
    }
    str += String.format("\nMating Pool\n");
    // for matingpool
    for(DNA member : matingPool){
      str += String.format("%s\n", member.toString());
    }
    return str;
  }
}
