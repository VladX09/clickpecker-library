MROOT=$HOME/sdk/openstf/minitouch
adb start-server
ABI=$(adb shell getprop ro.product.cpu.abi | tr -d '\r')
adb push $MROOT/libs/$ABI/minitouch /data/local/tmp/
adb shell /data/local/tmp/minitouch
