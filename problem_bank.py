import json


SUPPORTED_LANGUAGES = {
    "python": {
        "name": "Python 3",
        "judge_name": "Python",
        "codemirror_mode": "python",
        "read_keywords": ["input(", "sys.stdin", "stdin"],
        "output_keywords": ["print("],
        "time_factor": 1.25,
        "memory_base": 10.0,
    },
    "cpp": {
        "name": "C++17",
        "judge_name": "C++",
        "codemirror_mode": "text/x-c++src",
        "read_keywords": ["cin", "scanf"],
        "output_keywords": ["cout", "printf"],
        "time_factor": 0.75,
        "memory_base": 6.0,
    },
    "java": {
        "name": "Java 17",
        "judge_name": "Java",
        "codemirror_mode": "text/x-java",
        "read_keywords": ["scanner", "bufferedreader", "system.in"],
        "output_keywords": ["system.out"],
        "time_factor": 1.45,
        "memory_base": 32.0,
    },
    "c": {
        "name": "C11",
        "judge_name": "C",
        "codemirror_mode": "text/x-csrc",
        "read_keywords": ["scanf", "fgets"],
        "output_keywords": ["printf", "puts"],
        "time_factor": 0.8,
        "memory_base": 5.0,
    },
}


STARTER_TEMPLATES = {
    "python": """# 请在这里编写 Python 3 代码
import sys

def solve():
    data = sys.stdin.read().strip().split()
    # TODO: 根据题目要求处理输入并输出结果

if __name__ == "__main__":
    solve()
""",
    "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // TODO: 根据题目要求处理输入并输出结果
    return 0;
}
""",
    "java": """import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        // TODO: 根据题目要求处理输入并输出结果
    }
}
""",
    "c": """#include <stdio.h>

int main(void) {
    // TODO: 根据题目要求处理输入并输出结果
    return 0;
}
""",
}


def _cases(*items):
    return json.dumps(
        [{"input": item[0], "output": item[1], "name": item[2]} for item in items],
        ensure_ascii=False,
    )


PROBLEMS = [
    {
        "id": 1,
        "title": "输出 Hello World",
        "difficulty": 1,
        "tag": "第一章:基础语法",
        "content": "请在控制台输出一行 Hello World。该题用于熟悉平台提交、标准输出和基础程序结构。",
        "example_input": "无",
        "example_output": "Hello World",
        "test_cases": _cases(("", "Hello World", "基础输出"), ("", "Hello World", "无输入场景")),
        "keywords": ["hello world"],
        "answers": {
            "python": """print("Hello World")
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    cout << "Hello World" << '\\n';
    return 0;
}
""",
            "java": """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    printf("Hello World\\n");
    return 0;
}
""",
        },
    },
    {
        "id": 2,
        "title": "变量交换",
        "difficulty": 1,
        "tag": "第一章:基础语法",
        "content": "输入两个整数 a 和 b，交换它们的值并按 b a 的顺序输出。两个数可以位于同一行或两行。",
        "example_input": "10 20",
        "example_output": "20 10",
        "test_cases": _cases(("10 20", "20 10", "基础交换"), ("-3 8", "8 -3", "含负数")),
        "keywords": ["input", "swap", "temp", "a", "b"],
        "answers": {
            "python": """a, b = map(int, input().split())
print(b, a)
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    int a, b;
    cin >> a >> b;
    cout << b << ' ' << a << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        System.out.println(b + " " + a);
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int a, b;
    scanf("%d%d", &a, &b);
    printf("%d %d\\n", b, a);
    return 0;
}
""",
        },
    },
    {
        "id": 3,
        "title": "计算矩形面积",
        "difficulty": 1,
        "tag": "第一章:基础语法",
        "content": "输入矩形的长和宽，输出矩形面积。输入均为整数，结果也为整数。",
        "example_input": "5 10",
        "example_output": "50",
        "test_cases": _cases(("5 10", "50", "基础面积"), ("7 3", "21", "普通数据")),
        "keywords": ["*", "area", "面积"],
        "answers": {
            "python": """length, width = map(int, input().split())
