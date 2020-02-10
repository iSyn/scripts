
# SSHTO

This is a simple script that allows you to easily SSH into pre-specified instances.

Example: `sshto -c www` will connect you to www.medly.link

## How to use
1. Download or copy/paste the `sshto` file and add into one of your $PATH locations.
	
    a) I personally put my scripts within a folder I made at `~/bin`. Then add the new path to /etc/paths [guide](https://stackoverflow.com/questions/7703041/editing-path-variable-on-mac)
    
    b) You might need to run the command `chmod +x sshto` to give it executable permissions.

2. `vi sshto` and edit the `PATH_TO_PEM_KEYS` with your personal location.

3. Run script by typing `sshto <command>`

