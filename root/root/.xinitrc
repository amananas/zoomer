while ! [ -e /tmp/grayscale ]; do
    sleep 1
done
if [ `cat /tmp/grayscale` == "False" ]; then
    exec mpv --force-seekable /dev/video0
else
    exec mpv --force-seekable --vf format=gray /dev/video0
fi