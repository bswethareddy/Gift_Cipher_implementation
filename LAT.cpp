#include<bits/stdc++.h>
#define NUM 16
using namespace std;
int Sbox[NUM] = {1,10, 4, 12, 6, 15, 3, 9, 2,13, 11, 7, 5, 0, 8, 14}; //mySbox from Assignment 4 Question 2
int LAT[NUM-1][NUM-1];
void printMat(); //utility function to print the LAT matrix
void findLAT();  // function to find the LAT matrix
int dot(int a,int b); //implements the dot function i.e. the matrix multiplication with xor instead of
                      // addition

int main()
{
  //initialising the matrices with 0
  memset(LAT,0,sizeof(LAT));

  findLAT();
  printMat();

  return 0;
}
int dot(int a,int b)
{
  int count=0,temp = a&b;
  // efficient algorithm to find the number of set bits complexity = O(number of set bits)
  while(temp)
  {
    temp &= (temp-1) ;
    count++;
  }
  if(count&1)
   return 1;
  else
   return 0;
}

void findLAT()  // finds the LAT
{
  int alpha,beta,x,count=0;
  for(alpha=1;alpha<NUM;alpha++)  // rows of LAT
  {
    for(beta=1;beta<NUM;beta++)  //columns of LAT
    {
      count=0;
      for(x=0;x<NUM;x++)   //for every plaintext
      {
        if(dot(alpha,x)==dot(beta,Sbox[x]))
         count++;
      }
      LAT[alpha-1][beta-1]=count-8;
    }
  }
}

void printMat() // prints the LAT
{
  int i,j;
  cout << "\u03B1\\\u03B2\t\t";
  for(i=1;i<NUM;i++)
   cout<< std::hex <<i<<"\t";
  cout<<endl<<endl;
  for(i=0;i<NUM;i++)
  {
    cout <<std::hex<<i<<"\t\t";
    for(j=0;j<NUM;j++)
    {
      if(LAT[i-1][j-1]==0)
      cout<<"-\t";
      else
      cout << std::dec <<LAT[i-1][j-1]<<"\t";
    }
    cout<<endl<<endl;
  }
}
