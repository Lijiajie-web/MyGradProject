import sqlite3
import random
from datetime import datetime, timedelta

# 连接数据库
conn = sqlite3.connect('system.db')
c = conn.cursor()

print("🤖 正在模拟学生 'student_01' 的做题历史...")

# 清空旧数据（保留表结构）
c.execute("DELETE FROM learning_logs")

# 模拟过去30天的行为
start_date = datetime.now() - timedelta(days=30)

# 生成 30 条记录
for i in range(30):
    # 随机时间
    random_days = random.randint(0, 30)
    log_time = start_date + timedelta(days=random_days)
    
    # 随机题目 (ID 1-4)
    pid = random.randint(1, 4)
    
    # 模拟做题结果：80%概率做对，20%概率做错
    is_accepted = random.random() < 0.8
    status = "Accepted" if is_accepted else "Wrong Answer"
    
    # 随便写点代码充数
    code = "print('Simulated Code')"
    
    # 插入数据库
    c.execute("INSERT INTO learning_logs (user_id, problem_id, code, status, timestamp) VALUES (?, ?, ?, ?, ?)",
              ("student_01", pid, code, status, log_time))

conn.commit()
print(f"✅ 成功插入 30 条模拟数据！请刷新 Dashboard 查看效果。")
conn.close()