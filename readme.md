# CyberCobra

## Credits

Created by Milan

## Description

CyberCobra is a tool made to exploit the ticket controller vulnerability in mezzcms 2.5+

## Requirements

- Python 3.9 or above
- `requests` library
- `argparse` library
- `logging` library

## Installation

1. Clone the repository:

    git clone https://github.com/WinQz/CyberCobra-MezzVuln/CyberCobra.git
    cd CyberCobra

## Configuration

Create a `config_bot.json` file with the following structure:

    {
      "num_bots": 10,
      "rate_per_minute": 60,
      "use_proxy": false,
      "retry_attempts": 3,
      "retry_delay": 5
    }

## Usage

### Start the bot system

To start the bot system, use the following command:

    python script.py --config config_bot.json --start

### Stop the bot system

To stop the bot system, use the following command:

    python script.py --config config_bot.json --stop
    

### Check the status of the bot system

To check the status of the bot system, use the following command:

    python script.py --config config_bot.json --status

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
