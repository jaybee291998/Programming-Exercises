// The Nature of Code
// Daniel Shiffman
// http://natureofcode.com

class Neuron {
  PVector position;

  ArrayList<Connection> connections;

  Neuron(float x, float y) {
    position = new PVector(x, y);
    connections = new ArrayList<Connection>();
  }

  void connect(Neuron n) {
    Connection c = new Connection(this, n, random(1));
    connections.add(c);
  } 

  void display() {
    stroke(0);
    strokeWeight(1);
    fill(0);
    ellipse(position.x, position.y, 16, 16);

    for (Connection c : connections) {
      c.display();
    }
  }
}

