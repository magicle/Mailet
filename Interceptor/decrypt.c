// do gcm mode encryption


#include <openssl/evp.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>




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








void printHex(unsigned char *p, int len) {
  int i;
  for (i = 0; i < len; i++) {
    printf("%02x", p[i]);
  }
  printf("\n");
}
void handleErrors() {  
  printf("error!\n");
}


/*
 * flag = 0 ecb dec
 * flag = 1 ctr dec
 *
 * */


int decrypt(unsigned char *ciphertext, int ciphertext_len, unsigned char *key,
  unsigned char *iv, unsigned char *plaintext, int flag)
{
  EVP_CIPHER_CTX *ctx;

  int len;

  int plaintext_len;

  /* Create and initialise the context */
  if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

  /* Initialise the decryption operation. IMPORTANT - ensure you use a key
   * and IV size appropriate for your cipher
   * In this example we are using 256 bit AES (i.e. a 256 bit key). The
   * IV size for *most* modes is the same as the block size. For AES this
   * is 128 bits */
  if(flag == 0) {
    if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, iv))
      handleErrors();
  }
  if(flag == 1) {
    if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_128_ctr(), NULL, key, iv))
      handleErrors();
  }

  /* Provide the message to be decrypted, and obtain the plaintext output.
   * EVP_DecryptUpdate can be called multiple times if necessary
   */
  if(1 != EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len))
    handleErrors();
  plaintext_len = len;

  /* Finalise the decryption. Further plaintext bytes may be written at
   * this stage.
   */
  if(1 != EVP_DecryptFinal_ex(ctx, plaintext + len, &len)) handleErrors();
  plaintext_len += len;

  /* Clean up */
  EVP_CIPHER_CTX_free(ctx);

  return plaintext_len;
}




  

void main(int argc, char **argv) {
    
  int cipher_len;
  unsigned char *cipher = HexHandler(argv[1], &cipher_len);

  // counter = iv1 | iv2
  int counter_len = 16;
  unsigned char *counter = HexHandler(argv[2], &counter_len);
  
  int key_len;
  unsigned char *key = HexHandler(argv[3], &key_len);

  unsigned char plain[4096];


 

  
//  printf("counter is: ");
//  printHex(counter, 16);
//
//  printf("key is: ");
//  printHex(key, 16);
//
//  printf("cipher is: ");
//  printHex(cipher, cipher_len);




  decrypt(cipher, cipher_len, key, counter, plain, 1);

  printHex(plain, cipher_len);


/*
  unsigned char *cipher = "\x61\x61\x61\x61\x61\x61\x61\x61\x61\x61";
  int cipher_len = 10;
  unsigned char *key = "\xde\xbc\xff\x7f\x41\xfd\x39\x45\xa8\x36\x75\x7c\xf1\x28\x08\x97";

  
  unsigned char plain[1024];
  
  unsigned char *counter = "\x37\x74\xC1\xF8\x15\xF8\x93\x24\x69\xFD\xA8\x09\x00\x00\x00\x02";
  
  decrypt(cipher, 10, key, counter, plain, 1);

 printHex(plain, 10);
*/


}
