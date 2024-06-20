# SafeState Extension for Flask

The `SafeState` extension provides safe and convenient state management for Flask applications. It supports both synchronous and asynchronous contexts, allowing you to manage shared or isolated states easily.

## Installation

First, ensure you have Flask and `safestate` installed:

```bash
pip install flask-safestate
```

Next, include the `SafeState` class in your project.

## Usage

### Initialization

To initialize the `SafeState` extension, you can pass an instance of your Flask app, initial state data, and other configurations as needed.

```python
from flask import Flask
from flask_safestate import SafeState

app = Flask(__name__)
safestate = SafeState(app, data={"counter": 0}, isolated=True, is_async=False)
```

- `data`: Initial state data (default: empty dictionary).
- `isolated`: If `True`, each request will have its own isolated state (default: `False`).
- `is_async`: If `True`, the state will be managed asynchronously (default: `False`).
- `lock`: A lock object for synchronization (default: `None`).
- `callback`: A callback function for state updates (default: `None`).
- `errback`: A callback function for errors (default: `None`).

### Injecting State into Views

You can use the `with_state` decorator to inject the state into your view functions. The decorator supports both synchronous and asynchronous views.

#### Synchronous Views

```python
from flask import jsonify
from safestate_extension import with_state

@app.route('/increment', methods=['POST'])
@with_state()
def increment(state):
    state["counter"] += 1
    return jsonify(state["counter"])
```

#### Asynchronous Views

```python
from flask import jsonify
from safestate_extension import with_state

@app.route('/async-increment', methods=['POST'])
@with_state()
async def async_increment(state):
    state["counter"] += 1
    return jsonify(state["counter"])
```

### Unpacking State

If you want to unpack the state into the function arguments, set the `unpack` parameter to `True`.

```python
@app.route('/update', methods=['POST'])
@with_state(unpack=True)
def update(counter):
    counter += 1
    return jsonify(counter)
```

### Example Application

Here is a full example of a Flask application using the `SafeState` extension:

```python
from flask import Flask, jsonify, request
from safestate_extension import SafeState, with_state

app = Flask(__name__)
safestate = SafeState(app, data={"counter": 0}, isolated=True, is_async=False)

@app.route('/increment', methods=['POST'])
@with_state()
def increment(state):
    state["counter"] += 1
    return jsonify(state["counter"])

@app.route('/async-increment', methods=['POST'])
@with_state()
async def async_increment(state):
    state["counter"] += 1
    return jsonify(state["counter"])

@app.route('/update', methods=['POST'])
@with_state(unpack=True)
def update(counter):
    counter += 1
    return jsonify(counter)

if __name__ == '__main__':
    app.run(debug=True)
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.