

def reverse(arr):
    print(len(arr) % 2)
    ac_len = len(arr) / 2
    for x in range(ac_len, 0):
            tmp = arr[x-1]
            arr[x] = arr[x-1]
            arr[x-1] = tmp
            print("eol")

    for x in arr:
        print(x)


a = [1, 2, 3, 4]
reverse(a)