print(length * width)
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    long long length, width;
    cin >> length >> width;
    cout << length * width << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        long length = sc.nextLong();
        long width = sc.nextLong();
        System.out.println(length * width);
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    long long length, width;
    scanf("%lld%lld", &length, &width);
    printf("%lld\\n", length * width);
    return 0;
}
""",
        },
    },
    {
        "id": 4,
        "title": "判断奇偶数",
        "difficulty": 1,
        "tag": "第二章:逻辑判断",
        "content": "输入一个整数，若为偶数输出 Even，否则输出 Odd。",
        "example_input": "7",
        "example_output": "Odd",
        "test_cases": _cases(("7", "Odd", "奇数"), ("12", "Even", "偶数")),
        "keywords": ["%", "if", "even", "odd"],
        "answers": {
            "python": """n = int(input())
print("Even" if n % 2 == 0 else "Odd")
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    cout << (n % 2 == 0 ? "Even" : "Odd") << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        System.out.println(n % 2 == 0 ? "Even" : "Odd");
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    printf("%s\\n", n % 2 == 0 ? "Even" : "Odd");
    return 0;
}
""",
        },
    },
    {
        "id": 5,
        "title": "判断闰年",
        "difficulty": 2,
        "tag": "第二章:逻辑判断",
        "content": "输入一个年份，判断是否为闰年。是闰年输出 Yes，否则输出 No。",
        "example_input": "2024",
        "example_output": "Yes",
        "test_cases": _cases(("2024", "Yes", "普通闰年"), ("1900", "No", "世纪非闰年"), ("2000", "Yes", "世纪闰年")),
        "keywords": ["%", "400", "100", "4", "if"],
        "answers": {
            "python": """year = int(input())
is_leap = (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)
print("Yes" if is_leap else "No")
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    int year;
    cin >> year;
    bool isLeap = (year % 400 == 0) || (year % 4 == 0 && year % 100 != 0);
    cout << (isLeap ? "Yes" : "No") << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int year = sc.nextInt();
        boolean isLeap = (year % 400 == 0) || (year % 4 == 0 && year % 100 != 0);
        System.out.println(isLeap ? "Yes" : "No");
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int year;
    scanf("%d", &year);
    int isLeap = (year % 400 == 0) || (year % 4 == 0 && year % 100 != 0);
    printf("%s\\n", isLeap ? "Yes" : "No");
    return 0;
}
""",
        },
    },
    {
        "id": 6,
        "title": "三数最大值",
        "difficulty": 2,
        "tag": "第二章:逻辑判断",
        "content": "输入三个整数，输出其中的最大值。",
        "example_input": "1 5 3",
        "example_output": "5",
        "test_cases": _cases(("1 5 3", "5", "中间最大"), ("9 -2 4", "9", "第一个最大"), ("0 0 0", "0", "相等数据")),
        "keywords": ["max", "if", ">"],
        "answers": {
            "python": """nums = list(map(int, input().split()))
print(max(nums))
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    int a, b, c;
    cin >> a >> b >> c;
    cout << max(a, max(b, c)) << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        int b = sc.nextInt();
        int c = sc.nextInt();
        System.out.println(Math.max(a, Math.max(b, c)));
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int a, b, c;
    scanf("%d%d%d", &a, &b, &c);
    int ans = a;
    if (b > ans) ans = b;
    if (c > ans) ans = c;
    printf("%d\\n", ans);
    return 0;
}
""",
        },
    },
    {
        "id": 7,
        "title": "计算 1 到 N 的和",
        "difficulty": 1,
        "tag": "第三章:循环结构",
        "content": "输入正整数 N，计算并输出 1+2+...+N 的值。",
        "example_input": "100",
        "example_output": "5050",
        "test_cases": _cases(("100", "5050", "较大数据"), ("1", "1", "边界数据")),
        "keywords": ["for", "while", "sum", "n *"],
        "answers": {
            "python": """n = int(input())
print(n * (n + 1) // 2)
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n;
    cin >> n;
    cout << n * (n + 1) / 2 << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        long n = sc.nextLong();
        System.out.println(n * (n + 1) / 2);
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    long long n;
    scanf("%lld", &n);
    printf("%lld\\n", n * (n + 1) / 2);
    return 0;
}
""",
        },
    },
    {
        "id": 8,
        "title": "计算阶乘",
        "difficulty": 2,
        "tag": "第三章:循环结构",
        "content": "输入非负整数 n，输出 n!。测试数据保证结果在 64 位整数范围内。",
        "example_input": "5",
        "example_output": "120",
        "test_cases": _cases(("5", "120", "普通数据"), ("0", "1", "零阶乘")),
        "keywords": ["for", "while", "*=", "factorial"],
        "answers": {
            "python": """n = int(input())
