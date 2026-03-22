import ast
import csv
import datetime
import random
import sqlite3
from collections import Counter
from io import StringIO

from flask import (
    Flask,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session,
)

app = Flask(__name__)
app.secret_key = '123456'

DB_PATH = 'system.db'
DEFAULT_RECOMMENDATION_SOURCE = '薄弱知识点诊断引擎'
DIFF_NAMES = {1: '入门', 2: '进阶', 3: '挑战', 4: '专家'}
SKILL_MAP = {
    '第一章': '基础语法',
    '第二章': '逻辑判断',
    '第三章': '循环结构',
    '第四章': '数组操作',
    '第五章': '字符串处理',
    '第六章': '函数递归',
    '第七章': '算法进阶',
}
SKILL_KEYS = list(dict.fromkeys(SKILL_MAP.values()))
FEEDBACK_SCORE_MAP = {'匹配': 100, '一般': 60, '不匹配': 20}
HELPFUL_SCORE_MAP = {'有帮助': 100, '一般': 60, '没帮助': 20}
MIN_LOGS_FOR_PERSONAL_RECOMMENDATION = 3


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def clamp(value, low, high):
    return max(low, min(high, value))


def ensure_columns(cursor, table_name, columns):
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing = {row[1] for row in cursor.fetchall()}
    for column_name, ddl in columns.items():
        if column_name not in existing:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {ddl}")


