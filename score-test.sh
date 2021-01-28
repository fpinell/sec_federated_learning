#!/bin/bash

for i in `seq 1 10`; do
  echo Launching container N. $i
  docker run -v $(pwd):/home/fedexp/src/tests gabrielec/fedexp-test-score > "score-${i}.out" &
done

wait
echo Completed