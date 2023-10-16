#! /bin/bash
EYE="$1 /mnt/e/dev/timeloop-accelergy-exercises/workspace/exercises/2020.ispass/timeloop+accelergy/arch/components/*.yaml /home/mplagge/ath_copy/athena_tool/athena_tool/accelergy_architectures/sonos_pim/mapper/mapper.yaml /mnt/e/dev/timeloop-accelergy-exercises/workspace/exercises/2020.ispass/timeloop+accelergy/constraints/*.yaml"
timeloop-mapper $EYE $2
