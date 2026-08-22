"""A dead connection must not poison the client for the rest of the run.

`requests.Session` pools keep-alive connections.  When one dies -- a laptop
suspending, a peer dropping the socket -- every later request on that pool
fails at the transport layer.  The client only rebuilt its session on a bad
HTTP *status*, so a transport failure left the dead pool in place and the
process timed out on every subsequent document forever.

Observed 2026-08-18: 27 consecutive 45-second read timeouts, while the same
URLs fetched in 2 seconds from a fresh session.  Silence looked identical to
slow progress, which is what made it expensive to spot.
"""

import unittest

import requests

from app.event_research.nse_client import NSEDocumentNotFound, NSEResearchClient, NSEUnavailable


class _FakeResponse:
    def __init__(self, status_code, content=b"ok"):
        self.status_code = status_code
        self.content = content


class _FakeSession:
    """One HTTP session. Outcomes come from a queue *shared* across sessions.

    Shared deliberately: the point of these tests is that the client moves on
    to the next outcome after rebuilding, rather than replaying the same failure
    against a fresh pool forever.
    """

    instances: list["_FakeSession"] = []

    def __init__(self, queue):
        self.queue = queue
        self.calls = 0
        self.closed = False
        self.headers = {}
        _FakeSession.instances.append(self)

    def get(self, url, **kwargs):
        self.calls += 1
        if not self.queue:
            return _FakeResponse(200)
        outcome = self.queue.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    def close(self):
        self.closed = True


class SessionRecoveryTests(unittest.TestCase):
    def setUp(self):
        _FakeSession.instances = []

    def _client(self, behaviours, **kwargs):
        client = NSEResearchClient(request_delay_seconds=0.0, **kwargs)
        queue = list(behaviours)

        def ensure():
            if client._session is None:
                client._session = _FakeSession(queue)
            return client._session

        client._ensure_session = ensure
        return client

    def test_transport_failure_rebuilds_the_session(self):
        """The regression: a read timeout must not reuse the dead pool."""
        behaviours = [
            requests.exceptions.ReadTimeout("read timed out"),
            _FakeResponse(200, b"recovered"),
        ]
        client = self._client(behaviours, max_attempts=3)
        self.assertEqual(client._get("u", referer="r", accept="a"), b"recovered")
        self.assertGreaterEqual(len(_FakeSession.instances), 2)
        self.assertTrue(_FakeSession.instances[0].closed)

    def test_connection_error_also_rebuilds(self):
        behaviours = [
            requests.exceptions.ConnectionError("peer reset"),
            _FakeResponse(200, b"recovered"),
        ]
        client = self._client(behaviours, max_attempts=3)
        self.assertEqual(client._get("u", referer="r", accept="a"), b"recovered")
        self.assertGreaterEqual(len(_FakeSession.instances), 2)

    def test_repeated_transport_failures_still_give_up_cleanly(self):
        behaviours = [requests.exceptions.ReadTimeout("timeout")] * 5
        client = self._client(behaviours, max_attempts=3)
        with self.assertRaises(NSEUnavailable):
            client._get("u", referer="r", accept="a")

    def test_404_is_raised_immediately_without_retrying(self):
        """A permanent absence must not burn the retry budget."""
        behaviours = [_FakeResponse(404, b""), _FakeResponse(200, b"never reached")]
        client = self._client(behaviours, max_attempts=3)
        with self.assertRaises(NSEDocumentNotFound):
            client._get("u", referer="r", accept="a")
        self.assertEqual(_FakeSession.instances[0].calls, 1)

    def test_empty_200_is_not_treated_as_success(self):
        behaviours = [_FakeResponse(200, b""), _FakeResponse(200, b"real content")]
        client = self._client(behaviours, max_attempts=3)
        self.assertEqual(client._get("u", referer="r", accept="a"), b"real content")


if __name__ == "__main__":
    unittest.main()
