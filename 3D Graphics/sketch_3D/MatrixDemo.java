import java.util.ArrayList;

public class MatrixDemo
{
	public static void main(String[] args) 
	{
		Matrix projMat = Matrix.full(4, 4, 0);

		double width = 1280;
		double heigth = 720;
		double fov = 45;
		double nearPlaneDist = 0.1;
		double farPlaneDist = 1000;

		double aspect = width / heigth;
		double fFov = 1/Math.tan((0.5*fov)*(Math.PI/180));
		double q = farPlaneDist / (farPlaneDist - nearPlaneDist);

		projMat.set(0,0,aspect*fFov);
		projMat.set(1,1,fFov);
		projMat.set(2,2,q);
		projMat.set(3,2,-nearPlaneDist*q);
		projMat.set(2,3,1);

		System.out.println("Projection Matrix");
		projMat.print();
		System.out.println();

		double x = 1;
		double y = 1;
		double z = 1;
		Matrix point = Matrix.full(1,4,1);
		point.set(0,0,x);
		point.set(0,1,y);
		point.set(0,2,z);
		System.out.println("Point Matrix");
		point.print();
		System.out.println();

		Matrix projectedMat = Matrix.matMul(point, projMat);
		projectedMat.sclDiv(projectedMat.get(0,3));
		//projectedMat.sclMul(50);
		System.out.println("Projected Point Matrix");
		projectedMat.print();
		System.out.println();
	}
}