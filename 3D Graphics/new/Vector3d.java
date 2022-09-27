public class Vector3d
{
	private double[] v = new double[3]; // x,y,z
	private Matrix matrixForm;

	public Vector3d(double x, double y, double z)
	{
		v[0] = x;
		v[1] = y;
		v[2] = z;

		double[][] m = {{x,y,z}};
		matrixForm = new Matrix(m);
	}

	/**
		add a vector to the vector
		@param vector
	*/
	public void addVector(Vector3d vector)
	{
		v[0] += vector.getComp(0);
		v[1] += vector.getComp(1);
		v[2] += vector.getComp(2);
	}

	/**
		subtracta a vector to the vector
		@param vector
	*/
	public void subtractVector(Vector3d vector)
	{
		v[0] -= vector.getComp(0);
		v[1] -= vector.getComp(1);
		v[2] -= vector.getComp(2);
	}

	/**
		return the specified component
		@param i
		@return componnt
	*/
	public double getComp(int i)
	{
		return v[i];
	}

	/**
		return the matrix form of the vector
		@return matrix
	*/
	public Matrix getMatrixForm()
	{
		return matrixForm;
	}

	/**
		return the string representation of  the vector
		@return str
	*/
	public String toString()
	{
		return "<" + v[0] + "," + v[1] + "," + v[2] + ">";
	}

}