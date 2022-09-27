import java.util.ArrayList;

public class PointDemo
{
	public static void main(String[] args) 
	{
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

		ArrayList<Triangle> m = new ArrayList<Triangle>();
		m.add(eastTop); m.add(eastBot);
		m.add(northTop); m.add(northBot);
		m.add(topTop); m.add(topBot);
		m.add(westTop); m.add(westBot);
		m.add(southTop); m.add(southBot);
		m.add(botTop); m.add(botBot);

		Mesh mesh = new Mesh(m);
		System.out.println(mesh);

		//3d projection
		double height = 720;
		double width = 1280;
		double fov = 90;
		double Zn = 1;
		double Zf = 1000;

		double aspect = width/height;
		double fFov = 1 / Math.tan((0.5 * fov)/(180 * 3.14159));
		double q = Zf / (Zf - Zn);

		double[][] proj = {
							{aspect*fFov,0, 	0, 			0},
							{0,			fFov,	0,			0},
							{0,			0,		q,			0},
							{0,			0,		-1*Zn*q,	0}};
		Matrix projMat = new Matrix(proj);

		projMat.print();
	}
}