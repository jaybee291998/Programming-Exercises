public class DNA {
  private char[] genes;
  private float fitness = 0;
  public DNA(int num) {
    genes = new char[num];
    for(int i = 0; i < genes.length; i++) {
      genes[i] = (char) random(32, 128);
    }
  }
  
  public DNA(char[] genes){
    this.genes = genes;
  }
  
  public void fitness(String target){
    int score = 0;
    for(int i = 0; i < target.length(); i++)
      if(genes[i] == target.charAt(i)) score++;
    fitness = float (score)/(float) genes.length;
  }
  
  public DNA crossover(DNA other){
    char[] newGenes = new char[genes.length];
    char[] otherGenes = other.getGenes();
    for(int i = 0; i < genes.length; i++){
      newGenes[i] = int(random(2)) == 1 ? genes[i] : otherGenes[i];
    }
    return new DNA(newGenes);
  }
  
  public void mutate(float mutationRate){
    for(int i = 0; i < genes.length; i++){
      if(random(1) < mutationRate) genes[i] = (char) random(32, 128);
    }
  }
 
  
  public char[] getGenes(){
    return genes;
  }
  
  public float getFitness(){
    return fitness;
  }
  
  public String toString(){
    return new String(genes);
  }
}
