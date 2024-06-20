import asyncio
from safestate import State, AsyncState
from functools import wraps
from flask import Flask, g

class SafeState:
    def __init__(self, app=None, data=None, isolated=False, is_async=False, lock=None, callback=None, errback=None):
        """Initializes the SafeState extension for safe state management.

        Args:
            app (Flask): Flask application instance.
            data (dict): Initial state data.
            isolated (bool): Indicates if the state should be request-isolated.
            is_async (bool): Indicates if the state should be asynchronous.
            lock (Lock): Lock object for synchronization.
            callback (Callable): Callback function for state updates.
            errback (Callable): Callback function for errors.
        """
        self.data = data or {}
        self.isolated = isolated
        self.is_async = is_async
        self.lock = lock
        self.callback = callback
        self.errback = errback

        # Initialize state based on async or sync mode
        if self.is_async:
            self.state = AsyncState(
                state=self.data,
                use_lock=not self.isolated,
                lock=self.lock,
                callback=self.callback,
                errback=self.errback
            )
        else:
            self.state = State(
                state=self.data,
                use_lock=not self.isolated,
                lock=self.lock,
                callback=self.callback,
                errback=self.errback
            )

        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initializes the extension with the Flask application.

        Args:
            app (Flask): Flask application instance.
        """
        app.safestate = self
        app.before_request(self.before_request)
        app.teardown_appcontext(self.teardown)

    def before_request(self):
        """Handler for before the request, setting the state in the global request context."""
        g.state = self.state.clone() if self.isolated else self.state

    def teardown(self, exception):
        """Handler for cleaning up the state at the end of the application context."""
        if not self.isolated:
            g.pop("state", None)

def with_state(unpack=False):
    """Decorator to inject the state into the view function.

    Args:
        unpack (bool): Indicates if the state should be unpacked as function arguments.

    Returns:
        Callable: Decorated function.
    """
    def decorator(view_func):
        @wraps(view_func)
        async def async_wrapper(*args, **kwargs):
            state = kwargs.pop("state", None) or g.state
            if not unpack:
                return await view_func(*args, state=state, **kwargs)
            else:
                return await view_func(*args, **state, **kwargs)

        @wraps(view_func)
        def sync_wrapper(*args, **kwargs):
            state = kwargs.pop("state", None) or g.state
            if not unpack:
                return view_func(*args, state=state, **kwargs)
            else:
                return view_func(*args, **state, **kwargs)

        if asyncio.iscoroutinefunction(view_func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
