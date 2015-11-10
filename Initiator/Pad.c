#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <openssl/evp.h>


/*Initiator generates H*/

void printHex(unsigned char *p, int len) {
 int i;
 for (i = 0; i < len; i++) {
   printf("%02x", p[i]);
 }
 printf("\n");

}




void handleErrors() {
  printf("error: in EVP usage!\n");
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


int encrypt(unsigned char *plaintext, int plaintext_len, unsigned char *key,    unsigned char *iv, unsigned char *ciphertext, int flag)
{
  EVP_CIPHER_CTX *ctx;

  int len;

  int ciphertext_len;

  /* Create and initialise the context */
  if(!(ctx = EVP_CIPHER_CTX_new()))
    handleErrors();

  /* Initialise the encryption operation. IMPORTANT - ensure you use a key
   *    * and IV size appropriate for your cipher
   *       * In this example we are using 256 bit AES (i.e. a 256 bit key). The
   *          * IV size for *most* modes is the same as the block size. For AES this
   *             * is 128 bits */
  if(flag == 0) {
    if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_ecb(), NULL, key, iv))
      handleErrors();
  } 
  if(flag == 1) {
    if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_ctr(), NULL, key, iv))
      handleErrors();
  }
  /* Provide the message to be encrypted, and obtain the encrypted output.
   *    * EVP_EncryptUpdate can be called multiple times if necessary
   *       */
  if(1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len))
    handleErrors();
  ciphertext_len = len;

  /* Finalise the encryption. Further ciphertext bytes may be written at
   *    * this stage.
   *       */
  if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) handleErrors();
  ciphertext_len += len;

  /* Clean up */
  EVP_CIPHER_CTX_free(ctx);

  return ciphertext_len;
}







void main (int argc, char **argv) {

  FILE *kfd;
  unsigned char key[16];
  unsigned char material[1024];
  int len_material;
  kfd = fopen("/tmp/key_material", "r");
  len_material = fread(material, sizeof(char), 1024, kfd);
  fclose(kfd);


  // extract key

  memcpy(key, material, 16);


  int iv_len;
  unsigned char *iv = HexHandler(argv[1], &iv_len);

  unsigned char pad[1024];
  
  encrypt(iv, 16, key, NULL, pad, 0);
  printHex(pad, 16);


}