ans = 1
for i in range(2, n + 1):
    ans *= i
print(ans)
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    long long ans = 1;
    for (int i = 2; i <= n; ++i) ans *= i;
    cout << ans << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        long ans = 1;
        for (int i = 2; i <= n; i++) ans *= i;
        System.out.println(ans);
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    long long ans = 1;
    for (int i = 2; i <= n; ++i) ans *= i;
    printf("%lld\\n", ans);
    return 0;
}
""",
        },
    },
    {
        "id": 9,
        "title": "水仙花数",
        "difficulty": 3,
        "tag": "第三章:循环结构",
        "content": "输出 100 到 999 之间所有水仙花数，数字之间用一个空格分隔。水仙花数是指各位数字立方和等于该数本身的三位数。",
        "example_input": "无",
        "example_output": "153 370 371 407",
        "test_cases": _cases(("", "153 370 371 407", "完整枚举")),
        "keywords": ["for", "100", "999", "%", "/"],
        "answers": {
            "python": """ans = []
for n in range(100, 1000):
    a = n // 100
    b = n // 10 % 10
    c = n % 10
    if a ** 3 + b ** 3 + c ** 3 == n:
        ans.append(str(n))
print(" ".join(ans))
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<int> ans;
    for (int n = 100; n <= 999; ++n) {
        int a = n / 100, b = n / 10 % 10, c = n % 10;
        if (a * a * a + b * b * b + c * c * c == n) ans.push_back(n);
    }
    for (int i = 0; i < (int)ans.size(); ++i) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    cout << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        List<Integer> ans = new ArrayList<>();
        for (int n = 100; n <= 999; n++) {
            int a = n / 100, b = n / 10 % 10, c = n % 10;
            if (a * a * a + b * b * b + c * c * c == n) ans.add(n);
        }
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) System.out.print(" ");
            System.out.print(ans.get(i));
        }
        System.out.println();
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int first = 1;
    for (int n = 100; n <= 999; ++n) {
        int a = n / 100, b = n / 10 % 10, c = n % 10;
        if (a * a * a + b * b * b + c * c * c == n) {
            if (!first) printf(" ");
            printf("%d", n);
            first = 0;
        }
    }
    printf("\\n");
    return 0;
}
""",
        },
    },
    {
        "id": 10,
        "title": "质数判断",
        "difficulty": 3,
        "tag": "第三章:循环结构",
        "content": "输入一个整数 n，判断 n 是否为质数。若是输出 Yes，否则输出 No。",
        "example_input": "17",
        "example_output": "Yes",
        "test_cases": _cases(("17", "Yes", "质数"), ("1", "No", "非正质数"), ("25", "No", "合数")),
        "keywords": ["for", "sqrt", "%", "prime"],
        "answers": {
            "python": """n = int(input())
if n < 2:
    print("No")
else:
    ok = True
    i = 2
    while i * i <= n:
        if n % i == 0:
            ok = False
            break
        i += 1
    print("Yes" if ok else "No")
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n;
    cin >> n;
    if (n < 2) {
        cout << "No\\n";
        return 0;
    }
    for (long long i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
            cout << "No\\n";
            return 0;
        }
    }
    cout << "Yes\\n";
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        long n = sc.nextLong();
        if (n < 2) {
            System.out.println("No");
            return;
        }
        for (long i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                System.out.println("No");
                return;
            }
        }
        System.out.println("Yes");
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    long long n;
    scanf("%lld", &n);
    if (n < 2) {
        printf("No\\n");
        return 0;
    }
    for (long long i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
            printf("No\\n");
            return 0;
        }
    }
    printf("Yes\\n");
    return 0;
}
""",
        },
    },
    {
        "id": 11,
        "title": "数组最大值",
        "difficulty": 1,
        "tag": "第四章:数组操作",
        "content": "输入若干个整数，输出其中的最大值。输入数据全部位于标准输入中，以空白符分隔。",
        "example_input": "1 9 2",
        "example_output": "9",
        "test_cases": _cases(("1 9 2", "9", "普通数组"), ("-8 -2 -5", "-2", "全负数")),
        "keywords": ["max", "for", "while", "array", "list"],
        "answers": {
            "python": """import sys