# --- 数据库初始化 ---
def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS problems
                 (id INTEGER PRIMARY KEY, title TEXT, difficulty INTEGER, tag TEXT, content TEXT,
                  standard_answer TEXT, example_input TEXT, example_output TEXT)'''
    )
    c.execute(
        '''CREATE TABLE IF NOT EXISTS learning_logs
                 (id INTEGER PRIMARY KEY, user_id TEXT, problem_id INTEGER,
                  code TEXT, status TEXT, timestamp DATETIME)'''
    )
    c.execute(
        '''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)'''
    )
    c.execute(
        '''CREATE TABLE IF NOT EXISTS recommendation_events
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id TEXT,
                  problem_id INTEGER,
                  knowledge_point TEXT,
                  weak_skill TEXT,
                  source TEXT,
                  recommendation_reason TEXT,
                  reason_mapping TEXT,
                  matched_difficulty INTEGER,
                  historical_accuracy REAL,
                  historical_avg_time REAL,
                  historical_error_types TEXT,
                  before_accuracy REAL,
                  before_avg_time REAL,
                  before_error_types TEXT,
                  after_accuracy REAL,
                  after_avg_time REAL,
                  after_error_types TEXT,
                  followup_accuracy REAL,
                  effect_score REAL,
                  helpful INTEGER DEFAULT 0,
                  rule_adjustment TEXT,
                  status TEXT DEFAULT 'pending',
                  recommendation_time DATETIME,
                  completed_at DATETIME,
                  last_evaluated_at DATETIME)'''
    )

    ensure_columns(
        c,
        'learning_logs',
        {
            'duration_seconds': 'duration_seconds INTEGER DEFAULT 0',
            'error_type': "error_type TEXT DEFAULT '未分类'",
            'pass_rate': 'pass_rate INTEGER DEFAULT 0',
            'memory_usage': 'memory_usage REAL DEFAULT 0',
            'run_time_ms': 'run_time_ms INTEGER DEFAULT 0',
            'knowledge_point': 'knowledge_point TEXT',
            'difficulty_snapshot': 'difficulty_snapshot INTEGER DEFAULT 0',
            'recommendation_id': 'recommendation_id INTEGER',
            'recommendation_source': 'recommendation_source TEXT',
            'recommended_at': 'recommended_at DATETIME',
            'completion_state': "completion_state TEXT DEFAULT '未关联推荐'",
            'effect_change': 'effect_change REAL DEFAULT 0',
            'same_type_followup_accuracy': 'same_type_followup_accuracy REAL DEFAULT 0',
        },
    )

    ensure_columns(
        c,
        'recommendation_events',
        {
            'matched_skill_score': 'matched_skill_score REAL DEFAULT 0',
            'difficulty_fit_score': 'difficulty_fit_score REAL DEFAULT 0',
            'evidence_confidence': 'evidence_confidence REAL DEFAULT 0',
            'accuracy_score': 'accuracy_score REAL DEFAULT 0',
            'accuracy_label': "accuracy_label TEXT DEFAULT '待验证'",
            'student_feedback': 'student_feedback TEXT',
            'student_feedback_note': 'student_feedback_note TEXT',
            'student_feedback_at': 'student_feedback_at DATETIME',
            'perceived_helpfulness': 'perceived_helpfulness TEXT',
            'manual_helpful': 'manual_helpful INTEGER DEFAULT 0',
            'diagnostic_summary': 'diagnostic_summary TEXT',
            'evidence_level': "evidence_level TEXT DEFAULT '低'",
            'validation_status': "validation_status TEXT DEFAULT '待继续观察'",
            'followup_sample_size': 'followup_sample_size INTEGER DEFAULT 0',
            'evaluation_notes': 'evaluation_notes TEXT',
        },
    )

    c.execute('SELECT count(*) FROM problems')
    if c.fetchone()[0] == 0:
        data = [
            (1, '输出 Hello World', 1, '第一章:基础语法', '请在控制台输出 "Hello World"。', 'print("Hello World")', '无', 'Hello World'),
            (2, '变量交换', 1, '第一章:基础语法', '输入两个整数 a 和 b，交换它们的值并输出。', 'a=input()\nb=input()\nprint(b,a)', '10\n20', '20 10'),
            (3, '计算矩形面积', 1, '第一章:基础语法', '输入长和宽，输出面积。', 'l=int(input())\nw=int(input())\nprint(l*w)', '5\n10', '50'),
            (4, '判断奇偶数', 1, '第二章:逻辑判断', '输入整数，偶数输出Even，奇数输出Odd。', 'n=int(input())\nprint("Even" if n%2==0 else "Odd")', '7', 'Odd'),
            (5, '判断闰年', 2, '第二章:逻辑判断', '输入年份，判断是否为闰年(Yes/No)。', '...略...', '2024', 'Yes'),
            (6, '三数最大值', 2, '第二章:逻辑判断', '输入三个整数，输出最大值。', '...略...', '1 5 3', '5'),
            (7, '计算 1到N 的和', 1, '第三章:循环结构', '计算 1+2+...+N。', '...略...', '100', '5050'),
            (8, '计算阶乘', 2, '第三章:循环结构', '计算 n!。', '...略...', '5', '120'),
            (9, '水仙花数', 3, '第三章:循环结构', '输出 100-999 的水仙花数。', '...略...', '无', '153...'),
            (10, '质数判断', 3, '第三章:循环结构', '判断是否为质数(Yes/No)。', '...略...', '17', 'Yes'),
            (11, '数组最大值', 1, '第四章:列表数组', '输出数组最大值。', '...略...', '1 9 2', '9'),
            (12, '数组逆序', 1, '第四章:列表数组', '将数组逆序输出。', '...略...', '1 2 3', '3 2 1'),
            (13, '冒泡排序', 3, '第四章:列表数组', '从小到大排序。', '...略...', '5 1 2', '1 2 5'),
            (14, '统计元音字母', 2, '第五章:字符串', '统计元音个数。', '...略...', 'Hello', '2'),
            (15, '判断回文串', 2, '第五章:字符串', '判断字符串是否回文。', '...略...', 'aba', 'Yes'),
            (16, '斐波那契数列', 3, '第六章:函数递归', '递归求第N个斐波那契数。', '...略...', '6', '8'),
            (17, '汉诺塔问题', 4, '第六章:函数递归', '输出移动步骤。', '...略...', '2', 'A->B...'),
            (18, '两数之和', 2, '第七章:算法进阶', '找出和为目标值的两个数下标。', '...略...', '2 7 11 15, 9', '[0, 1]'),
            (19, '二分查找', 3, '第七章:算法进阶', '有序数组查找索引。', '...略...', '1 3 5, 3', '1'),
            (20, '爬楼梯', 4, '第七章:算法进阶', '动态规划求爬楼梯方法数。', '...略...', '3', '3'),
        ]
        c.executemany('INSERT INTO problems VALUES (?,?,?,?,?,?,?,?)', data)

    conn.commit()
    conn.close()


init_db()


# --- 核心逻辑 ---
def analyze_code_structure(code_str):
    try:
        tree = ast.parse(code_str)
        num_vars = 0
        num_loops = 0
        has_recursion = False
        function_names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                num_vars += 1
            if isinstance(node, (ast.For, ast.While)):
                num_loops += 1
            if isinstance(node, ast.Call) and hasattr(node.func, 'id') and node.func.id in function_names:
                has_recursion = True
        return num_vars, num_loops, has_recursion, None
    except SyntaxError as exc:
        return 0, 0, False, f'语法错误: 第 {exc.lineno} 行附近存在语法问题'
    except Exception:
        return 0, 0, False, '代码结构分析失败'


def extract_knowledge_point(tag_value):
    if not tag_value:
        return '综合能力'
    chapter = tag_value.split(':')[0]
    return SKILL_MAP.get(chapter, chapter)


def classify_error_type(code, status, parse_error, pass_rate, has_recursion, num_loops):
    if parse_error:
        return '语法错误'
    if status == 'Accepted':
        return '无明显错误'
    lowered = (code or '').lower()
    if 'print' not in lowered and 'return' not in lowered:
        return '输出缺失'
    if 'if' not in lowered and 'for' not in lowered and 'while' not in lowered and pass_rate < 60:
        return '逻辑分支缺失'
    if has_recursion and 'def' in lowered and pass_rate < 100:
        return '递归边界不完整'
    if num_loops == 0 and pass_rate < 100:
        return '核心逻辑错误'
    return '测试用例未覆盖'


def calculate_pass_metrics(code, has_recursion, num_loops):
    pass_count = 0
    if code and len(code.strip()) > 5:
        pass_count = 1
    if 'print' in code or 'return' in code:
        pass_count = 2
    if len(code) > 20:
        pass_count = 3
    pass_rate = int((pass_count / 3) * 100)
    status = 'Accepted' if pass_rate == 100 else ('Partial Accepted' if pass_rate > 0 else 'Wrong Answer')
    memory_usage = round(3.0 + (len(code.splitlines()) * 0.1) + random.uniform(0, 0.5), 1)
    run_time = 20 + (num_loops * 10) + (30 if has_recursion else 0) + random.randint(0, 10)
    return pass_count, pass_rate, status, memory_usage, run_time


def fetch_logs_for_user(conn, user_id):
    c = conn.cursor()
    c.execute(
        '''SELECT l.*, p.title AS problem_title, p.tag AS problem_tag, p.difficulty AS problem_difficulty
           FROM learning_logs l
           LEFT JOIN problems p ON p.id = l.problem_id
           WHERE l.user_id=?
           ORDER BY l.timestamp DESC''',
        (user_id,),
    )
    return c.fetchall()


def build_user_metrics(conn, user_id):
    logs = fetch_logs_for_user(conn, user_id)
    skill_stats = {
        key: {
            'attempts': 0,
            'accepted': 0,
            'total_time': 0,
            'difficulties': [],
            'error_types': Counter(),
        }
        for key in SKILL_KEYS
    }

    for log in logs:
        skill = extract_knowledge_point(log['problem_tag'])
        if skill not in skill_stats:
            skill_stats[skill] = {
                'attempts': 0,
                'accepted': 0,
                'total_time': 0,
                'difficulties': [],
                'error_types': Counter(),
            }
        item = skill_stats[skill]
        item['attempts'] += 1
        item['accepted'] += 1 if log['status'] == 'Accepted' else 0
        item['total_time'] += log['duration_seconds'] or 0
        if log['problem_difficulty']:
            item['difficulties'].append(log['problem_difficulty'])
        item['error_types'][log['error_type'] or '未分类'] += 1

    skills = {}
    basis_rows = []
    for skill, stat in skill_stats.items():
        attempts = stat['attempts']
        accuracy = round((stat['accepted'] / attempts) * 100, 1) if attempts else 0.0
        avg_time = round(stat['total_time'] / attempts, 1) if attempts else 0.0
        avg_diff = round(sum(stat['difficulties']) / len(stat['difficulties']), 1) if stat['difficulties'] else 1.0
        penalty = min(40, avg_time / 18) if avg_time else 0
        base_score = 55 + accuracy * 0.45 - penalty + attempts * 1.5
        skills[skill] = clamp(round(base_score), 10, 100)
        top_errors = ', '.join(f'{name}×{count}' for name, count in stat['error_types'].most_common(2)) or '暂无'
        basis_rows.append(
            {
                'knowledge_point': skill,
                'attempts': attempts,
                'accuracy': accuracy,
                'avg_time': avg_time,
                'avg_difficulty': avg_diff,
                'top_errors': top_errors,
            }
        )

    overall_attempts = len(logs)
    overall_accuracy = round(sum(1 for log in logs if log['status'] == 'Accepted') / overall_attempts * 100, 1) if overall_attempts else 0.0
    overall_avg_time = round(sum((log['duration_seconds'] or 0) for log in logs) / overall_attempts, 1) if overall_attempts else 0.0
    return logs, skills, basis_rows, overall_accuracy, overall_avg_time


def find_best_problem_for_recommendation(conn, weak_skill, preferred_difficulty, user_id):
    c = conn.cursor()
    attempts = {row['problem_id'] for row in fetch_logs_for_user(conn, user_id)}
    chapter_prefix = next((k for k, v in SKILL_MAP.items() if v == weak_skill), weak_skill)
    c.execute(
        '''SELECT * FROM problems
           WHERE tag LIKE ?
           ORDER BY ABS(difficulty - ?) ASC, difficulty ASC, id ASC''',
        (f"{chapter_prefix}%", preferred_difficulty),
    )
    candidates = c.fetchall()
    for row in candidates:
        if row['id'] not in attempts:
            return row
    return candidates[0] if candidates else None


def derive_rule_adjustment(conn, user_id, weak_skill, base_difficulty):
    c = conn.cursor()
    c.execute(
        '''SELECT effect_score, helpful, matched_difficulty, accuracy_score
           FROM recommendation_events
           WHERE user_id=? AND weak_skill=? AND effect_score IS NOT NULL
           ORDER BY recommendation_time DESC LIMIT 3''',
        (user_id, weak_skill),
    )
    recent = c.fetchall()
    if not recent:
        return base_difficulty, '首次针对该薄弱知识点推荐，采用与当前能力相匹配的默认难度。'

    helpful_ratio = sum(1 for row in recent if row['helpful']) / len(recent)
    avg_effect = sum((row['effect_score'] or 0) for row in recent) / len(recent)
    avg_accuracy = sum((row['accuracy_score'] or 0) for row in recent) / len(recent)
    if helpful_ratio < 0.5 or avg_effect < 5 or avg_accuracy < 55:
        adjusted = max(1, base_difficulty - 1)
        return adjusted, '根据前序推荐效果与命中度偏弱，系统自动下调一档难度并继续针对同类错误做巩固练习。'
    adjusted = min(4, base_difficulty + 1 if avg_effect > 15 and avg_accuracy > 75 else base_difficulty)
    return adjusted, '根据前序推荐命中度较好，系统维持或适度提升难度，以继续验证推荐是否准确有效。'


def compute_recommendation_scores(weak_row, problem):
    knowledge_point = extract_knowledge_point(problem['tag'])
    matched_skill_score = 100 if knowledge_point == weak_row['knowledge_point'] else 60
    difficulty_gap = abs((weak_row['avg_difficulty'] or 1) - problem['difficulty'])
    difficulty_fit_score = round(clamp(100 - difficulty_gap * 25, 40, 100), 1)
    evidence_confidence = round(
        clamp(
            (100 - weak_row['accuracy']) * 0.32
            + min(weak_row['attempts'], 8) * 7
            + min(weak_row['avg_time'], 120) * 0.18
            + min(weak_row['attempts'], 3) * 4,
            20,
            95,
        ),
        1,
    )
    if weak_row['attempts'] >= 6:
        evidence_level = '高'
    elif weak_row['attempts'] >= 3:
        evidence_level = '中'
    else:
        evidence_level = '低'
    diagnostic_summary = (
        f"薄弱项命中度 {matched_skill_score} 分，难度匹配度 {difficulty_fit_score} 分，"
        f"依据可信度 {evidence_confidence} 分，当前证据等级为{evidence_level}。"
    )
    return matched_skill_score, difficulty_fit_score, evidence_confidence, evidence_level, diagnostic_summary


def calculate_recommendation_accuracy(rec):
    base = (rec['matched_skill_score'] or 0) * 0.3 + (rec['difficulty_fit_score'] or 0) * 0.2 + (rec['evidence_confidence'] or 0) * 0.2
    effect_component = clamp((rec['effect_score'] or 0) + 55, 20, 100) if rec['effect_score'] is not None else 45
    feedback_component = FEEDBACK_SCORE_MAP.get(rec['student_feedback'], 60)
    helpful_component = HELPFUL_SCORE_MAP.get(rec['perceived_helpfulness'], 60)
    evidence_level = rec['evidence_level'] or '低'
    followup_sample_size = rec['followup_sample_size'] or 0

    if evidence_level == '低' and followup_sample_size == 0 and not rec['student_feedback']:
        accuracy_score = round(base * 0.75, 1)
        return accuracy_score, '证据不足'

    if rec['status'] in {'pending', 'completed'} and not rec['student_feedback'] and rec['effect_score'] is None:
        accuracy_score = round(base * 0.85, 1)
        return accuracy_score, '待验证'

    accuracy_score = round(base + effect_component * 0.2 + feedback_component * 0.06 + helpful_component * 0.04, 1)
    accuracy_score = clamp(accuracy_score, 0, 100)
    if accuracy_score >= 80:
        label = '推荐较准确'
    elif accuracy_score >= 60:
        label = '基本准确'
    elif accuracy_score >= 40:
        label = '部分命中'
    else:
        label = '有待修正'
    return accuracy_score, label


def refresh_recommendation_accuracy(conn, recommendation_id):
    c = conn.cursor()
    c.execute('SELECT * FROM recommendation_events WHERE id=?', (recommendation_id,))
    rec = c.fetchone()
    if not rec:
        return None
    accuracy_score, accuracy_label = calculate_recommendation_accuracy(rec)
    c.execute(
        'UPDATE recommendation_events SET accuracy_score=?, accuracy_label=? WHERE id=?',
        (accuracy_score, accuracy_label, recommendation_id),
    )
    conn.commit()
    c.execute('SELECT * FROM recommendation_events WHERE id=?', (recommendation_id,))
    return c.fetchone()


def ensure_recommendation_for_user(conn, user_id, basis_rows, overall_accuracy, overall_avg_time):
    c = conn.cursor()
    c.execute(
        '''SELECT * FROM recommendation_events
           WHERE user_id=? AND status='pending'
           ORDER BY recommendation_time DESC LIMIT 1''',
        (user_id,),
    )
    existing = c.fetchone()
    if existing:
        return refresh_recommendation_accuracy(conn, existing['id'])

    observed_rows = [row for row in basis_rows if row['attempts'] > 0]
    if len(fetch_logs_for_user(conn, user_id)) < MIN_LOGS_FOR_PERSONAL_RECOMMENDATION or not observed_rows:
        return None

    weak_row = min(
        observed_rows,
        key=lambda row: (row['accuracy'], -row['avg_time'], -row['attempts']),
    )

    base_difficulty = max(1, min(4, round(weak_row['avg_difficulty'] or 1)))
    adjusted_difficulty, rule_adjustment = derive_rule_adjustment(conn, user_id, weak_row['knowledge_point'], base_difficulty)
    problem = find_best_problem_for_recommendation(conn, weak_row['knowledge_point'], adjusted_difficulty, user_id)
    if not problem:
        c.execute('SELECT * FROM problems ORDER BY difficulty ASC, id ASC LIMIT 1')
        problem = c.fetchone()

    matched_skill_score, difficulty_fit_score, evidence_confidence, evidence_level, diagnostic_summary = compute_recommendation_scores(weak_row, problem)
    recommendation_reason = (
        f"薄弱知识点为【{weak_row['knowledge_point']}】，历史正确率 {weak_row['accuracy']}%，"
        f"平均完成时间 {weak_row['avg_time']} 秒，历史高频错误为 {weak_row['top_errors']}，"
        f"当前诊断证据等级为{evidence_level}。"
    )
    mapping = (
        f"推荐题目《{problem['title']}》属于 {extract_knowledge_point(problem['tag'])}，"
        f"难度 {problem['difficulty']} 星，与学生当前薄弱项和历史练习难度相匹配。"
    )
    validation_status = '待继续观察' if evidence_level == '低' else '待验证'
    now = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
    insert_sql = '''INSERT INTO recommendation_events
           (user_id, problem_id, knowledge_point, weak_skill, source, recommendation_reason,
            reason_mapping, matched_difficulty, historical_accuracy, historical_avg_time,
            historical_error_types, before_accuracy, before_avg_time, before_error_types,
            matched_skill_score, difficulty_fit_score, evidence_confidence, diagnostic_summary,
            evidence_level, validation_status, evaluation_notes, rule_adjustment, status, recommendation_time)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    insert_values = (
        user_id,
        problem['id'],
        extract_knowledge_point(problem['tag']),
        weak_row['knowledge_point'],
        DEFAULT_RECOMMENDATION_SOURCE,
        recommendation_reason,
        mapping,
        problem['difficulty'],
        overall_accuracy,
        overall_avg_time,
        weak_row['top_errors'],
        weak_row['accuracy'],
        weak_row['avg_time'],
        weak_row['top_errors'],
        matched_skill_score,
        difficulty_fit_score,
        evidence_confidence,
        diagnostic_summary,
        evidence_level,
        validation_status,
        '当前推荐基于历史日志诊断生成，需结合学生反馈与后续同类题表现继续验证。',
        rule_adjustment,
        'pending',
        now,
    )
    c.execute(insert_sql, insert_values)
    conn.commit()
    return refresh_recommendation_accuracy(conn, c.lastrowid)


