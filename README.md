# Python Logging & Dependency Injection Example

![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![mypy](https://img.shields.io/badge/mypy-type_checked-blueviolet)
![pytest](https://img.shields.io/badge/pytest-tested-green)

This project demonstrates a clean, type-safe architecture for building Python applications using:

- **Structured logging** via interchangeable backends (Structlog, Seq, Mock)
- **Dependency injection (IoC)** with `dependency_injector`
- **Service abstraction** with protocol-based interfaces (`ILogger`, `IService`)
- **Runtime configurability** via `config.json`
- **Static type checking** with `mypy`
- **Unit testing** with `pytest` and mock loggers

## 🤔 What is Dependency Injection and Why Is It Important?

Dependency Injection (DI) is a design pattern that promotes **loose coupling** by supplying a class’s dependencies — like loggers, services, or database clients — from the outside, rather than constructing them internally.

One common problem in Python codebases is the need to **manually pass shared resources**, like a logger, to dozens or even hundreds of classes. This quickly becomes unwieldy as more shared dependencies are added, leading to tangled constructors and brittle code.

DI helps solve this by letting you:

- **Centralize configuration** of shared services (like logging)
- **Swap implementations** at runtime or for testing
- **Simplify class construction**, even when many dependencies are involved
- **Avoid global state** without the overhead of passing objects everywhere

Instead of this:

```python
class MyClass:
    def __init__(self):
        self.logger = Logger()
```

You do this:

```python
class MyClass:
    def __init__(self, logger: ILogger):
        self.logger = logger
```

And let the IoC container handle the wiring:

```python
my_class = container.my_class()  # logger is injected automatically
```

This makes it easier to test, extend, and reason about your code — and keeps your constructors clean and focused.


## Project Overview

```text
app/
├── container.py                  # Dependency injection container
├── container_registries.py       # Registry of logger factories
├── logging/
│   ├── ilogger.py                # ILogger interface
│   ├── ilogger_factory.py        # ILoggerFactory interface
│   ├── struct_logger/            # Structlog-based logger impl
│   ├── seqlogger/                # Seqlog-based logger impl
│   └── mock_logger/              # Mock logger for testing
├── service/
│   ├── iservice.py               # IService protocol
│   ├── hello_console_service.py  # console application 
│   ├── hello_web_service.py      # web service application
│   └── hello_windows_service.py  # windows service application
├── tests/
│   ├── test_hello_service.py     # hello service tests, run with pytest
config.json                       # Runtime configuration
config.py                         # Implementation of AppConfig (a TypedDict)
main.py                           # Entry point
mypy.ini                          # Configuration for mypy
pytest.ini                        # Configuration for pytest
```

## Configuration

The `config.json` file drives the application wiring and behavior:

```json
{
  "available_loggers": [
    "structlog",
    "seqlog",
    "mocklog"
  ],
  "logger_factory": "seqlog",
  "available_services": [
    "console",
    "windows",
    "web"
  ],
  "service_type": "web" 
}
```

You can change `service_type` and `logger_factory` to switch between implementations without modifying any code.

## Why Use a Registry for Logger Factories?

Instead of using a `providers.Selector()` inside the container, we use a separate `LOGGER_REGISTRY`:

```python
LOGGER_REGISTRY = {
  "structlog": lambda: StructLoggerFactory(),
  "mocklog": lambda: MockLoggerFactory(),
  "seqlog": lambda: SeqLoggerFactory()
}
```

This allows us to:

- **Configure logging early**, before the container exists
- Log immediately during startup
- Keep the container focused on *wiring*, not *logic or policy*

```python
logger_factory = configure_logging(config)
container.logger_factory.override(logger_factory)
```

## Type Safety

### `TypedDict` for Configuration

We use a strongly-typed config definition for safety and autocomplete:

```python
class AppConfig(TypedDict):
    service_type: str
    available_services: list[str]
    logger_factory: str
    available_loggers: list[str]
```

Because `providers.Configuration().from_dict()` expects a `dict[str, Any]`, we use a type cast:

```python
container.config.from_dict(cast(dict[str, Any], config))
```

This is safe and typical when using `TypedDict` + IoC.

## Testing

Tests use a `MockLogger` to validate behavior without requiring a real logger backend.

```bash
pytest
```

```python
@pytest.mark.parametrize("service_class, expected_log", [...])
def test_services_log_expected_messages(...):
    mock_logger = MockLogger()
    service = service_class(logger=mock_logger)
    ...
    assert any(expected_log in msg for msg in mock_logger.logs)
```

## Summary

This project demonstrates:

- Decoupled, testable design via dependency injection
- Structured logging with pluggable backends
- Runtime configuration using JSON
- Full type safety with `mypy`
- Fast, isolated unit testing

If you're building maintainable Python applications that may grow in complexity, this structure offers a solid foundation.

## Walkthrough

`main()` first processes the configuration file, through `config = load_config()`. Because this application is configuration-driven, it's important to process the configuration first. The configuration is also needed before logging can be initialized. Otherwise, we would simply use the IoC container to provide configuration as well.

Then `main()` configures the `logger_factory` to establish which sort of logger to create, and creates a `bootstrap_logger` for immediate use:

```python
logger_factory = configure_logging(config)
bootstrap_logger = logger_factory.create_logger("bootstrap")
bootstrap_logger.info("Logger factory configured successfully.")
```

This creates two instances of `ILogger`: one named `"bootstrap"` and one for `"main". Both use the same logging backend and configuration. 

Finally, `main()` creates and configures the IoC container:

```python
container = AppContainer()
container.config.from_dict(cast(dict[str, Any], config))
container.logger_factory.override(logger_factory)
```

Once created, the container can be used to resolve providers it knows about, such as `IService`:

```python
service = container.hello_service()
service.run()
```

It is worth calling out that at this point, now that the IoC is created, we can — and likely should — rely on it for all providers it manages, such as `IService` and `ILogger`.

This startup sequence ensures that configuration and logging are available from the beginning, services are selected dynamically at runtime, and all dependencies are cleanly injected — without hardcoding implementation details.

> ⚠️ You could design the container to load configuration and create the logger internally, but this introduces uncertainty around when the logger becomes usable. It's often better to handle configuration and bootstrap logging externally, then inject them into the container explicitly. This ensures safe, predictable startup behavior.

### 💡 Pro Tip: Services vs. Providers

In .NET, IoC containers typically refer to registered components as **services**. You’ll often see code like:

```csharp
services.AddSingleton<ILogger>()
```

In Python, especially when using `dependency-injector`, these are referred to as **providers**:

```python
logger_factory = providers.Factory(StructLoggerFactory)
```

Both are mechanisms for wiring dependencies, but the terminology differs slightly:

| Concept            | .NET                                   | Python (`dependency_injector`)               |
| ------------------ | -------------------------------------- | -------------------------------------------- |
| Registered object  | **Service**                            | **Provider**                                 |
| Provides instance  | **Service provider**                   | **Provider instance**                        |
| Configuration unit | `IServiceCollection` (e.g. `services`) | `DeclarativeContainer` (e.g. `AppContainer`) |

This distinction reflects the focus: .NET emphasizes what you're getting (*services*), while Python emphasizes how it's built (*providers*).

This is especially helpful for developers transitioning between ecosystems.


## 🚧 Known Limitations / Notes

- Python's type system requires occasional use of `cast()` with `TypedDict` and DI frameworks
- `providers.Dependency()` is invariant and needs explicit typing/casting
- No runtime type enforcement — use `mypy` to validate correctness

For runtime-validated configs, consider integrating `pydantic`.

## License

MIT — free to use, modify, and learn from.

## Attribution

**Primary Author:** Gary McNickle (gmcnickle@outlook.com)<br>
**Co-Author & Assistant:** ChatGPT (OpenAI)

This project was collaboratively designed and developed through interactive sessions with ChatGPT, combining human experience and AI-driven support to solve real-world development challenges.

## Closing Thoughts
I hope this gives you some idea on how to loosely couple classes and their dependencies in python.  At the end of the day, doing so will make your code far easier to test, change, and maintain. Dependency injection is a powerful pattern for achieving these goals, but it does add some complexity initially.  I hope this has helped walk you through those challenges.

The provided code was meant to be illustrative of the concept, and not a framework itself.  Use these concepts as a foundation, and adapt them to fit your own projects and needs.

Best of luck. Reach out if you have questions.

[**Gary**](https://github.com/gmcnickle)  

[![GitHub](https://img.shields.io/badge/GitHub-%40gmcnickle-181717?logo=github&style=flat-square)](https://github.com/gmcnickle)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin&style=flat-square)](https://www.linkedin.com/in/gmcnickle)
![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python&logoColor=white)
