while true;do
  echo "listening!"
  txt="$(echo "nc" | nc -l 8080)"
  echo "$txt" | base64 -D > processes.txt
  echo "$txt" | base64 -D > screenshot.png
  echo "saved!"
  exit
done
