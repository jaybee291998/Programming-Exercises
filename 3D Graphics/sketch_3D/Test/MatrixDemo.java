public class MatrixDemo
{
	public static void main(String[] args) 
	{
		double[][] m = {{1,2,3}};
		Matrix pointVec = new Matrix(m);

		double[][] p = {{2,4,6},
						{3,6,9},
						{4,8,12}};
		Matrix proj = new Matrix(p);

		Matrix point =  Matrix.matMul(pointVec, proj);

		point.print();
	}
}