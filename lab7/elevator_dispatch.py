def to_int(value):
    # returns None instead of raising when the text is not a whole number
    try:
        return int(value.strip())
    except ValueError:
        return None


def parse_request(text):
    if not isinstance(text, str):
        return None
    parts = text.split('->')
    if len(parts) != 2:
        return None
    start, end = to_int(parts[0]), to_int(parts[1])
    if start is None or end is None:
        return None
    return start, end


def total_travel(floors_csv):
    if not isinstance(floors_csv, str) or not floors_csv.strip():
        return None
    floors = [to_int(f) for f in floors_csv.split(',')]
    if None in floors:
        return None
    return sum(abs(floors[i + 1] - floors[i]) for i in range(len(floors) - 1))


def load_percent(text):
    if not isinstance(text, str):
        return None
    parts = text.split(' of ')
    if len(parts) != 2:
        return None
    load, capacity = to_int(parts[0]), to_int(parts[1])
    if load is None or capacity is None:
        return None
    if load < 0 or capacity <= 0:
        return None
    return load * 100 // capacity


def show(label, result):
    if result is None:
        print(label, "invalid input")
    else:
        print(label, result)


def main():
    print("==== Running parse_request ====")
    user_input = input("Enter a request as FROM->TO (e.g. 5->9): ")
    show("From and To:", parse_request(user_input))

    print("\n==== Running total_travel ====")
    user_input = input("Enter floors visited as CSV (e.g. 1,5,3,9): ")
    show("Floors Travelled:", total_travel(user_input))

    print("\n==== Running load_percent ====")
    user_input = input("Enter load as 'X of Y' (e.g. 450 of 630): ")
    show("Load Percent:", load_percent(user_input))

if __name__ == "__main__":
    main()
