//3d projection
Matrix projMat = Matrix.full(4, 4, 0);

double wd = 1280;
double ht = 720;
double fov = 45;
double nearPlaneDist = 0.1;
double farPlaneDist = 1000;

double aspect = ht / wd;
double fFov = 1/Math.tan((0.5*fov)*(Math.PI/180));
double q = farPlaneDist / (farPlaneDist - nearPlaneDist);

Point a = new Point(0.2, 0.2, 0);
Point b = new Point(-0.3, -0.3, 0);
Point c = new Point(0.4, -0.7, 0);
Point[] points = {a, b, c};
Matrix[] projectedPointsMatrices = new Matrix[3];

void setup()
{
    size(1280, 720);
    projMat.set(0,0,aspect*fFov);
    projMat.set(1,1,fFov);
    projMat.set(2,2,q);
    projMat.set(3,2,-nearPlaneDist*q);
    projMat.set(2,3,1);
}

void draw()
{
  frameRate(0);
  background(255);
  strokeWeight(10);
  int i = 0;
  for(Point p : points)
  {
    projectedPointsMatrices[i] = Matrix.matMul(p.getVec(), projMat);
    projectedPointsMatrices[i].sclMul(500);
    i++;
  }
  print(i);
  
  
  for(Matrix p : projectedPointsMatrices)
  {
    point((float)(p.get(0,0)), (float)(p.get(0,1)));
    println((float)(p.get(0,0))+ " " + (float)(p.get(0,1)));
  }
}