nums = list(map(int, sys.stdin.read().split()))
print(max(nums))
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    long long x, ans;
    if (!(cin >> ans)) return 0;
    while (cin >> x) ans = max(ans, x);
    cout << ans << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int ans = sc.nextInt();
        while (sc.hasNextInt()) ans = Math.max(ans, sc.nextInt());
        System.out.println(ans);
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int x, ans;
    if (scanf("%d", &ans) != 1) return 0;
    while (scanf("%d", &x) == 1) {
        if (x > ans) ans = x;
    }
    printf("%d\\n", ans);
    return 0;
}
""",
        },
    },
    {
        "id": 12,
        "title": "数组逆序",
        "difficulty": 1,
        "tag": "第四章:数组操作",
        "content": "输入若干个整数，将它们按逆序输出，数字之间用一个空格分隔。",
        "example_input": "1 2 3",
        "example_output": "3 2 1",
        "test_cases": _cases(("1 2 3", "3 2 1", "基础逆序"), ("5", "5", "单元素")),
        "keywords": ["reverse", "for", "array", "list"],
        "answers": {
            "python": """import sys
nums = sys.stdin.read().split()
print(" ".join(reversed(nums)))
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<string> nums;
    string x;
    while (cin >> x) nums.push_back(x);
    reverse(nums.begin(), nums.end());
    for (int i = 0; i < (int)nums.size(); ++i) {
        if (i) cout << ' ';
        cout << nums[i];
    }
    cout << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<String> nums = new ArrayList<>();
        while (sc.hasNext()) nums.add(sc.next());
        Collections.reverse(nums);
        System.out.println(String.join(" ", nums));
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int nums[1000], n = 0;
    while (scanf("%d", &nums[n]) == 1) n++;
    for (int i = n - 1; i >= 0; --i) {
        if (i != n - 1) printf(" ");
        printf("%d", nums[i]);
    }
    printf("\\n");
    return 0;
}
""",
        },
    },
    {
        "id": 13,
        "title": "冒泡排序",
        "difficulty": 3,
        "tag": "第四章:数组操作",
        "content": "输入若干个整数，将它们从小到大排序后输出，数字之间用一个空格分隔。",
        "example_input": "5 1 2",
        "example_output": "1 2 5",
        "test_cases": _cases(("5 1 2", "1 2 5", "普通排序"), ("3 3 1", "1 3 3", "重复元素")),
        "keywords": ["sort", "for", "swap", "bubble"],
        "answers": {
            "python": """import sys
nums = list(map(int, sys.stdin.read().split()))
nums.sort()
print(" ".join(map(str, nums)))
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<int> nums;
    int x;
    while (cin >> x) nums.push_back(x);
    sort(nums.begin(), nums.end());
    for (int i = 0; i < (int)nums.size(); ++i) {
        if (i) cout << ' ';
        cout << nums[i];
    }
    cout << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ArrayList<Integer> nums = new ArrayList<>();
        while (sc.hasNextInt()) nums.add(sc.nextInt());
        Collections.sort(nums);
        for (int i = 0; i < nums.size(); i++) {
            if (i > 0) System.out.print(" ");
            System.out.print(nums.get(i));
        }
        System.out.println();
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int nums[1000], n = 0;
    while (scanf("%d", &nums[n]) == 1) n++;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j + 1 < n - i; ++j) {
            if (nums[j] > nums[j + 1]) {
                int t = nums[j];
                nums[j] = nums[j + 1];
                nums[j + 1] = t;
            }
        }
    }
    for (int i = 0; i < n; ++i) {
        if (i) printf(" ");
        printf("%d", nums[i]);
    }
    printf("\\n");
    return 0;
}
""",
        },
    },
    {
        "id": 14,
        "title": "统计元音字母",
        "difficulty": 2,
        "tag": "第五章:字符串处理",
        "content": "输入一个字符串，统计其中元音字母 a、e、i、o、u 的数量，大小写均计入。",
        "example_input": "Hello",
        "example_output": "2",
        "test_cases": _cases(("Hello", "2", "含大写"), ("Programming", "3", "普通字符串")),
        "keywords": ["aeiou", "char", "string", "count"],
        "answers": {
            "python": """s = input().strip()
