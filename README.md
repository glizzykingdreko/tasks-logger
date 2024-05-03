# Tasks Logger
![Logo](https://i.imgur.com/sI4C8kC.jpeg)

## Overview
`tasks-logger` is a versatile Python logging library designed to facilitate detailed and color-coded logging for applications that manage multiple tasks, such as those operating across various threads or processes. It extends the basic functionality of Python’s built-in logging module to include dynamic log levels, thread-safe output, conditional file logging, and vivid color outputs for better clarity and monitoring.

Check also [tasks-loader](https://github.com/glizzykingdreko/tasks-loader/)

## Table Of Contents
- [Tasks Logger](#tasks-logger)
  - [Overview](#overview)
  - [Table Of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [How It Works](#how-it-works)
  - [Usage](#usage)
    - [Basic Setup](#basic-setup)
    - [Adding New Log Levels](#adding-new-log-levels)
    - [Thread-Safe Logging](#thread-safe-logging)
    - [Conditional File Logging](#conditional-file-logging)
  - [Example Application: Sneakers/Tickets Bot](#example-application-sneakerstickets-bot)
  - [Stay in touch with me](#stay-in-touch-with-me)


## Features
- **Dynamic Log Levels**: Easily define new log levels on the fly.
- **Color-coded Output**: Enhance log visibility with configurable color outputs for each log level.
- **Conditional File Logging**: Decide which log level messages are important enough to save to files.
- **Thread Safety**: Ensure logs are thread-safe using locks to prevent text scrambling when used in multi-threaded applications.

## Installation
Install `tasks-logger` via pip:

```bash
pip install tasks-logger
```

## How It Works
`tasks-logger` utilizes the Colorama library to add color to log messages depending on their severity. You can set up different log levels and specify whether these should be output to the console, saved to a file, or both. The logger also supports dynamic addition of new log levels with specific properties.

## Usage

### Basic Setup
Here's how to set up and use the `tasks-logger`:

```python
from tasks_logger import Logger

logger = Logger(level='INFO', file_level='ERROR', filename='app.log')
logger.info("This is an informational message.")
logger.error("This error message will also be saved to a file.")
```

### Adding New Log Levels
You can add new log levels dynamically:

```python
logger.add_level('VERBOSE', 15, Fore.LIGHTBLUE_EX)
logger.verbose("This is a verbose message with custom log level.")
```

### Thread-Safe Logging
`tasks-logger` is designed to be safe for use in multi-threaded environments:

```python
import threading

def task():
    logger.info("Log from a thread.")

thread = threading.Thread(target=task)
thread.start()
thread.join()
```

### Conditional File Logging
Control which log levels are logged to files:

```python
# Only ERROR and above levels will be saved to the file.
logger = Logger(level='DEBUG', file_level='ERROR', filename='important.log')
logger.debug("This message will not be logged in the file.")
logger.error("This error will be logged in the file.")
```

## Example Application: Sneakers/Tickets Bot

Here is an example showing how `tasks-logger` might be used in a sneakers/tickets purchasing bot, which operates with multiple tasks:

```python
class MyTask:
    def __init__(self, task_id: str, mail: str, ...):
        self.logger = Logger(
            level='INFO', 
            task_id=task_id,
            mail=mail,
            formatting="[{timestamp}] [{level}] ({task_id}) {mail} - {message}"
        )

```


## Stay in touch with me

For any inquiries or further information, please reach out:

- [GitHub](https://github.com/glizzykingdreko)
- [Twitter](https://mobile.twitter.com/glizzykingdreko)
- [Medium](https://medium.com/@glizzykingdreko)
- [Email](mailto:glizzykingdreko@protonmail.com) 
- [Website](https://glizzykingdreko.github.io)
- [Buy me a coffee ❤️](https://www.buymeacoffee.com/glizzykingdreko)
- Antibot bypass solutions needed? [TakionAPI](https://takionapi.tech/discord)

Feel free to contact for collaborations, questions, or feedback any of my projects.