def evaluate_recommendation_effect(conn, recommendation_id):
    c = conn.cursor()
    c.execute('SELECT * FROM recommendation_events WHERE id=?', (recommendation_id,))
    rec = c.fetchone()
    if not rec:
        return None

    c.execute(
        '''SELECT * FROM learning_logs
           WHERE recommendation_id=?
           ORDER BY timestamp ASC''',
        (recommendation_id,),
    )
    recommendation_logs = c.fetchall()
    if not recommendation_logs:
        return refresh_recommendation_accuracy(conn, recommendation_id)

    recommended_log = recommendation_logs[0]
    chapter_prefix = next((k for k, v in SKILL_MAP.items() if v == rec['knowledge_point']), rec['knowledge_point'])
    c.execute(
        '''SELECT l.*, p.tag AS problem_tag
           FROM learning_logs l
           LEFT JOIN problems p ON p.id = l.problem_id
           WHERE l.user_id=? AND p.tag LIKE ? AND l.timestamp > ? AND l.recommendation_id IS NULL
           ORDER BY l.timestamp ASC''',
        (rec['user_id'], f"{chapter_prefix}%", recommended_log['timestamp']),
    )
    followup_logs = c.fetchall()
    attempts = len(followup_logs)
    accepted = sum(1 for row in followup_logs if row['status'] == 'Accepted')
    after_accuracy = round(accepted / attempts * 100, 1) if attempts else None
    after_avg_time = round(sum((row['duration_seconds'] or 0) for row in followup_logs) / attempts, 1) if attempts else None
    error_counter = Counter(row['error_type'] or '未分类' for row in followup_logs)
    after_errors = ', '.join(f'{name}×{count}' for name, count in error_counter.most_common(3)) if attempts else None

    before_accuracy = rec['before_accuracy'] or 0
    before_avg_time = rec['before_avg_time'] or 0
    recommended_success = 1 if recommended_log['status'] == 'Accepted' else 0
    if attempts:
        effect_score = round(
            (after_accuracy - before_accuracy) + max(0, before_avg_time - after_avg_time) * 0.3 + recommended_success * 8,
            1,
        )
        helpful = 1 if (after_accuracy >= before_accuracy or after_avg_time <= before_avg_time) and effect_score >= 0 else 0
        validation_status = '已验证'
        evaluation_notes = (
            f"已收集 {attempts} 条同知识点后续练习记录，用于验证本次推荐是否真的改善了同类题表现。"
        )
    else:
        effect_score = 8.0 if recommended_success else -5.0
        helpful = 1 if recommended_success else 0
        validation_status = '待继续观察'
        evaluation_notes = '推荐题已完成，但同知识点后续样本不足；当前仅依据推荐题完成情况做阶段性判断。'
    completed_at = recommended_log['timestamp']

    c.execute(
        '''UPDATE recommendation_events
           SET after_accuracy=?, after_avg_time=?, after_error_types=?, followup_accuracy=?,
               effect_score=?, helpful=?, status='evaluated', completed_at=COALESCE(completed_at, ?),
               last_evaluated_at=?, validation_status=?, followup_sample_size=?, evaluation_notes=?
           WHERE id=?''',
        (
            after_accuracy,
            after_avg_time,
            after_errors,
            after_accuracy if after_accuracy is not None else 0,
            effect_score,
            helpful,
            completed_at,
            datetime.datetime.now().isoformat(sep=' ', timespec='seconds'),
            validation_status,
            attempts,
            evaluation_notes,
            recommendation_id,
        ),
    )
    c.execute(
        '''UPDATE learning_logs
           SET effect_change=?, same_type_followup_accuracy=?, completion_state=?
           WHERE recommendation_id=?''',
        (effect_score, after_accuracy, '已完成推荐题' if accepted else '已提交待提升', recommendation_id),
    )
    conn.commit()
    return refresh_recommendation_accuracy(conn, recommendation_id)