vowels = set("aeiouAEIOU")
print(sum(1 for ch in s if ch in vowels))
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    getline(cin, s);
    string vowels = "aeiouAEIOU";
    int ans = 0;
    for (char ch : s) {
        if (vowels.find(ch) != string::npos) ans++;
    }
    cout << ans << '\\n';
    return 0;
}
""",
            "java": """import java.io.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        String vowels = "aeiouAEIOU";
        int ans = 0;
        for (int i = 0; i < s.length(); i++) {
            if (vowels.indexOf(s.charAt(i)) >= 0) ans++;
        }
        System.out.println(ans);
    }
}
""",
            "c": """#include <stdio.h>
#include <string.h>

int main(void) {
    char s[1005];
    fgets(s, sizeof(s), stdin);
    int ans = 0;
    for (int i = 0; s[i]; ++i) {
        if (strchr("aeiouAEIOU", s[i])) ans++;
    }
    printf("%d\\n", ans);
    return 0;
}
""",
        },
    },
    {
        "id": 15,
        "title": "判断回文串",
        "difficulty": 2,
        "tag": "第五章:字符串处理",
        "content": "输入一个字符串，判断它是否为回文串。若是输出 Yes，否则输出 No。",
        "example_input": "aba",
        "example_output": "Yes",
        "test_cases": _cases(("aba", "Yes", "回文"), ("abc", "No", "非回文")),
        "keywords": ["reverse", "string", "left", "right"],
        "answers": {
            "python": """s = input().strip()
print("Yes" if s == s[::-1] else "No")
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    string s;
    cin >> s;
    string t = s;
    reverse(t.begin(), t.end());
    cout << (s == t ? "Yes" : "No") << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.next();
        String t = new StringBuilder(s).reverse().toString();
        System.out.println(s.equals(t) ? "Yes" : "No");
    }
}
""",
            "c": """#include <stdio.h>
#include <string.h>

int main(void) {
    char s[1005];
    scanf("%1000s", s);
    int l = 0, r = (int)strlen(s) - 1;
    while (l < r && s[l] == s[r]) {
        l++;
        r--;
    }
    printf("%s\\n", l >= r ? "Yes" : "No");
    return 0;
}
""",
        },
    },
    {
        "id": 16,
        "title": "斐波那契数列",
        "difficulty": 3,
        "tag": "第六章:函数递归",
        "content": "输入正整数 N，输出第 N 个斐波那契数。规定 F(1)=1，F(2)=1。",
        "example_input": "6",
        "example_output": "8",
        "test_cases": _cases(("6", "8", "普通数据"), ("1", "1", "边界数据")),
        "keywords": ["fib", "for", "while", "recursive"],
        "answers": {
            "python": """n = int(input())
if n <= 2:
    print(1)
else:
    a, b = 1, 1
    for _ in range(3, n + 1):
        a, b = b, a + b
    print(b)
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    long long a = 1, b = 1;
    if (n <= 2) {
        cout << 1 << '\\n';
        return 0;
    }
    for (int i = 3; i <= n; ++i) {
        long long c = a + b;
        a = b;
        b = c;
    }
    cout << b << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        long a = 1, b = 1;
        if (n <= 2) {
            System.out.println(1);
            return;
        }
        for (int i = 3; i <= n; i++) {
            long c = a + b;
            a = b;
            b = c;
        }
        System.out.println(b);
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    long long a = 1, b = 1;
    if (n <= 2) {
        printf("1\\n");
        return 0;
    }
    for (int i = 3; i <= n; ++i) {
        long long c = a + b;
        a = b;
        b = c;
    }
    printf("%lld\\n", b);
    return 0;
}
""",
        },
    },
    {
        "id": 17,
        "title": "汉诺塔问题",
        "difficulty": 4,
        "tag": "第六章:函数递归",
        "content": "输入圆盘数量 n，输出将 n 个圆盘从 A 柱移动到 C 柱的全部步骤。每一步格式为 A->C。",
        "example_input": "2",
        "example_output": "A->B\nA->C\nB->C",
        "test_cases": _cases(("2", "A->B\nA->C\nB->C", "两层汉诺塔")),
        "keywords": ["hanoi", "def", "void", "recursive", "->"],
        "answers": {
            "python": """def hanoi(n, src, aux, dst):
    if n == 1:
        print(f"{src}->{dst}")
        return
    hanoi(n - 1, src, dst, aux)
    print(f"{src}->{dst}")
    hanoi(n - 1, aux, src, dst)

