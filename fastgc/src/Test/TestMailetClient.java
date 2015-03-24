// copyright by shuai@cs.umn.edu
//


package Test;

import java.util.*;
import java.math.*;
import java.security.SecureRandom;

import jargs.gnu.CmdLineParser;

import Utils.*;
import Program.*;


import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;



class TestMailetClient {
  static short[] msgIn;
//  static short[] msgIn = {0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x28};

  static short[] keyIn;
//  static short[] keyIn = {0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32,0x31,0x32};
  static short[] constIn;
  private static void printUsage() {
    System.out.println("Usage: java TestHammingClient [{-n, --bit-length} length] [{-s, --server} servername] [{-r, --iteration}     r]");
  }

  private static void process_cmdline_args(String[] args) {
    CmdLineParser parser = new CmdLineParser();
    CmdLineParser.Option optionServerIPname = parser.addStringOption('s', "server");
    try {
      parser.parse(args);
    }
  
  catch (CmdLineParser.OptionException e) {
    System.err.println(e.getMessage());
    printUsage();
    System.exit(2);
  }
  ProgClient.serverIPname = (String) parser.getOptionValue(optionServerIPname, new String("localhost"));
 
  Program.iterCount = 1;


  }
  

  private static short[] hexString2ShortArray(String s) {
    int i;
    int len = s.length();
    short[] data = new short[len/2];

    for(i = 0; i < len; i += 2) {
      int higher = Character.digit(s.charAt(i), 16);
      int lower = Character.digit(s.charAt(i+1), 16);
      data[i/2] = (short) ((higher << 4) + lower);
    }
    return data;
  }



  public static void main(String[] args) throws Exception {
    StopWatch.pointTimeStamp("Starting program");
    process_cmdline_args(args);

    System.out.format("Note starts here!\n");
    int msgInLength = 0;
    int constInLength = 0;

    // Read from stdin
    try {
      String str1, str2, str3;
      InputStreamReader in = new InputStreamReader(System.in);
      BufferedReader input = new BufferedReader(in);

      // first line: keyIn
      str1 = input.readLine();

      System.out.println("[Client] Key is:");
      keyIn = hexString2ShortArray(str1);
      System.out.println(str1);

      // second line: msgIn
      str2 = input.readLine();
      if(str2 != null) {
        msgIn = hexString2ShortArray(str2);

        System.out.println("[Client] Msg is:");
        System.out.println(str2);
        msgInLength = msgIn.length;
      }

      // third line: ConstIn
      str3 = input.readLine();
      if(str3 != null) {
        constIn = hexString2ShortArray(str3);
        System.out.println("[ConstIn] is:");
        System.out.println(str3);
        constInLength = constIn.length;
      }
      else {
        System.out.println("Client has no msg stream!");
        msgInLength = 0;
      }
    }

    catch(IOException io) {
      io.printStackTrace();
    }


    for (int j=0; j < msgInLength; j++) {
         System.out.format("%02X ", msgIn[j]);
    }
     System.out.println();


     System.out.format("Note ends here!");
     System.out.println("Client msgIn length is");
     System.out.println(msgInLength);


    MailetClient mclient = new MailetClient(msgIn, keyIn, 8*msgInLength, constIn);
    mclient.run();
  }

}
