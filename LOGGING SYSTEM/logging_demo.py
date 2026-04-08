import time
import threading
from core.log_level import LogLevel
from core.log_configuration import LogConfiguration
from appenders.file_appender import FileAppender
from appenders.console_appender import ConsoleAppender
from core.logger_implementation import LoggerImplementation
from filters.level_filter import LevelFilter
from formatters.simple_formatter import SimpleFormatter

def demo_basic_logging():
    print("1. Basic Logging Demo:")
    print("----------------------")
    logger = LoggerImplementation("BasicLogger")
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.fatal("This is a fatal message")
    print()

def demo_multiple_appenders():
    print("2. Multiple Appenders Demo:")
    print("---------------------------")
    logger = LoggerImplementation("MultiAppenderLogger")
    file_appender = FileAppender("demo.log")
    logger.add_appender(file_appender)
    logger.info("This message goes to both console and file")
    logger.error("This error also goes to both destinations")
    print("Check 'demo.log' file for the logged messages")
    print()

def demo_custom_formatters():
    print("3. Custom Formatters Demo:")
    print("--------------------------")
    logger = LoggerImplementation("FormatterLogger", config=LogConfiguration(LogLevel.INFO))
    custom_formatter = SimpleFormatter("[%LEVEL] %TIMESTAMP - %MESSAGE")
    console_appender = ConsoleAppender()
    console_appender.set_formatter(custom_formatter)
    logger.add_appender(console_appender)
    logger.info("This message uses custom formatting")
    logger.error("This error also uses custom formatting")
    print()

def demo_filters():
    print("4. Filters Demo:")
    print("----------------")
    logger = LoggerImplementation("FilterLogger")
    level_filter = LevelFilter(LogLevel.WARNING)
    logger.add_filter(level_filter)
    logger.debug("This debug message will be filtered out")
    logger.info("This info message will be filtered out")
    logger.warning("This warning message will be shown")
    logger.error("This error message will be shown")
    print()

def demo_thread_safety():
    print("5. Thread Safety Demo:")
    print("----------------------")
    logger = LoggerImplementation("ThreadSafeLogger")
    def log_messages(thread_id):
        for j in range(3):
            logger.info(f"Thread {thread_id} - Message {j}")
            time.sleep(0.01)
    threads = []
    for i in range(5):
        t = threading.Thread(target=log_messages, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print("All threads completed - check for any mixed-up messages above")
    print()

if __name__ == "__main__":
    print("=== LoggingFramework Python Demo ===\n")
    # demo_basic_logging()
    #demo_multiple_appenders()
    # demo_custom_formatters()
    # demo_filters()
    demo_thread_safety()
    # print("\n=== Demo Complete ===")