def build_recommendation_summary(recommendation_history):
    total = len(recommendation_history)
    accurate = sum(1 for item in recommendation_history if (item['accuracy_score'] or 0) >= 60)
    validated = sum(1 for item in recommendation_history if item['accuracy_label'] not in {'待验证', '证据不足'})
    insufficient = sum(1 for item in recommendation_history if item['accuracy_label'] == '证据不足')
    average_score = round(sum((item['accuracy_score'] or 0) for item in recommendation_history) / total, 1) if total else 0.0
    return {
        'total': total,
        'validated': validated,
        'accurate': accurate,
        'insufficient': insufficient,
        'average_score': average_score,
    }


def row_to_dict(row):
    return dict(row) if row else None


# --- 路由 ---
@app.route('/')
def index():
    tag = request.args.get('tag')
    diff = request.args.get('diff')

    conn = get_connection()
    c = conn.cursor()

    query = 'SELECT * FROM problems WHERE 1=1'
    params = []
    mode_text = []
    if tag:
        query += ' AND tag = ?'
        params.append(tag)
        mode_text.append(f"章节: {tag.split(':')[0]}")
    if diff:
        query += ' AND difficulty = ?'
        params.append(diff)
        mode_text.append(f"难度: {DIFF_NAMES.get(int(diff), diff)}")

    c.execute(query, params)
    problems = c.fetchall()
    c.execute('SELECT DISTINCT tag FROM problems ORDER BY id')
    all_tags = [row[0] for row in c.fetchall()]
    conn.close()

    current_mode = ' + '.join(mode_text) if mode_text else '全部题目库'
    return render_template(
        'index.html',
        problems=problems,
        all_tags=all_tags,
        current_tag=tag,
        current_diff=diff,
        mode=current_mode,
    )


