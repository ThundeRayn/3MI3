#include <stdio.h>

int main()
{
    int arr[5] = {0,1,2,3,4}; //a static one dim array
    printf("%d",arr[0]); //returns 0
    printf("%d",arr[1]); //returns 1
    printf("%d",arr[2]); //returns 2
    printf("%d",arr[3]); //returns 3
    printf("%d",arr[4]); //returns 4
    //*when out of bound
    printf("%d",arr[5]); //returns 32766 or another random number but not an error. 
    printf("%d",arr[-1]); //returns 22060 or another random number but not an error.

    //this indicates that C/C++ does not check the index range for static one-dimensional arrays
    return 0;
}
