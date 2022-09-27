public class Point3d
{
	private double[] p = new double[3]; //(x,y,z)

	public Point3d(double x, double y, double z)
	{
		p[0] = x;
		p[1] = y;
		p[2] = z;	}

	/**
		add a vector to the point
		@param vector
		@return newPoint
	*/
	public void addVectorToPoint(Vector3d vector)
	{
		p[0] += vector.getComp(0);
		p[1] += vector.getComp(1);
		p[2] += vector.getComp(2);
	}

	/**
		subtract a vector to the point 
		@param vector
		@return newPoint
	*/
	public void subtractVectorToPoint(Vector3d vector)
	{
		p[0] -= vector.getComp(0);
		p[1] -= vector.getComp(1);
		p[2] -= vector.getComp(2);
	}

	/**
		substracts a given point from the point
		@param point
		@return vector
	*/
	public Vector3d subtractPointToPoint(Point3d point)
	{
		double vectorX = p[0] - point.getComp(0);
		double vectorY = p[1] - point.getComp(1);
		double vectorZ = p[2] - point.getComp(2);

		Vector3d vector = new Vector3d(vectorX, vectorY, vectorZ);
		return vector;
	}

	/**
		returns the specified component of the point
		@param i
		@return component
	*/
	public double getComp(int i)
	{
		return p[i];
	}

	/**
		reutrns a string represenation of the point
		@return str
	*/
	public String toString()
	{
		return "(" + p[0] + "," + p[1] + "," + p[2] + ")";
	}
}