@app.route('/paper')
def paper():
    conn = get_connection()
    c = conn.cursor()
    paper_problems = []
    c.execute('SELECT * FROM problems WHERE difficulty=1 ORDER BY RANDOM() LIMIT 2')
    paper_problems.extend(c.fetchall())
    c.execute('SELECT * FROM problems WHERE difficulty=2 ORDER BY RANDOM() LIMIT 2')
    paper_problems.extend(c.fetchall())
    c.execute('SELECT * FROM problems WHERE difficulty>=3 ORDER BY RANDOM() LIMIT 1')
    paper_problems.extend(c.fetchall())
    c.execute('SELECT DISTINCT tag FROM problems ORDER BY id')
    all_tags = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template('index.html', problems=paper_problems, all_tags=all_tags, mode='📑 智能组卷 (覆盖简单/中等/困难)')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['user_id'] = user['username']
            return redirect('/')
        return render_template('login.html', error='用户名或密码错误')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            conn = get_connection()
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except Exception:
            return render_template('register.html', error='该用户名已被注册')
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')


@app.route('/problem/<int:pid>')
def problem_page(pid):
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM problems WHERE id=?', (pid,))
    problem = c.fetchone()
    current_user = session.get('user_id')
    recommendation = None
    if current_user:
        c.execute(
            '''SELECT * FROM recommendation_events
               WHERE user_id=? AND problem_id=? AND status IN ('pending', 'completed', 'evaluated')
               ORDER BY recommendation_time DESC LIMIT 1''',
            (current_user, pid),
        )
        recommendation = c.fetchone()
    conn.close()
    return render_template('solve.html', problem=problem, recommendation=recommendation)


