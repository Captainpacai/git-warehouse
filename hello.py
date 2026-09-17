def main():
    name = input("你的名字：").strip() or "朋友"
    age = input("你的年龄：").strip() or "未知"
    gender = input("你的性别：").strip() or "未知"
    print(f"你好，{name}！你今年 {age} 岁，性别 {gender}。欢迎使用 git-warehouse。")


if __name__ == "__main__":
    main()
