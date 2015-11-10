#include <stdio.h>
#include <string.h>
#include <stdlib.h>
/*do GF(2^128) calculation*/

void printHex(unsigned char *p, int len) {
  int i;
  for (i = 0; i < len; i++) {
      printf("%02x", p[i]);
      }

}


char Hex2Int(char p) {
  if(p < 58 && p > 47)
    return (p - 48);
  else if (p < 103 && p > 96)
    return 10 + (p - 97);
  else
    printf("error: input contains invalid char\n");
}

unsigned char *HexHandler(char *p, int *alen){
  int len = strlen(p);
  if(len%2 != 0) {
    printf("error: input hex string is wrong!\n");
    return 0;
  }
  
  *alen = len/2;
  unsigned char *str = (unsigned char *) malloc(len/2);
  
  
  
  int i;
  for(i = 0; i < len; i = i+2) {
    str[i/2] = Hex2Int(p[i]) * 16 + Hex2Int(p[i+1]);
  }

  return str;
}



int TestBit(unsigned char *p, int i);

/* 128 to the block and index into a 16 array*/



void PrintBit(unsigned char *p) {
  int i;
  for(i = 0; i < 128; i++) {
    printf("%d", TestBit(p, i));
  }
  printf("\n");
}


int TestBit(unsigned char *p, int i) {
  int block = i/8;
  int position = i%8;
  return ( p[block] >> (7 - position) ) & 1;
}

int SetBit(unsigned char *p, int i) {
  int block = i/8;
  int position = i%8;
  p[block] = p[block] | ( 1<< (7 - position) );
}

// suppose A and B all 16 bytes
void XOR(unsigned char *A, unsigned char *B) {
  int i;
  for(i = 0; i < 16; i++) {
    A[i] = A[i] ^ B[i];
  }
}


// shift to right one bit, and add 0 for the leading empty
// suppose p has 16 elements
void RightShift(unsigned char *p) {
  unsigned char temp[16] = {0};
  int i;
  for(i = 0; i < 127; i++) {
    if(TestBit(p, i)) {
      SetBit(temp, i + 1);
    }
  }
  memcpy(p, temp, 16);
}

int GF(unsigned char *Y, unsigned char *X, unsigned char *Z) {

  // suppose input = Y, H is X
  unsigned char V[16];
  unsigned char R[16] = {225};

  memcpy(V, X, 16);

  memset(Z, 0, 16);

  int i;
  for(i = 0; i < 128; i++) {
    if(TestBit(Y, i)) {
      XOR(Z, V);
    }
    if(!TestBit(V, 127)) {
      RightShift(V);
    }
    else {
      RightShift(V);
      XOR(V, R);
    }
  }
}


// assumption:
// aad is only 16 bytes
// ciphertext is no longer than 8192
void main (int argc, char **argv) {
  int H_len; 
  unsigned char *H = HexHandler(argv[1], &H_len);
//  printf("H length is: %d\n", H_len);
  int aad_len;
  unsigned char *aadin = HexHandler(argv[2], &aad_len);
  
  int cipher_len;
  unsigned char *cipher = HexHandler(argv[3], &cipher_len);



  int cipherin_len = 16*(cipher_len/16 + 1);
  unsigned char *cipherin = (unsigned char *) malloc(cipherin_len);
  memset(cipherin, 0, cipherin_len);
  memcpy(cipherin, cipher, cipher_len);

  unsigned char X[16] = {0};
  unsigned char temp[16];

  unsigned char len[16] = {0, 0, 0, 0, 0, 0, 0, 104, 0, 0, 0, 0, 0, 0, 0, 0};
  len[14] = (cipher_len*8)/256; 
  len[15] = (cipher_len*8)%256;

//  printHex(H, H_len);
//  printHex(aadin, aad_len);
//  printHex(cipher, cipher_len);

  
  GF(aadin, H, X);
 
   
  int i;
  for(i = 0; i < cipherin_len/16; i++) {
    XOR(X, cipherin + 16*i);
    GF(X, H, temp);
    memcpy(X, temp, 16);
  }

  XOR(X, len); 
  GF(X, H, temp);
  memcpy(X, temp, 16);

//  PrintBit(X);
  printHex(X, 16);
}
