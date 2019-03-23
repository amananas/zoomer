while ! [ -e /tmp/grayscale ]; do
    sleep 1
done
if [ `cat /tmp/grayscale` == "False" ]; then
    exec mpv --force-seekable --geometry 100%x100% /dev/video0
else
    exec mpv --force-seekable --geometry 100%x100% --vf format=gray /dev/video0
fi