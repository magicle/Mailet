// copyright by shuai@cs.umn.edu


package Program;

import java.math.*;

import java.io.OutputStream;
import java.io.FileOutputStream;


import java.security.SecureRandom;
import YaoGC.*;
import Utils.*;


public class MailetServer extends ProgServer {
  private short[] msg;       // or msg1
  private BigInteger m;      // BigInteger version of msg1
  private int bitLengthS;   
  private int bitLengthC;
  private State outputState;


  private BigInteger Http;
  private int httpLength;

  private BigInteger[][] msg1Labpair, msg2Labpair, keyLabpair;


  private static final SecureRandom rnd = new SecureRandom();

  public MailetServer(short[] msgIn, int length) {
    msg = msgIn;
    bitLengthS = length;
    m = MailetCommon.array2Biginteger(msg, bitLengthS);
  }


  protected void init() throws Exception {

    // pass length info to client
    MailetCommon.oos.writeInt(bitLengthS);
    MailetCommon.oos.flush();
 
    // read length info from client
    bitLengthC = MailetCommon.ois.readInt();


    // read Http and its length
//    Http = Utils.readBigInteger(MailetCommon.ois);
    httpLength = MailetCommon.ois.readInt();
    Http = Utils.readBigInteger(httpLength/8, MailetCommon.ois);

    System.out.println("httpLength is: ");
    System.out.println(httpLength);


    // init MailetCommon.
    MailetCommon.bitLengthS = bitLengthS;
    MailetCommon.bitLengthC = bitLengthC;

    Circuit.isForGarbling = true;     // setup isForGarbling flag BEFORE create instance!!

    MailetCommon.initCircuits();
    generateLabelPairs();
    super.init();
  }

  private void generateLabelPairs() {
    msg1Labpair = new BigInteger[bitLengthS][2];
    msg2Labpair = new BigInteger[bitLengthC][2];
    keyLabpair = new BigInteger[MailetCommon.keyLength][2];

    for(int i = 0; i < bitLengthS; i++) {
      BigInteger glb0 = new BigInteger(Wire.labelBitLength, rnd);
      BigInteger glb1 = glb0.xor(Wire.R.shiftLeft(1).setBit(0));
      msg1Labpair[i][0] = glb0;
      msg1Labpair[i][1] = glb1;
    }


    for(int i = 0; i < bitLengthC; i++) {
      BigInteger glb0 = new BigInteger(Wire.labelBitLength, rnd);
      BigInteger glb1 = glb0.xor(Wire.R.shiftLeft(1).setBit(0));
      msg2Labpair[i][0] = glb0;
      msg2Labpair[i][1] = glb1;
    }
                                      

    for(int i = 0; i < MailetCommon.keyLength; i++) {
      BigInteger glb0 = new BigInteger(Wire.labelBitLength, rnd);
      BigInteger glb1 = glb0.xor(Wire.R.shiftLeft(1).setBit(0));
      keyLabpair[i][0] = glb0;
      keyLabpair[i][1] = glb1;
    }
  }

  protected void execTransfer() throws Exception {

    StopWatch.taskTimeStamp("enter execTransfer...");

    int bytelength = (Wire.labelBitLength-1)/8 + 1;

    for(int i = 0; i < bitLengthS; i++) {

      int idx = m.testBit(i) == true? 1 : 0;


      Utils.writeBigInteger(msg1Labpair[i][idx], bytelength, MailetCommon.oos);
    }
    MailetCommon.oos.flush();

    StopWatch.taskTimeStamp("sending labels for selfs inputs");


    // combine msg2 and key
    BigInteger[][] keyPlusMsg2;

    keyPlusMsg2 = new BigInteger[bitLengthC + MailetCommon.keyLength][2];
    
    // key first
    for(int i = 0; i < MailetCommon.keyLength; i++) {
      keyPlusMsg2[i][0] = keyLabpair[i][0];
      keyPlusMsg2[i][1] = keyLabpair[i][1];
    }
    for(int i = 0; i < bitLengthC; i++) {
      keyPlusMsg2[i + MailetCommon.keyLength][0] = msg2Labpair[i][0];
      keyPlusMsg2[i + MailetCommon.keyLength][1] =                 msg2Labpair[i][1];
    }


    snder.execProtocol(keyPlusMsg2);

    StopWatch.taskTimeStamp("sending labels for peers inputs");


//  // Test by Shuai 
//  OutputStream testoutstream = new FileOutputStream("/home/shuai/workspace/output/server.txt");
//  for (int i = 0; i<keyLabpair.length; i++) {
////    testoutstream.write((byte[])Character.toChars(i));
//    testoutstream.write((byte)'\n');
//    Utils.writeBigInteger(keyLabpair[i][0], bytelength, testoutstream);
//    testoutstream.write((byte)'\n');
//    Utils.writeBigInteger(keyLabpair[i][1], bytelength, testoutstream);
//    testoutstream.write((byte)'\n');
//  }
//
//
//
//
//  // Test End
//
//




  }

