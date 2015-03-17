#include<stdio.h>
#include<openssl/rc4.h>


void main(int argc, char **argv) {

  int i;
  unsigned char key[1024];
  unsigned char pad[1024];
  unsigned char msgin[1024] = {0};
  
  size_t len_key;
  FILE *kfd;
  kfd = fopen("key_material", "r");
  len_key = fread(key, sizeof(char), 1024, kfd);
  fclose(kfd);




  // RC4 
  RC4_KEY rckey;
  RC4_set_key(&rckey, 16, &key[40]);
  RC4(&rckey, 1024, msgin, pad);

  // print pad for hmac key
  printf("EncryptPad:"); 
  for(i = 36; i < 1024; i++) {
    printf("%02x", pad[i]);
  }



  printf("\nMacKey:");
  
  for(i = 0; i < 20; i++) {
    printf("%02x", key[i]);
  }

  printf("\n");






//
//  printf("\n..............TEST................\n");
//  printf("key masterial is: \n");
//  for(i = 0; i < len_key; i++) {
//    printf("%02x ", key[i]);
//  }
//  printf("\nlength is: %zu\n", len_key);
}
