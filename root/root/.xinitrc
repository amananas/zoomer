while ! [ -e /tmp/grayscale ]; do
    sleep 1
done
if [ `cat /tmp/grayscale` == "False" ]; then
    exec mpv --force-seekable --geometry 100%x100% --video-rotate 180 /dev/video0
else
    exec mpv --force-seekable --geometry 100%x100% --vf format=gray --video-rotate 180 /dev/video0
fi