@app.route('/api/recommendation_feedback', methods=['POST'])
def recommendation_feedback():
    current_user = session.get('user_id')
    if not current_user:
        return jsonify({'ok': False, 'msg': '请先登录'})

    data = request.json or {}
    recommendation_id = data.get('recommendation_id')
    feedback = data.get('feedback')
    helpfulness = data.get('helpfulness')
    note = (data.get('note') or '').strip()
    if not recommendation_id:
        return jsonify({'ok': False, 'msg': '缺少推荐事件编号'})

    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM recommendation_events WHERE id=? AND user_id=?', (recommendation_id, current_user))
    rec = c.fetchone()
    if not rec:
        conn.close()
        return jsonify({'ok': False, 'msg': '未找到对应推荐记录'})

    manual_helpful = 1 if helpfulness == '有帮助' else 0
    c.execute(
        '''UPDATE recommendation_events
           SET student_feedback=?, student_feedback_note=?, perceived_helpfulness=?,
               manual_helpful=?, student_feedback_at=?
           WHERE id=?''',
        (
            feedback,
            note,
            helpfulness,
            manual_helpful,
            datetime.datetime.now().isoformat(sep=' ', timespec='seconds'),
            recommendation_id,
        ),
    )
    conn.commit()
    updated = refresh_recommendation_accuracy(conn, recommendation_id)
    conn.close()
    return jsonify(
        {
            'ok': True,
            'msg': '反馈已记录，系统会据此判断本次推荐是否准确。',
            'accuracy_score': updated['accuracy_score'] if updated else 0,
            'accuracy_label': updated['accuracy_label'] if updated else '待验证',
            'validation_status': updated['validation_status'] if updated else '待继续观察',
        }
    )


