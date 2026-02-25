"""Unit tests for shared observer base class"""
import pytest
from shared.observer_base import ObserverBase


class TestObserverBaseInitialization:
    """Tests for ObserverBase initialization"""

    def test_initialize_with_initial_value(self) -> None:
        """Test creating observer with initial value"""
        observer = ObserverBase(42)
        expected_value = 42
        
        assert observer.value == expected_value

    def test_initialize_with_string_value(self) -> None:
        """Test creating observer with string value"""
        observer = ObserverBase("initial")
        expected_value = "initial"
        
        assert observer.value == expected_value

    def test_initialize_with_list_value(self) -> None:
        """Test creating observer with list value"""
        initial = [1, 2, 3]
        observer = ObserverBase(initial)
        
        assert observer.value == initial

    def test_initialize_with_dict_value(self) -> None:
        """Test creating observer with dict value"""
        initial = {"key": "value"}
        observer = ObserverBase(initial)
        
        assert observer.value == initial

    def test_initialize_with_none_value(self) -> None:
        """Test creating observer with None value"""
        observer = ObserverBase(None)
        
        assert observer.value is None

    def test_initialize_with_zero(self) -> None:
        """Test creating observer with zero"""
        observer = ObserverBase(0)
        
        assert observer.value == 0

    def test_initialize_with_false(self) -> None:
        """Test creating observer with False"""
        observer = ObserverBase(False)
        
        assert observer.value is False

    def test_initialize_empty_subscriptions(self) -> None:
        """Test that new observer has no subscriptions"""
        observer = ObserverBase(10)
        
        assert len(observer._subs) == 0
        assert observer._subs == []


class TestObserverBaseSubscribe:
    """Tests for subscribe operation"""

    def test_subscribe_single_callback(self) -> None:
        """Test subscribing a single callback"""
        observer = ObserverBase(0)
        callback_called = []
        
        def callback(value):
            callback_called.append(value)
        
        observer.subscribe(callback)
        
        assert len(observer._subs) == 1

    def test_subscribe_multiple_callbacks(self) -> None:
        """Test subscribing multiple callbacks"""
        observer = ObserverBase(0)
        
        def callback1(value):
            pass
        
        def callback2(value):
            pass
        
        def callback3(value):
            pass
        
        observer.subscribe(callback1)
        observer.subscribe(callback2)
        observer.subscribe(callback3)
        
        assert len(observer._subs) == 3

    def test_subscribe_same_callback_twice(self) -> None:
        """Test subscribing same callback multiple times"""
        observer = ObserverBase(0)
        
        def callback(value):
            pass
        
        observer.subscribe(callback)
        observer.subscribe(callback)
        
        assert len(observer._subs) == 2

    def test_subscribe_lambda_function(self) -> None:
        """Test subscribing with lambda function"""
        observer = ObserverBase(0)
        
        observer.subscribe(lambda x: x * 2)
        
        assert len(observer._subs) == 1

    def test_subscribe_returns_none(self) -> None:
        """Test that subscribe returns None"""
        observer = ObserverBase(10)
        
        result = observer.subscribe(lambda x: None)
        
        assert result is None


class TestObserverBaseNotify:
    """Tests for notify operation"""

    def test_notify_calls_single_callback(self) -> None:
        """Test that notify calls registered callback"""
        observer = ObserverBase(0)
        results = []
        
        def callback(value):
            results.append(value)
        
        observer.subscribe(callback)
        observer.notify(42)
        
        assert results == [42]
        assert observer.value == 42

    def test_notify_calls_multiple_callbacks(self) -> None:
        """Test that notify calls all registered callbacks"""
        observer = ObserverBase(0)
        results1 = []
        results2 = []
        results3 = []
        
        def callback1(value):
            results1.append(value)
        
        def callback2(value):
            results2.append(value)
        
        def callback3(value):
            results3.append(value)
        
        observer.subscribe(callback1)
        observer.subscribe(callback2)
        observer.subscribe(callback3)
        observer.notify(100)
        
        assert results1 == [100]
        assert results2 == [100]
        assert results3 == [100]
        assert observer.value == 100

    def test_notify_updates_value(self) -> None:
        """Test that notify updates the observer's value"""
        observer = ObserverBase("old")
        observer.notify("new")
        expected_value = "new"
        
        assert observer.value == expected_value

    def test_notify_with_no_subscribers(self) -> None:
        """Test that notify works even with no subscribers"""
        observer = ObserverBase(5)
        observer.notify(10)
        expected_value = 10
        
        assert observer.value == expected_value

    def test_notify_with_string_value(self) -> None:
        """Test notify with string values"""
        observer = ObserverBase("initial")
        results = []
        
        observer.subscribe(lambda x: results.append(x))
        observer.notify("updated")
        
        assert observer.value == "updated"
        assert results == ["updated"]

    def test_notify_with_list_value(self) -> None:
        """Test notify with list values"""
        observer = ObserverBase([])
        results = []
        
        observer.subscribe(lambda x: results.append(x))
        observer.notify([1, 2, 3])
        
        assert observer.value == [1, 2, 3]
        assert results == [[1, 2, 3]]

    def test_notify_with_dict_value(self) -> None:
        """Test notify with dict values"""
        observer = ObserverBase({})
        results = []
        
        observer.subscribe(lambda x: results.append(x))
        observer.notify({"key": "value"})
        
        assert observer.value == {"key": "value"}
        assert results == [{"key": "value"}]

    def test_notify_with_none(self) -> None:
        """Test notify with None value"""
        observer = ObserverBase(10)
        results = []
        
        observer.subscribe(lambda x: results.append(x))
        observer.notify(None)
        
        assert observer.value is None
        assert results == [None]

    def test_notify_multiple_times(self) -> None:
        """Test notifying multiple times"""
        observer = ObserverBase(0)
        results = []
        
        observer.subscribe(lambda x: results.append(x))
        observer.notify(1)
        observer.notify(2)
        observer.notify(3)
        
        assert observer.value == 3
        assert results == [1, 2, 3]

    def test_notify_returns_none(self) -> None:
        """Test that notify returns None"""
        observer = ObserverBase(10)
        
        result = observer.notify(20)
        
        assert result is None