n = int(input())
hanoi(n, "A", "B", "C")
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

void hanoi(int n, char src, char aux, char dst) {
    if (n == 1) {
        cout << src << "->" << dst << '\\n';
        return;
    }
    hanoi(n - 1, src, dst, aux);
    cout << src << "->" << dst << '\\n';
    hanoi(n - 1, aux, src, dst);
}

int main() {
    int n;
    cin >> n;
    hanoi(n, 'A', 'B', 'C');
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    static void hanoi(int n, char src, char aux, char dst) {
        if (n == 1) {
            System.out.println(src + "->" + dst);
            return;
        }
        hanoi(n - 1, src, dst, aux);
        System.out.println(src + "->" + dst);
        hanoi(n - 1, aux, src, dst);
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        hanoi(n, 'A', 'B', 'C');
    }
}
""",
            "c": """#include <stdio.h>

void hanoi(int n, char src, char aux, char dst) {
    if (n == 1) {
        printf("%c->%c\\n", src, dst);
        return;
    }
    hanoi(n - 1, src, dst, aux);
    printf("%c->%c\\n", src, dst);
    hanoi(n - 1, aux, src, dst);
}

int main(void) {
    int n;
    scanf("%d", &n);
    hanoi(n, 'A', 'B', 'C');
    return 0;
}
""",
        },
    },
    {
        "id": 18,
        "title": "两数之和",
        "difficulty": 2,
        "tag": "第七章:算法进阶",
        "content": "第一行输入若干个整数作为数组，第二行输入目标值 target。输出两个下标 i j，使 nums[i]+nums[j]=target。保证存在一组答案。",
        "example_input": "2 7 11 15\n9",
        "example_output": "0 1",
        "test_cases": _cases(("2 7 11 15\n9", "0 1", "经典样例"), ("3 2 4\n6", "1 2", "中间答案")),
        "keywords": ["map", "dict", "hash", "target"],
        "answers": {
            "python": """import sys
lines = sys.stdin.read().strip().splitlines()
nums = list(map(int, lines[0].split()))
target = int(lines[1])
pos = {}
for i, x in enumerate(nums):
    if target - x in pos:
        print(pos[target - x], i)
        break
    pos[x] = i
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> nums;
    int x;
    while (ss >> x) nums.push_back(x);
    int target;
    cin >> target;
    unordered_map<int, int> pos;
    for (int i = 0; i < (int)nums.size(); ++i) {
        int need = target - nums[i];
        if (pos.count(need)) {
            cout << pos[need] << ' ' << i << '\\n';
            return 0;
        }
        pos[nums[i]] = i;
    }
    return 0;
}
""",
            "java": """import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] parts = br.readLine().trim().split("\\\\s+");
        int[] nums = new int[parts.length];
        for (int i = 0; i < parts.length; i++) nums[i] = Integer.parseInt(parts[i]);
        int target = Integer.parseInt(br.readLine().trim());
        HashMap<Integer, Integer> pos = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int need = target - nums[i];
            if (pos.containsKey(need)) {
                System.out.println(pos.get(need) + " " + i);
                return;
            }
            pos.put(nums[i], i);
        }
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int nums[1000], n = 0, target;
    char ch;
    while (scanf("%d%c", &nums[n], &ch) == 2) {
        n++;
        if (ch == '\\n') break;
    }
    scanf("%d", &target);
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (nums[i] + nums[j] == target) {
                printf("%d %d\\n", i, j);
                return 0;
            }
        }
    }
    return 0;
}
""",
        },
    },
    {
        "id": 19,
        "title": "二分查找",
        "difficulty": 3,
        "tag": "第七章:算法进阶",
        "content": "第一行输入升序数组，第二行输入目标值 target。若找到目标值，输出其下标；否则输出 -1。",
        "example_input": "1 3 5\n3",
        "example_output": "1",
        "test_cases": _cases(("1 3 5\n3", "1", "命中数据"), ("1 3 5\n4", "-1", "未命中数据")),
        "keywords": ["binary", "left", "right", "mid"],
        "answers": {
            "python": """import sys
