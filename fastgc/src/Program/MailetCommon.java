// copyright by shuai@cs.umn.edu



package Program;

import java.math.*;

import Utils.*;

import YaoGC.*;
import YaoGC.Mailet.*;

import java.util.Arrays;

class MailetCommon extends ProgCommon {

  public static int keyLength = 64*8;
  public static int bitLengthS;
  public static int bitLengthC;




  protected static void initCircuits() {
    ccs = new Circuit[11];
    ccs[0] = new TEMP();
    ccs[1] = new FT1();
    ccs[2] = new FT2();
    ccs[3] = new FT3();
    ccs[4] = new FT4();
    ccs[5] = new WT();
    ccs[6] = new SHIFT_L(32, 30);
    ccs[7] = new ADD_MOD_2L_L(32);

      ccs[8] = new XOR_2L_L(512);
    if(bitLengthS == bitLengthC - 20*8) {
      ccs[9] = new XOR_2L_L(bitLengthS);
    }
    else {
      System.out.println("bitLengthS:" + bitLengthS + "bitLengthC" + bitLengthC);
      System.out.println("ERROR: bitLengthS != bitLengthC");
    }
    ccs[10] = new XOR_2L_L(20*8);



//    ccs[0] = new ADD_MOD_2L_L(8);
//    ccs[0] = new FT3();

//    ccs[0] = new FT2();
//    ccs[0] = new FT1();
//    ccs[0] = new WT();

//    ccs[0] = new SHIFT_L(2*bitLength, 5);
    
    
//    ccs[0] = new XOR_2_1();           // XOR Gate
//    ccs[0] = AND_2_1.newInstance();   // AND Gate
//    ccs[0] = OR_2_1.newInstance();    // OR Gate
//    ccs[0] = new XOR_2L_L(bitLength); // bitwise XOR
//    ccs[0] = new AND_2L_L(bitLength);   // bitwire AND
//    ccs[0] = new OR_2L_L(bitLength);      // bitwire OR

  }

  public static State execCircuit(BigInteger[] msg1Lab, BigInteger[] msg2Lab, BigInteger[] keyLab, BigInteger Http, int bitlen) throws Exception {

    // create http state object
    State HTTP = new State(Http, bitlen);

    // end


    int msg1Length = msg1Lab.length;
    int msg2Length = msg2Lab.length;


    BigInteger[] inLab = new BigInteger[msg1Length + msg2Length];
    System.arraycopy(msg1Lab, 0, inLab, 0, msg1Lab.length);
    System.arraycopy(msg2Lab, 0, inLab, msg1Lab.length, msg2Lab.length);

    State key = State.fromLabels(keyLab);

    // split msg into password and pad
    State in = State.fromLabels(Arrays.copyOfRange(inLab, 0, inLab.length - 20*8));
    State pad = State.fromLabels(Arrays.copyOfRange(inLab, inLab.length - 20*8, inLab.length));
    //    State in = State.fromLabels(inLab);
    State password = msgXor(in);
    in = State.concatenate(password, HTTP);
    State digest = HMACMsgDigest(in, key);
    
    State DigestPad = State.concatenate(digest, pad);
    
    StopWatch.taskTimeStamp("circuit garbling");
    return ccs[10].startExecuting(DigestPad);
  }


  private static State HMACMsgDigest(State in, State key) {
    short[] iiipad = {0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36,0x36};

    short[] ooopad = {0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C,0x5C};

    BigInteger iipad = array2Biginteger(iiipad, 512);
    BigInteger oopad = array2Biginteger(ooopad, 512);

    // create State object
    State ipad = new State(iipad, 512);
    State opad = new State(oopad, 512);

    
    State ikeypad = ccs[8].startExecuting(State.concatenate(ipad, key));
    State okeypad = ccs[8].startExecuting(State.concatenate(opad, key));

    State tog = State.concatenate(in, ikeypad);
    State hashSum1 = SHA1MsgDigest(tog);

    tog = State.concatenate(hashSum1, okeypad);
    State hashSum2 = SHA1MsgDigest(tog);

    return hashSum2;
  }


  private static State msgXor(State in) {
    return ccs[9].startExecuting(in);
  }

