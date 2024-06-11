#!/bin/bash

docker build . -t threatfinderai-quant

docker run -it -p 9000:9000  \
           --user $UID:$GID  \
           -v $(pwd):/app    \
           threatfinderai-quant 

