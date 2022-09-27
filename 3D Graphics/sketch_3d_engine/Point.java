/**
	Represents a 3d point in space
*/

public class Point
{
	private final double x;  //x-coordinate
	private final double y; //y-coordinate
	private final double z; //z-coordinate
	private final Matrix vec; //the vector representation of the point

	public Point(double x, double y, double z)
	{
		this.x = x;
		this.y = y;
		this.z = z;
		double[][] m = {{this.x, this.y, this.z, 1}};
		vec = new Matrix(m);
	}

	//accessor methods
	public double getX(){ return x;}
	public double getY(){ return y;}
	public double getZ(){ return z;}

	//return a string representaion of this point
	public String toString()
	{
		return "(" + x + " ," + y + " ," + z + ")";
	}
  
  //return the vector represenatation of the point
  public Matrix getVec()
  {
    return vec;
  }
}
