MROOT=$HOME/sdk/openstf/minicap
adb start-server
ABI=$(adb shell getprop ro.product.cpu.abi | tr -d '\r')
SDK=$(adb shell getprop ro.build.version.sdk | tr -d '\r')
DIR=/data/local/tmp/minicap-devel
adb shell mkdir $DIR
adb push $MROOT/libs/$ABI/minicap $DIR
adb push $MROOT/jni/minicap-shared/aosp/libs/android-$SDK/$ABI/minicap.so $DIR
adb shell LD_LIBRARY_PATH=$DIR $DIR/minicap -P 480x854@480x854/0