  protected void execCircuit() throws Exception {

    BigInteger[] zero1Lab = new BigInteger[bitLengthS];
    BigInteger[] zero2Lab = new BigInteger[bitLengthC];
    BigInteger[] zero3Lab = new BigInteger[MailetCommon.keyLength];

    for(int i = 0; i < msg1Labpair.length; i++){
      zero1Lab[i] = msg1Labpair[i][0];
    }

    for(int i = 0; i < msg2Labpair.length; i++) {
      zero2Lab[i] = msg2Labpair[i][0];
    }

    for(int i = 0; i < keyLabpair.length; i++) {
      zero3Lab[i] = keyLabpair[i][0];
    }

    outputState = MailetCommon.execCircuit(zero1Lab, zero2Lab, zero3Lab, Http, httpLength);
  }








  protected void interpretResult() throws Exception {
    BigInteger[] outLabels = (BigInteger[]) MailetCommon.ois.readObject();
    BigInteger output = BigInteger.ZERO;
    for (int i = 0; i < outLabels.length; i++) {
        if (outputState.wires[i].value != Wire.UNKNOWN_SIG) {
          if (outputState.wires[i].value == 1)
            output = output.setBit(i);
            continue;
        }
        else if (outLabels[i].equals(outputState.wires[i].invd ?
           outputState.wires[i].lbl :
           outputState.wires[i].lbl.xor(Wire.R.shiftLeft(1).setBit(0)))) {
          output = output.setBit(i);
        }
        else if (!outLabels[i].equals(outputState.wires[i].invd ?
            outputState.wires[i].lbl.xor(Wire.R.shiftLeft(1).setBit(0)) :
            outputState.wires[i].lbl))
    throw new Exception("Bad label encountered: i = " + i + "\t" +
            outLabels[i] + " != (" +
            outputState.wires[i].lbl + ", " +
            outputState.wires[i].lbl.xor(Wire.R.shiftLeft(1).setBit(0)) + ")");
    }

//    System.out.println("output (pp): " + output);
    StopWatch.taskTimeStamp("output labels received and interpreted");
    System.out.print("Circuit.counter_XOR = ");
    System.out.println(Circuit.counter_XOR);

    System.out.print("Circuit.counter_OR = ");
    System.out.println(Circuit.counter_OR);

    System.out.print("Circuit.counter_AND = ");
    System.out.println(Circuit.counter_AND);

    System.out.print("Circuit.counter_NOT = ");
    System.out.println(Circuit.counter_NOT);

    System.out.print("Circuit.counter_SHIFT = ");
    System.out.println(Circuit.counter_shift);
    // Test By Shuai
    //
    System.out.print("[Final Output]: ");
    for(int i = 0; i < outLabels.length; i++)  {
      int idx = output.testBit(i)? 1 : 0 ;
      if(idx == 1) {System.out.print("1");}
      if(idx == 0) {System.out.print("0");}
      if(i%8 == 7) {System.out.print(" ");}
    }
    System.out.println("");
  
  
  
  
  }

  protected void verify_result() throws Exception {
  
  }

} 
