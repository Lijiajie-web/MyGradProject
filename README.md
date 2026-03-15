# Personalized Recommendation and Guidance System for Programming Courses
## 面向程序设计课程的个性化推荐与指导系统

## Project Overview
This project is a Flask-based teaching support platform designed for programming courses. It integrates core functionalities such as user registration and login, problem display and filtering, random quiz generation, code submission, learning record tracking, learner-profile visualization, leaderboard display, and data export. The current version focuses on learning-log analysis, weak-point diagnosis, and AST-based code structure analysis to provide preliminary personalized guidance.

本项目是一个基于 Flask 开发的面向程序设计课程的教学支持平台。系统集成了用户注册与登录、题目展示与筛选、随机组卷、代码提交、学习记录追踪、学习画像可视化、排行榜展示以及数据导出等核心功能。当前版本主要通过学习日志分析、薄弱项诊断和 AST 代码结构分析，为学生提供初步的个性化指导。

---

## Background and Motivation
Programming courses are highly practice-oriented. Traditional exercise platforms often focus on static problem display and basic submission functions, while providing limited support for learner differentiation, process tracking, and targeted feedback. To address this issue, this project attempts to build a teaching support system that combines problem organization, learning-log recording, learner modeling, and code-structure analysis in one integrated prototype.

程序设计课程具有较强的实践性和连续性。传统练习平台通常侧重于题目展示与基础提交功能，在学习差异识别、过程留痕和针对性反馈方面支持不足。针对这一问题，本项目尝试构建一个集题目组织、学习记录保存、学习画像展示和代码结构分析于一体的教学支持系统原型。

---

## Core Functions
- User registration and login
- Problem display and filtering by difficulty and chapter
- Random quiz generation
- Code submission interface
- Learning-log recording
- Learner-profile visualization
- Leaderboard display
- Data export
- Preliminary personalized guidance based on learning records
- AST-based code structure analysis

## 核心功能
- 用户注册与登录
- 题目展示与按难度、章节筛选
- 随机组卷
- 代码提交界面
- 学习记录保存
- 学习画像可视化
- 排行榜展示
- 数据导出
- 基于学习记录的初步个性化指导
- 基于 AST 的代码结构分析

---

## System Features
1. **Teaching-oriented design**  
   The system is designed specifically for programming-course practice scenarios rather than for general online judging or commercial recommendation applications.

2. **Learning-log driven analysis**  
   Student interaction data, including submission records and status information, are stored in the database and used as the basis for learner modeling and feedback generation.

3. **Prototype-level personalized guidance**  
   The current version emphasizes weak-point diagnosis and learner support based on historical records, rather than claiming a fully deployed large-scale recommendation engine.

4. **AST-assisted feedback mechanism**  
   The system introduces Python AST-based code structure analysis to extract simple structural features from submitted code and support learning guidance.

## 系统特点
1. **面向教学场景设计**  
   系统面向程序设计课程练习场景构建，而不是通用在线评测平台或商业推荐平台。

2. **基于学习日志的数据分析**  
   系统将学生的提交记录和状态信息存入数据库，并以此作为学习画像与反馈生成的基础。

3. **原型化个性化指导机制**  
   当前版本以薄弱项诊断和历史记录分析为主，强调初步个性化指导，而不夸大为完整的大规模推荐引擎。

4. **AST 辅助反馈机制**  
   系统引入 Python AST 代码结构分析方法，对提交代码进行简单结构特征提取，用于辅助学习指导。

---

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite3
- **Frontend:** HTML, Template Rendering
- **Data Support:** Learning Logs
- **Analysis Method:** AST-based Code Structure Analysis
- **Version Control:** Git, GitHub

## 技术栈
- **后端：** Python、Flask
- **数据库：** SQLite3
- **前端：** HTML、模板渲染
- **数据基础：** 学习日志记录
- **分析方法：** 基于 AST 的代码结构分析
- **版本管理：** Git、GitHub

---

## Project Structure
```text
MyGradProject/
├── app.py
├── mock_data.py
├── system.db
└── templates/
    ├── dashboard.html
    ├── index.html
    ├── leaderboard.html
    ├── login.html
    ├── register.html
    └── solve.html