  // message padding
  private static State SHA1MsgDigest(State in) {
    
    // pading 1000 0000
    BigInteger Num01 = BigInteger.valueOf(1);
    State paddingOne = new State(Num01, 8);

    // length pading
    BigInteger bigLength = BigInteger.valueOf(in.wires.length);
    
    System.out.println("in.wires.length = " + in.wires.length);
    
    BigInteger bigLengthReverse = BigInteger.ZERO;

    for(int i = 0; i < 64; i++) {
      if(bigLength.testBit(i)) {
        bigLengthReverse = bigLengthReverse.setBit(63-i);
      }
    }

    System.out.println(new String(bigLength.toByteArray()));


    State paddingLength = new State(bigLengthReverse, 64);

    // length 0s
    State paddingZero = null;
    int numZero = 512 - ( (in.wires.length + 8 + 64) % 512 );
    

    if(numZero != 0) {
      paddingZero = new State(BigInteger.ZERO, numZero);
    }

    // get them together
    State msgFinal;
    if(numZero != 0) {
      msgFinal = State.concatenate(paddingLength, paddingZero);
      msgFinal = State.concatenate(msgFinal, paddingOne);
      msgFinal = State.concatenate(msgFinal, in);
    }
    else {
      msgFinal = State.concatenate(paddingLength, paddingOne);
      msgFinal = State.concatenate(msgFinal, in);
    }

    if(msgFinal.wires.length % 512 != 0) {
      System.out.println("[Error] padding fails!");
    }
    State out = SHA1Blk(msgFinal);
    return out;
  }




  // implement the SHA1 function
  // suppose the in is 16 words
  private static State SHA1Blk(State in) {


    State[] W80 = new State[80];
    State[] K80 = new State[80];
    
    State Words = in; 
    int round = Words.wires.length / 512;

    // [H Generation]: initialize H0~H4
    short[] hh0 = {0x67,0x45,0x23,0x01};
    short[] hh1 = {0xEF,0xCD,0xAB,0x89};
    short[] hh2 = {0x98,0xBA,0xDC,0xFE};
    short[] hh3 = {0x10,0x32,0x54,0x76};
    short[] hh4 = {0xC3,0xD2,0xE1,0xF0};

    // [H Generation]: convert to BigInteger
    BigInteger h0 = array2Biginteger(hh0, 32);
    BigInteger h1 = array2Biginteger(hh1, 32);
    BigInteger h2 = array2Biginteger(hh2, 32);
    BigInteger h3 = array2Biginteger(hh3, 32);
    BigInteger h4 = array2Biginteger(hh4, 32);

    // [H Generation]: create State object
    State H0 = new State(h0, 32);
    State H1 = new State(h1, 32);
    State H2 = new State(h2, 32);
    State H3 = new State(h3, 32);
    State H4 = new State(h4, 32);
    

    // [K(t) generation]
    short[] kk0 = {0x5A,0x82,0x79,0x99};
    short[] kk1 = {0x6E,0xD9,0xEB,0xA1};
    short[] kk2= {0x8F,0x1B,0xBC,0xDC};
    short[] kk3 = {0xCA,0x62,0xC1,0xD6};

    // [K(t) generation]: to BigInteger
    BigInteger k0 = array2Biginteger(kk0, 32);
    BigInteger k1 = array2Biginteger(kk1, 32);
    BigInteger k2 = array2Biginteger(kk2, 32);
    BigInteger k3 = array2Biginteger(kk3, 32);

    // [K(t) generation]: create State object
    State K0 = new State(k0, 32);
    State K1 = new State(k1, 32);
    State K2 = new State(k2, 32);
    State K3 = new State(k3, 32);
    
    for(int i = 0; i < 80; i++) {
      if(i>=0 && i<= 19) {
        K80[i] = K0;
      }
      else if(i>=20 && i<= 39) {
        K80[i] = K1;
      }
      else if(i>=40 && i<= 59) {
        K80[i] = K2;
      }
      else if(i>=60 && i<= 79) {
        K80[i] = K3;
      }
      else {
        System.out.println("Error: index of K80 is out of range!");
      }
    }

    for(int r = 0; r < round; r++) {
      State Msg = State.extractState(Words, 512*r, 512*r + 512);
      // expand message
      for(int i = 0; i < 16; i++) {
        W80[i] = State.extractState(Msg, 32*i, 32*i + 32);
      } 
    
      for(int i = 16; i < 80; i++) {
  //      System.out.println("Shuai Test: i=" + i);
        W80[i] = expandMessage(W80[i-3], W80[i-8], W80[i-14], W80[i-16]); 
      }


      State A = H0;
      State B = H1;
      State C = H2;
      State D = H3;
      State E = H4;

      State ftemp = null;
      State temp = null;
      for(int t = 0; t < 80; t++) {
         ftemp = fFunction(t, B, C, D);
         temp = tempFunction(A, ftemp, E, W80[t], K80[t]);
        
         E = D;
         D = C;
         C = ccs[6].startExecuting(B);
         B = A;
         A = temp;
      }


      H0 = addFunction(H0, A);
      H1 = addFunction(H1, B);
      H2 = addFunction(H2, C);
      H3 = addFunction(H3, D);
      H4 = addFunction(H4, E);

    }
    State Tog;
    Tog = State.concatenate(H4, H3);
    Tog = State.concatenate(Tog, H2);
    Tog = State.concatenate(Tog, H1);
    Tog = State.concatenate(Tog, H0);
  
//    return W80[15];  
        return Tog;

  }