lines = sys.stdin.read().strip().splitlines()
nums = list(map(int, lines[0].split()))
target = int(lines[1])
l, r = 0, len(nums) - 1
while l <= r:
    mid = (l + r) // 2
    if nums[mid] == target:
        print(mid)
        break
    if nums[mid] < target:
        l = mid + 1
    else:
        r = mid - 1
else:
    print(-1)
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    vector<int> nums;
    int x;
    while (ss >> x) nums.push_back(x);
    int target;
    cin >> target;
    int l = 0, r = (int)nums.size() - 1;
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (nums[mid] == target) {
            cout << mid << '\\n';
            return 0;
        }
        if (nums[mid] < target) l = mid + 1;
        else r = mid - 1;
    }
    cout << -1 << '\\n';
    return 0;
}
""",
            "java": """import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] parts = br.readLine().trim().split("\\\\s+");
        int[] nums = new int[parts.length];
        for (int i = 0; i < parts.length; i++) nums[i] = Integer.parseInt(parts[i]);
        int target = Integer.parseInt(br.readLine().trim());
        int l = 0, r = nums.length - 1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (nums[mid] == target) {
                System.out.println(mid);
                return;
            }
            if (nums[mid] < target) l = mid + 1;
            else r = mid - 1;
        }
        System.out.println(-1);
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int nums[1000], n = 0, target;
    char ch;
    while (scanf("%d%c", &nums[n], &ch) == 2) {
        n++;
        if (ch == '\\n') break;
    }
    scanf("%d", &target);
    int l = 0, r = n - 1;
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (nums[mid] == target) {
            printf("%d\\n", mid);
            return 0;
        }
        if (nums[mid] < target) l = mid + 1;
        else r = mid - 1;
    }
    printf("-1\\n");
    return 0;
}
""",
        },
    },
    {
        "id": 20,
        "title": "爬楼梯",
        "difficulty": 4,
        "tag": "第七章:算法进阶",
        "content": "一次可以爬 1 级或 2 级台阶。输入台阶数 n，输出到达第 n 级台阶的不同方法数。",
        "example_input": "3",
        "example_output": "3",
        "test_cases": _cases(("3", "3", "小规模"), ("5", "8", "普通数据")),
        "keywords": ["dp", "fib", "for", "dynamic"],
        "answers": {
            "python": """n = int(input())
if n <= 2:
    print(n)
else:
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    print(b)
""",
            "cpp": """#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    if (n <= 2) {
        cout << n << '\\n';
        return 0;
    }
    long long a = 1, b = 2;
    for (int i = 3; i <= n; ++i) {
        long long c = a + b;
        a = b;
        b = c;
    }
    cout << b << '\\n';
    return 0;
}
""",
            "java": """import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        if (n <= 2) {
            System.out.println(n);
            return;
        }
        long a = 1, b = 2;
        for (int i = 3; i <= n; i++) {
            long c = a + b;
            a = b;
            b = c;
        }
        System.out.println(b);
    }
}
""",
            "c": """#include <stdio.h>

int main(void) {
    int n;
    scanf("%d", &n);
    if (n <= 2) {
        printf("%d\\n", n);
        return 0;
    }
    long long a = 1, b = 2;
    for (int i = 3; i <= n; ++i) {
        long long c = a + b;
        a = b;
        b = c;
    }
    printf("%lld\\n", b);
    return 0;
}
""",
        },
    },
]


def get_problem_records():
    records = []
    supported = ",".join(SUPPORTED_LANGUAGES.keys())
    for problem in PROBLEMS:
        answers = problem["answers"]
        records.append(
            {
                "id": problem["id"],
                "title": problem["title"],
                "difficulty": problem["difficulty"],
                "tag": problem["tag"],
                "content": problem["content"],
                "standard_answer": answers["python"],
                "example_input": problem["example_input"],
                "example_output": problem["example_output"],
                "answer_python": answers["python"],
                "answer_cpp": answers["cpp"],
                "answer_java": answers["java"],
                "answer_c": answers["c"],
                "supported_languages": supported,
                "time_limit_ms": 1000 + problem["difficulty"] * 250,
                "memory_limit_mb": 128,
                "test_cases": problem["test_cases"],
                "judge_keywords": json.dumps(problem["keywords"], ensure_ascii=False),
            }
        )
    return records

