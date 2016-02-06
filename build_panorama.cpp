#include <stdio.h>  
#include <opencv2/opencv.hpp>  
#include <opencv2/stitching/stitcher.hpp>

#ifdef _DEBUG  
#pragma comment(lib, "opencv_core246d.lib")   
#pragma comment(lib, "opencv_imgproc246d.lib")   //MAT processing  
#pragma comment(lib, "opencv_highgui246d.lib")  
#pragma comment(lib, "opencv_stitching246d.lib");

#else  
#pragma comment(lib, "opencv_core246.lib")  
#pragma comment(lib, "opencv_imgproc246.lib")  
#pragma comment(lib, "opencv_highgui246.lib")  
#pragma comment(lib, "opencv_stitching246.lib");
#endif  

using namespace cv;  
using namespace std;


int main()  
{
 vector< Mat > vImg;
 Mat rImg;

// vImg.push_back( imread("./workspace/r30.jpg") );
 vImg.push_back( imread("./workspace/r45.jpg") );
 vImg.push_back( imread("./workspace/r90.jpg") );
 vImg.push_back( imread("./workspace/r135.jpg") );
 //vImg.push_back( imread("./workspace/r150.jpg") );
  

 Stitcher stitcher = Stitcher::createDefault();


 unsigned long AAtime=0, BBtime=0; //check processing time
 AAtime = getTickCount(); //check processing time

 Stitcher::Status status = stitcher.stitch(vImg, rImg);

 BBtime = getTickCount(); //check processing time 
 printf("%.2lf sec \n",  (BBtime - AAtime)/getTickFrequency() ); //check processing time

 if (Stitcher::OK == status) 
  imwrite("workspace/result.jpg",rImg);
  else
  printf("Stitching fail.");


}  

