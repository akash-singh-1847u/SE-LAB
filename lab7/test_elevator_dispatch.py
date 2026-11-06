from hypothesis import given, settings, strategies as st
from elevator_dispatch import parse_request, total_travel, load_percent

# random text that looks a bit like real input, so the fuzzer gets past split()
messy = st.text(alphabet="0123456789-> ,of\t", max_size=20)
any_input = st.text() | st.none() | messy


@settings(max_examples=500)
@given(any_input)
def test_parse_request_no_crash(s):
    try:
        parse_request(s)
    except Exception as e:
        assert False, f"parse_request crashed with: {e!r}"


@settings(max_examples=500)
@given(any_input)
def test_total_travel_no_crash(s):
    try:
        total_travel(s)
    except Exception as e:
        assert False, f"total_travel crashed with: {e!r}"


@settings(max_examples=500)
@given(any_input)
def test_load_percent_no_crash(s):
    try:
        load_percent(s)
    except Exception as e:
        assert False, f"load_percent crashed with: {e!r}"


# valid input should still give the right answer

@given(st.integers(-5, 200), st.integers(-5, 200))
def test_parse_request_valid(a, b):
    assert parse_request(f"{a}->{b}") == (a, b)


@given(st.lists(st.integers(-5, 200), min_size=1, max_size=15))
def test_total_travel_valid(floors):
    expected = sum(abs(floors[i + 1] - floors[i]) for i in range(len(floors) - 1))
    assert total_travel(",".join(map(str, floors))) == expected


@given(st.integers(0, 2000), st.integers(1, 2000))
def test_load_percent_valid(load, cap):
    assert load_percent(f"{load} of {cap}") == load * 100 // cap