  public static State addFunction(State N1, State N2) {
    State Tog;
    Tog = State.concatenate(N2, N1);
    return ccs[7].startExecuting(Tog);
  }

  public static State tempFunction(State N1, State N2, State N3, State N4, State N5) { 
    State Tog;
    Tog = State.concatenate(N5, N4);
    Tog = State.concatenate(Tog, N3);
    Tog = State.concatenate(Tog, N2);
    Tog = State.concatenate(Tog, N1);
    return ccs[0].startExecuting(Tog);
  }

  public static State fFunction(int t, State B, State C, State D) {
    State Tog;
    Tog = State.concatenate(D, C);
    Tog = State.concatenate(Tog, B);
    if( t>=0 && t<= 19) {
      return ccs[1].startExecuting(Tog);
    }
    else if(t>=20 && t<=39) {
      return ccs[2].startExecuting(Tog);
    }
    else if(t>=40 && t<= 59) {
      return ccs[3].startExecuting(Tog);
    }
    else if(t>=60 && t<= 79) {
      return ccs[4].startExecuting(Tog);
    }
    else {
      System.out.println("Error: the index t is out of range!");
      return null;
    }
  }

  public static State expandMessage(State N1, State N2, State N3, State N4) {
    State Tog;
    Tog = State.concatenate(N4, N3);
    Tog = State.concatenate(Tog, N2);
    Tog = State.concatenate(Tog, N1);
    return ccs[5].startExecuting(Tog);
  }


  // convert msg into a bigInteger
  //
  // bits of msg: left -> right 
  // bits of bigInteger: right -> left
  // equal
  //
  // this results in
  // order of input = order of inputWires
  //
  static BigInteger array2Biginteger(short[] msg, int length) {
    reFormat(msg);
    BigInteger m = BigInteger.ZERO;
    int i = length / 8;
    int j = length % 8;

//    System.out.println("i = " + i + ", j = " + j);
    if(j != 0) {    // have a incomplete block
      
      for (int k = 0; k < j; k++) {
        int idx = byteTestBit(msg[i], k);
        if(idx != 0) { 
          m = m.setBit(k);
        }
      }
    } 
    // deal with the rest
    for(int k = 0; k < i; k++) {
      m = m.shiftLeft(8).xor(BigInteger.valueOf(msg[i-k-1]));
    }
    return m;

  }


  // this method reformats input parameters for easy recognition.
  // Original: input block order = circuit block order, but the    order in block is reversed
  // Let's fix it

  public static int byteTestBit(short a, int pos) {
    return a & (1<<pos);
  }

  public static short byteSetBit(short a, int pos) {
    return (short) (a | (1<<pos));
  }

  public static short byteResetBit(short a, int pos) {
    return (short)(a & ~(1<<pos));
  }



  public static void reFormat(short[] original) {
    short temp;
    short result;
    
    if(original != null) {
      for(int i = 0; i < original.length; i++) {
        temp = original[i];
        result = 0;
        for(int j = 0; j < 8; j++) {
          if( byteTestBit(temp, j) != 0) {
            result = byteSetBit(result, 7-j);
          }
          else {
            result = byteResetBit(result, 7-j);
          }
        }
        original[i] = result;
      }
    }
  }
}





