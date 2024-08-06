print("This is my 2024.2.8 go back to python and protect it again ")
print("实现了一个二分查找")

if __name__ == "__main__":
    new = [1,2,3,4,5]
    right = (len(new) - 1)
    left = 0
    target = int(input("输入目标"))

    while True:
        mid = left + (right - left) // 2
        text = new[mid]
        if left > right:
            print("-1")
            break
        if text == target:
            print(mid)
            break
        elif target < text:
            right = mid - 1
        else:
            left = mid + 1