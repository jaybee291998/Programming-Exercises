//initialize all the vertices
Point a = new Point(1,0,0);
Point b = new Point(1,1,0);
Point c = new Point(0,1,0);
Point d = new Point(0,1,1);
Point e = new Point(0,0,1);
Point f = new Point(1,0,1);
Point g = new Point(1,1,1);
Point h = new Point(0,0,0);

//initialize all the triangles

//East
Triangle eastTop = new Triangle(a,f,g);
Triangle eastBot = new Triangle(a,g,b);

//north
Triangle northTop = new Triangle(b,g,d);
Triangle northBot = new Triangle(b,d,c);

//top
Triangle topTop = new Triangle(f,e,d);
Triangle topBot = new Triangle(f,d,g);

//west
Triangle westTop = new Triangle(h,e,d);
Triangle westBot = new Triangle(h,d,c);

//south
Triangle southTop = new Triangle(h,e,f);
Triangle southBot = new Triangle(h,f,a);

//bottom
Triangle botTop = new Triangle(a,h,c);
Triangle botBot = new Triangle(a,c,b);

//3d projection
     Matrix projMat = Matrix.full(4, 4, 0);

    double wd = 1280;
    double ht = 720;
    double fov = 45;
    double nearPlaneDist = 0.1;
    double farPlaneDist = 1000;

    double aspect = wd / ht;
    double fFov = 1/Math.tan((0.5*fov)*(Math.PI/180));
    double q = farPlaneDist / (farPlaneDist - nearPlaneDist);
    Mesh mesh;

void setup()
{
  size(1280, 720);
  ArrayList<Triangle> m = new ArrayList<Triangle>();
  m.add(eastTop); m.add(eastBot);
  m.add(northTop); m.add(northBot);
  m.add(topTop); m.add(topBot);
  m.add(westTop); m.add(westBot);
  m.add(southTop); m.add(southBot);
  m.add(botTop); m.add(botBot);
  
  mesh = new Mesh(m);
  
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
  
  for(Triangle tri : mesh.getTriangles())
  {
    Matrix[] projPt = new Matrix[3];
    int i = 0;
    for(Matrix p : tri.getPoints())
    {
      println(p.get(0,2));
      p.set(0,2,p.get(0,2)+2);
      println(p.get(0,2));
      projPt[i] = Matrix.matMul(p, projMat);
      
      projPt[i].set(0,0,(projPt[i].get(0,0)+1)*0.5*wd*0.25);
      projPt[i].set(0,1,(projPt[i].get(0,1)+1)*0.5*wd*0.25);
      i++;
    }
    triangle((float)(projPt[0].get(0,0)), (float)(projPt[0].get(0,1)),(float)(projPt[1].get(0,0)), (float)(projPt[1].get(0,1)),(float)(projPt[2].get(0,0)), (float)(projPt[2].get(0,1)));
  }
  
  
}
