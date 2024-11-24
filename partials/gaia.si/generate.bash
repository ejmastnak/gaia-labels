#!/usr/bin/env bash

red50="#fef2f2"
red950="#450a0a"
amber50="#fffbeb"
orange950="#431407"
yellow50="#fefce8"
yellow950="#422006"

URL="https://gaia.si"

segno "${URL}" --light ${red50} --dark ${red950} --scale 10 --border 2 --output "gaia-si-red.svg"
segno "${URL}" --light ${amber50} --dark ${orange950} --scale 10 --border 2 --output "gaia-si-orange.svg"
segno "${URL}" --light ${yellow50} --dark ${yellow950} --scale 10 --border 2 --output "gaia-si-yellow.svg"
