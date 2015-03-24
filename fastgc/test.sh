#!/bin/bash


java -cp /home/shuai/Desktop/fastgc/dist/FasterGC.jar:/home/shuai/Desktop/fastgc/extlibs/jargs.jar:/home/shuai/Desktop/fastgc/extlibs/commons-io-1.4.jar Test.TestMailetServer &

sleep 0.8

java -cp /home/shuai/Desktop/fastgc/dist/FasterGC.jar:/home/shuai/Desktop/fastgc/extlibs/jargs.jar:/home/shuai/Desktop/fastgc/extlibs/commons-io-1.4.jar Test.TestMailetClient --server localhost & 
