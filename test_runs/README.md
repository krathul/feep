This directory contains script to automatically go through usage scenarios.

There is one example for okular which uses xdotool to generate mouse and keyboard actions. There is a python script `okular.py` which writes a shell script `okular.sh`. The shell script can then be executed to run okular through the usage scenario for pdf readers.

*Note: The script might be sensitive to the local environment in terms of local configuration or exact versions of the used software. Use it with care.*

Other ways to automate test runs are possible as well. See the [description of the measurement setup](../measurement-setup.md) for more details.