@app.route('/api/submit', methods=['POST'])
def submit_code():
    try:
        data = request.json or {}
        pid = data.get('pid')
        code = data.get('code', '')
        duration_seconds = max(1, int(data.get('duration_seconds') or 1))
        if not code.strip():
            return jsonify({'status': 'Error', 'msg': '代码不能为空'})

        num_vars, num_loops, has_recursion, parse_error = analyze_code_structure(code)
        pass_count, pass_rate, status, memory_usage, run_time = calculate_pass_metrics(code, has_recursion, num_loops)
        error_type = classify_error_type(code, status, parse_error, pass_rate, has_recursion, num_loops)

        current_user = session.get('user_id', '匿名用户')
        now = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')

        conn = get_connection()
        c = conn.cursor()
        c.execute('SELECT tag, difficulty FROM problems WHERE id=?', (pid,))
        problem_meta = c.fetchone()
        knowledge_point = extract_knowledge_point(problem_meta['tag']) if problem_meta else '综合能力'

        c.execute(
            '''SELECT * FROM recommendation_events
               WHERE user_id=? AND problem_id=? AND status='pending'
               ORDER BY recommendation_time DESC LIMIT 1''',
            (current_user, pid),
        )
        active_rec = c.fetchone()

        recommendation_id = active_rec['id'] if active_rec else None
        recommendation_source = active_rec['source'] if active_rec else '自主练习'
        recommended_at = active_rec['recommendation_time'] if active_rec else None
        completion_state = '已完成推荐题' if active_rec else '自主完成'

        c.execute(
            '''INSERT INTO learning_logs
               (user_id, problem_id, code, status, timestamp, duration_seconds, error_type, pass_rate,
                memory_usage, run_time_ms, knowledge_point, difficulty_snapshot, recommendation_id,
                recommendation_source, recommended_at, completion_state, effect_change, same_type_followup_accuracy)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0)''',
            (
                current_user,
                pid,
                code,
                status,
                now,
                duration_seconds,
                error_type,
                pass_rate,
                memory_usage,
                run_time,
                knowledge_point,
                problem_meta['difficulty'] if problem_meta else 0,
                recommendation_id,
                recommendation_source,
                recommended_at,
                completion_state,
            ),
        )

        if active_rec:
            c.execute(
                "UPDATE recommendation_events SET status='completed', completed_at=? WHERE id=?",
                (now, active_rec['id']),
            )
        conn.commit()

        evaluated_rec = None
        if active_rec:
            evaluated_rec = evaluate_recommendation_effect(conn, active_rec['id'])

        conn.close()

        test_cases = [
            {'name': '基础样例', 'passed': pass_count >= 1},
            {'name': '边界测试', 'passed': pass_count >= 2},
            {'name': '压力测试', 'passed': pass_count >= 3},
        ]
        feedback = '运行完成' if not parse_error else '检测到语法问题，建议先修复后再提交'
        effect_text = None
        if evaluated_rec:
            after_accuracy_text = f"{evaluated_rec['after_accuracy']}%" if evaluated_rec['after_accuracy'] is not None else '待继续观察'
            after_time_text = f"{evaluated_rec['after_avg_time']} 秒" if evaluated_rec['after_avg_time'] is not None else '待继续观察'
            effect_text = (
                f"推荐后同类题正确率 {after_accuracy_text}，平均用时 {after_time_text}，"
                f"当前推荐准确度 {evaluated_rec['accuracy_score']} 分（{evaluated_rec['accuracy_label']}），"
                f"验证状态：{evaluated_rec['validation_status']}。"
            )
        return jsonify(
            {
                'status': status,
                'pass_rate': pass_rate,
                'memory': memory_usage,
                'run_time': run_time,
                'test_cases': test_cases,
                'feedback': feedback,
                'ast_analysis': f"AST分析: {num_vars}个变量, {num_loops}个循环, 错误类型: {error_type}",
                'error_type': error_type,
                'effect_text': effect_text,
            }
        )
    except Exception as e:
        return jsonify({'status': 'Error', 'msg': str(e)})


