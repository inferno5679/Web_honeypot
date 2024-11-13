
# Trap Door

Trap Door is a modular, graphical honeypot designed to capture IP addresses, usernames, passwords, and commands from various protocols, currently supporting SSH and HTTP. Written in Python, Trap Door provides a controlled environment for monitoring network intrusions, making it ideal for studying attacker behavior.

## Installation

### 1. Clone the Repository
Clone the repository using Git:

```bash
git clone https://github.com/inferno5679/Web_honeypot.git
```

### 2. Set Permissions
Navigate to the `Web_honeypot` directory and ensure that `main.py` has executable permissions:

```bash
cd Web_honeypot
chmod 755 honeypy.py
```

### 3. Generate SSH Key
Create a directory named `static` to store the SSH server key:

```bash
mkdir static
cd static
```

Generate an RSA key for the SSH server host, which will provide authentication for the SSH server. Name the key `server.key` and keep it in the `static` directory:

```bash
ssh-keygen -t rsa -b 2048 -f server.key
```

## Usage

To run Trap Door, use the `honeypy.py` file. You’ll need to specify a bind IP address (`-a`) and network port (`-p`). Define the protocol type (SSH or HTTP) as well.

```
-a / --address: Bind address.
-p / --port: Network port.
-s / --ssh OR -wh / --http: Protocol type (SSH or HTTP).
```

### Example
To set up an SSH honeypot on all network interfaces (0.0.0.0) and listen on port 22, run:

```bash
python3 honeypy.py -a 0.0.0.0 -p 22 --ssh
```

💡 **Note:** Running Trap Door on a privileged port (like 22) requires `sudo` or root privileges. Ensure no other service is using the selected port.

To change the default SSH port, refer to Hostinger’s [How to Change the SSH Port guide](https://www.hostinger.com/tutorials/how-to-change-ssh-port-vps).

❗ **If using `sudo`,** make sure the `root` account has access to all Python libraries listed in `requirements.txt`:

```bash
sudo pip install -r requirements.txt
```

**Note:** Installing dependencies globally may affect the overall environment; consider using virtual environments for better isolation.

## Optional Arguments

Trap Door provides additional options to configure the honeypot further:

- `-u` / `--username`: Specify an SSH username for authentication.
- `-w` / `--password`: Specify an SSH password for authentication.
- `-t` / `--tarpit`: Enable tarpit mode for SSH, trapping sessions by sending a continuous SSH banner.

### Example with Optional Arguments
To set up an SSH honeypot with a specific username and password and enable tarpit mode:

```bash
python3 honeypy.py -a 0.0.0.0 -p 22 --ssh -u admin -w admin --tarpit
```

