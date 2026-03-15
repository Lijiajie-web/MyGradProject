# Intelligent Problem-Solving and Learning Recommendation System
## 智能算法刷题与学习推荐系统

## Project Overview
This project is a Flask-based intelligent learning platform designed for algorithm practice and personalized study support. It integrates core web functionalities such as user registration, login, problem display, and leaderboard management, while also exploring the application of collaborative filtering and AST (Abstract Syntax Tree) analysis for adaptive learning recommendation.

本项目是一个基于 Flask 开发的智能算法学习平台，面向编程练习与个性化学习支持场景，集成了用户注册、登录、题目展示、排行榜等基础功能，并进一步尝试将协同过滤推荐算法与 AST（抽象语法树）分析方法应用于学习推荐与代码分析中。

---

## Motivation
Traditional problem-solving platforms often focus mainly on static problem display and lack personalized support based on learner behavior or code characteristics. This project was developed to explore how recommendation techniques and code-structure analysis can be incorporated into an algorithm learning system, making the platform more adaptive and learner-centered.

传统刷题平台通常侧重于题目展示，较少结合学习者历史行为与代码特征提供个性化支持。本项目尝试构建一个“基础学习平台 + 个性化推荐 + 代码分析”的系统原型，以探索算法学习场景中的智能化学习支持方式。

---

## Core Features
- User registration and login
- Problem display and basic problem management
- Leaderboard visualization
- Learning data organization
- Personalized recommendation based on collaborative filtering
- Code structure analysis based on AST

## 核心功能
- 用户注册与登录
- 题目展示与基础管理
- 排行榜展示
- 学习数据组织与管理
- 基于协同过滤的个性化推荐
- 基于 AST 的代码结构分析

---

## Tech Stack
- **Backend:** Python, Flask
- **Database:** SQLite3
- **Frontend:** HTML, Template-based rendering
- **Algorithmic Components:** Collaborative Filtering, AST Analysis
- **Version Control:** Git, GitHub

## 技术栈
- **后端：** Python、Flask
- **数据库：** SQLite3
- **前端：** HTML、模板渲染
- **算法模块：** 协同过滤推荐、AST 抽象语法树分析
- **版本管理：** Git、GitHub

---

## Project Structure
```text
MyGradProject/
├── app.py
├── mock_data.py
└── templates/
    ├── dashboard.html
    ├── index.html
    ├── leaderboard.html
    ├── login.html
    └── register.html