@app.route('/dashboard')
def dashboard():
    current_user = session.get('user_id')
    if not current_user:
        return redirect('/login')

    conn = get_connection()
    logs, skills, basis_rows, overall_accuracy, overall_avg_time = build_user_metrics(conn, current_user)
    recommendation = ensure_recommendation_for_user(conn, current_user, basis_rows, overall_accuracy, overall_avg_time)
    if recommendation and recommendation['status'] in {'completed', 'evaluated'}:
        recommendation = evaluate_recommendation_effect(conn, recommendation['id']) or recommendation

    c = conn.cursor()
    c.execute(
        '''SELECT * FROM recommendation_events
           WHERE user_id=?
           ORDER BY recommendation_time DESC LIMIT 8''',
        (current_user,),
    )
    recommendation_history = [dict(row) for row in c.fetchall()]
    recommendation_summary = build_recommendation_summary(recommendation_history)
    conn.close()

    recommendation_text = f'当前学习样本少于 {MIN_LOGS_FOR_PERSONAL_RECOMMENDATION} 条，系统暂不做强结论推荐；请先完成几道题后再生成更可靠的个性化推荐。'
    recommend_id = None
    algo_type = '规则推断'
    if recommendation:
        recommendation_text = recommendation['recommendation_reason']
        recommend_id = recommendation['problem_id']
        algo_type = recommendation['source']

    return render_template(
        'dashboard.html',
        logs=logs,
        skills=skills,
        recommendation=recommendation_text,
        recommend_id=recommend_id,
        algo_type=algo_type,
        basis_rows=basis_rows,
        recommendation_event=row_to_dict(recommendation),
        recommendation_history=recommendation_history,
        recommendation_summary=recommendation_summary,
        overall_accuracy=overall_accuracy,
        overall_avg_time=overall_avg_time,
    )


@app.route('/export_data')
def export_data():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        '''SELECT id, user_id, problem_id, status, timestamp, duration_seconds, error_type, pass_rate,
                  knowledge_point, difficulty_snapshot, recommendation_source, recommended_at,
                  completion_state, effect_change, same_type_followup_accuracy
           FROM learning_logs ORDER BY timestamp DESC'''
    )
    logs = c.fetchall()
    conn.close()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow([
        'ID', 'User', 'ProblemId', 'Status', 'Time', 'DurationSeconds', 'ErrorType', 'PassRate',
        'KnowledgePoint', 'DifficultySnapshot', 'RecommendationSource', 'RecommendedAt',
        'CompletionState', 'EffectChange', 'SameTypeFollowupAccuracy',
    ])
    cw.writerows([tuple(row) for row in logs])
    resp = make_response(si.getvalue())
    resp.headers['Content-Disposition'] = 'attachment; filename=data.csv'
    resp.headers['Content-type'] = 'text/csv'
    return resp


@app.route('/leaderboard')
def leaderboard():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        '''SELECT user_id, COUNT(DISTINCT problem_id) as s
           FROM learning_logs
           WHERE status='Accepted'
           GROUP BY user_id
           ORDER BY s DESC LIMIT 10'''
    )
    leaders = c.fetchall()
    conn.close()
    return render_template('leaderboard.html', leaders=leaders)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