class TestObserverBaseIntegration:
    """Integration tests for observer pattern"""

    def test_subscribe_then_notify_workflow(self) -> None:
        """Test complete subscribe and notify workflow"""
        observer = ObserverBase("initial")
        results = []
        
        def callback(value):
            results.append(value)
        
        observer.subscribe(callback)
        assert observer.value == "initial"
        assert results == []
        
        observer.notify("updated")
        assert observer.value == "updated"
        assert results == ["updated"]

    def test_multiple_subscribers_receive_all_notifications(self) -> None:
        """Test that all subscribers receive notifications"""
        observer = ObserverBase(0)
        subscriber1_values = []
        subscriber2_values = []
        
        observer.subscribe(lambda x: subscriber1_values.append(x))
        observer.subscribe(lambda x: subscriber2_values.append(x))
        
        observer.notify(10)
        observer.notify(20)
        observer.notify(30)
        
        assert subscriber1_values == [10, 20, 30]
        assert subscriber2_values == [10, 20, 30]

    def test_observer_with_custom_callback_logic(self) -> None:
        """Test observer with callbacks that have custom logic"""
        observer = ObserverBase(0)
        results = []
        
        def double_callback(value):
            results.append(value * 2)
        
        observer.subscribe(double_callback)
        observer.notify(5)
        
        assert observer.value == 5
        assert results == [10]

    def test_observer_state_persists_across_notifications(self) -> None:
        """Test that observer state persists correctly"""
        observer = ObserverBase({"count": 0})
        
        observer.notify({"count": 1})
        assert observer.value == {"count": 1}
        
        observer.notify({"count": 2})
        assert observer.value == {"count": 2}

    def test_callback_receives_correct_value(self) -> None:
        """Test that callback receives the correct notified value"""
        observer = ObserverBase(None)
        received_values = []
        
        observer.subscribe(lambda x: received_values.append(x))
        
        test_values = [1, "test", [1, 2], {"key": "value"}, None]
        for val in test_values:
            observer.notify(val)
        
        assert received_values == test_values

    def test_observer_with_multiple_operations(self) -> None:
        """Test observer through multiple subscribe and notify operations"""
        observer = ObserverBase(0)
        tracker1 = []
        tracker2 = []
        
        observer.subscribe(lambda x: tracker1.append(x))
        observer.notify(1)
        
        observer.subscribe(lambda x: tracker2.append(x))
        observer.notify(2)
        
        observer.notify(3)
        
        assert tracker1 == [1, 2, 3]
        assert tracker2 == [2, 3]

    def test_observer_with_stateful_callback(self) -> None:
        """Test observer with callback that maintains state"""
        observer = ObserverBase(0)
        callback_state = {"count": 0}
        
        def stateful_callback(value):
            callback_state["count"] += 1
        
        observer.subscribe(stateful_callback)
        observer.notify(10)
        observer.notify(20)
        observer.notify(30)
        
        assert callback_state["count"] == 3


class TestObserverBaseEdgeCases:
    """Edge case tests for ObserverBase"""

    def test_observer_with_zero_initial_value(self) -> None:
        """Test observer initialized with 0"""
        observer = ObserverBase(0)
        results = []
        
        observer.subscribe(lambda x: results.append(x))
        observer.notify(0)
        
        assert observer.value == 0
        assert results == [0]

    def test_observer_with_empty_string(self) -> None:
        """Test observer with empty string"""
        observer = ObserverBase("")
        results = []
        
        observer.subscribe(lambda x: results.append(x))
        observer.notify("")
        
        assert observer.value == ""
        assert results == [""]

    def test_observer_with_empty_list(self) -> None:
        """Test observer with empty list"""
        observer = ObserverBase([])
        results = []
        
        observer.subscribe(lambda x: results.append(x))
        observer.notify([])
        
        assert observer.value == []
        assert results == [[]]

    def test_observer_with_empty_dict(self) -> None:
        """Test observer with empty dict"""
        observer = ObserverBase({})
        results = []
        
        observer.subscribe(lambda x: results.append(x))
        observer.notify({})
        
        assert observer.value == {}
        assert results == [{}]

    def test_observer_notification_order_preserved(self) -> None:
        """Test that notifications maintain order"""
        observer = ObserverBase(0)
        notifications = []
        
        observer.subscribe(lambda x: notifications.append(x))
        
        for i in range(100):
            observer.notify(i)
        
        assert notifications == list(range(100))
        assert observer.value == 99

    def test_callback_exceptions_propagate(self) -> None:
        """Test that exceptions in callbacks propagate"""
        observer = ObserverBase(0)
        
        def failing_callback(value):
            raise ValueError("Test error")
        
        observer.subscribe(failing_callback)
        
        with pytest.raises(ValueError, match="Test error"):
            observer.notify(10)

    def test_callback_modifying_observer_state(self) -> None:
        """Test callback accessing observer state"""
        observer = ObserverBase({"value": 0})
        callback_state = []
        
        def callback(value):
            callback_state.append(observer.value)
        
        observer.subscribe(callback)
        observer.notify({"value": 1})
        observer.notify({"value": 2})
        
        assert callback_state == [{"value": 1}, {"value": 2}]
