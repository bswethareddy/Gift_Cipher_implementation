#include<bits/stdc++.h>
#define NUM 16
using namespace std;
int Sbox[NUM] = {1,10, 4, 12, 6, 15, 3, 9, 2,13, 11, 7, 5, 0, 8, 14}; //mySbox

int InfluenceMat[NUM][4];
int DDT[NUM][NUM];
void printMat(); //utility function to print the DDT matrix
void findDDT();  // function to find the DDT matrix
void findInfluenceMat(int diff); //function to find the influence box of Sbox
// given one difference value and
// populates the entries of DDT based on frequencies
// of the output difference values.

void printTransitions(); // prints the transitions that give the maximum differential probability
int main()
{
  //initialising the matrices with 0
  memset(InfluenceMat,0,sizeof(InfluenceMat));
  memset(DDT,0,sizeof(DDT));

  findDDT();
  printMat();
  printTransitions();

  return 0;
}
void findDDT()
{
    int i,j;
    for(i=0;i<NUM;i++)
    findInfluenceMat(i);
}

void findInfluenceMat(int diff)
{
  int i;
  for(i=0;i<NUM;i++)
  {
    InfluenceMat[i][0] = i ^ diff;
    InfluenceMat[i][1] = Sbox[i];
    InfluenceMat[i][2] = Sbox[InfluenceMat[i][0]];
    InfluenceMat[i][3] = InfluenceMat[i][1] ^ InfluenceMat[i][2];
  }

  for(i=0;i<NUM;i++)
    DDT[diff][InfluenceMat[i][3]]++;
}


void printMat()
{
  int i,j;
  cout << "in\\out \t\t";
  for(i=0;i<NUM;i++)
   cout<< i<<"\t";
  cout<<endl<<endl;
  for(i=0;i<NUM;i++)
  {
    cout << i<<"\t\t";
    for(j=0;j<NUM;j++)
    {
      if(DDT[i][j]==0)
      cout<<"-\t";
      else
      cout << DDT[i][j]<<"\t";
    }
    cout<<endl;
  }
}

void printTransitions()
{
  vector<pair<int,int> > v;
  int i,j,maxele = INT_MIN;
  for(i=0;i<NUM;i++)
  {
    for(j=0;j<NUM;j++)
    {
      if( DDT[i][j] != 16 && maxele < DDT[i][j]  )
      {
        maxele = DDT[i][j];
        v.clear();
      }
      if(maxele == DDT[i][j])
       v.push_back(make_pair(i,j));
    }
  }
  cout << "The transitions that give the maximum differential probability of Gift cipher Sbox is -"<<endl;
  for(vector<pair<int,int> >::iterator it = v.begin(); it!=v.end();it++)
   cout << (*it).first <<"--->"<< (*it).second<<endl;
  cout << "The maximum differential probability is = "<<maxele<<"/"<<NUM<<endl;
}