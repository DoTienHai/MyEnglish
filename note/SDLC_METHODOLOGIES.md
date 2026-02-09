# Agile, Scrum, Waterfall, V Model - Định Nghĩa & So Sánh

## 📌 Tổng Quan

SDLC có nhiều **Methodologies** (phương pháp tiếp cận) khác nhau. 4 cái phổ biến nhất:
1. **Waterfall** - Sequential phases
2. **Agile** - Iterative & incremental
3. **Scrum** - Agile framework (most popular)
4. **V Model** - Test-driven approach

---

## 1️⃣ Waterfall (瀑布式)

### Định Nghĩa
**Waterfall** là phương pháp SDLC **tuần tự (Sequential)**, mỗi phase phải hoàn thành trọn vẹn trước khi bắt đầu phase tiếp theo. Dòng chảy "như một thác nước" từ trên xuống.

### Các Phase
```
Requirements → Design → Development → Testing → Deployment → Maintenance
      ↓
    (Completed)
```

### Chi Tiết

| Yếu tố | Mô tả |
|--------|-------|
| **Timeline** | Xác định từ đầu, fixed schedule |
| **Scope** | Fixed, rất ít thay đổi |
| **Testing** | Sau development (1 phase riêng) |
| **Feedback** | Cuối project (sau development xong) |
| **Communication** | Documentation heavy (ít gặp mặt) |
| **Flexibility** | Thấp (khó thay đổi mid-project) |

### Ví Dụ Workflow

```
1. Month 1: Requirements
   ✅ Collect all requirements
   ✅ Document full specification
   ✅ Get client sign-off

2. Month 2: Design
   ✅ Architecture design
   ✅ Database schema
   ✅ UI mockups

3. Month 3: Development
   ✅ Code implementation
   ✅ Code review

4. Month 4: Testing
   ✅ QA testing
   ✅ Bug fixes

5. Month 5: Deployment
   ✅ Release to production

6. Ongoing: Maintenance
   ✅ Bug fixes, updates
```

### ✅ Ưu Điểm
- ✅ Clear timeline & budget
- ✅ Easy to plan & manage
- ✅ Good for fixed-scope projects
- ✅ Comprehensive documentation
- ✅ Works for large teams
- ✅ Suitable for regulated industries (banking, healthcare)

### ❌ Nhược Điểm
- ❌ Inflexible to changes
- ❌ Late testing → late bug discovery
- ❌ Client sees result at the end
- ❌ High risk if requirements misunderstood
- ❌ Long wait time for delivery
- ❌ Not good for evolving requirements

### 🎯 Khi Nào Dùng Waterfall
- ✅ Fixed requirements, clear scope
- ✅ Regulatory/compliance needs
- ✅ Large, established teams
- ✅ Government, banking, healthcare projects
- ✅ Hardware + Software integration

### ❌ Khi Nào KHÔNG Dùng
- ❌ Startup projects (requirements change)
- ❌ New technologies (learning as you go)
- ❌ Fast-moving markets
- ❌ Need rapid feedback from users

---

## 2️⃣ Agile (敏捷)

### Định Nghĩa
**Agile** là phương pháp SDLC **linh hoạt (Flexible)**, chia project thành các **Sprint** (1-4 tuần). Mỗi sprint tạo ra **Working Software**, được gửi cho user feedback.

**4 Giá Trị Agile:**
```
1. Individuals & Interactions > Processes & Tools
2. Working Software > Comprehensive Documentation
3. Customer Collaboration > Contract Negotiation
4. Responding to Change > Following a Plan
```

### Các Phase (trong mỗi Sprint)

```
Sprint Planning
      ↓
Sprint Backlog (Tasks)
      ↓
Daily Standup (15 min)
      ↓
Development & Testing (Parallel)
      ↓
Sprint Review (Demo to customer)
      ↓
Sprint Retrospective (Team reflection)
      ↓
❓ Continue next sprint?
```

### Chi Tiết

| Yếu tố | Mô tả |
|--------|-------|
| **Timeline** | Flexible, iterative sprints (1-4 weeks) |
| **Scope** | Evolving, backlog-driven |
| **Testing** | Continuous (within each sprint) |
| **Feedback** | Weekly/bi-weekly (after each sprint) |
| **Communication** | Daily standups, face-to-face |
| **Flexibility** | Cao (easy to pivot) |

### Ví Dụ Workflow

```
Sprint 1 (Week 1-2):
├── Plan: "Authentication module"
├── Develop & Test in parallel
├── Demo to customer
└── Feedback: "Add 2FA feature"

Sprint 2 (Week 3-4):
├── Plan: "2FA + Dashboard UI"
├── Develop & Test
├── Demo improvements
└── Feedback: "Good, continue"

Sprint 3 (Week 5-6):
├── Plan: "Vocabulary feature"
├── Prioritize based on customer feedback
└── Release MVP
```

### Agile Frameworks

#### 🔵 Scrum (Most Popular - 60% of Agile teams)
- **Sprint** based (1-4 weeks)
- **Roles**: Product Owner, Scrum Master, Team
- **Artifacts**: Product Backlog, Sprint Backlog, Increment
- **Ceremonies**: Planning, Daily Standup, Review, Retrospective

#### 🟢 Kanban
- Continuous flow (no predefined sprints)
- Focus on **Work In Progress (WIP)** limit
- Pull-based system
- Example: Trello board

#### 🟡 XP (Extreme Programming)
- Heavy emphasis on **Code Quality**
- Pair programming
- TDD (Test-Driven Development)
- Continuous integration

#### 🟣 Lean
- Minimize waste
- Amplify learning
- Decide late
- Deliver fast

### ✅ Ưu Điểm
- ✅ Flexible to changes
- ✅ Early & continuous feedback
- ✅ Quick time-to-market
- ✅ Team morale (celebrate wins)
- ✅ Working software each sprint
- ✅ Risk discovered early

### ❌ Nhược Điểm
- ❌ Difficult to predict budget/timeline
- ❌ Requires experienced team
- ❌ Heavy customer involvement needed
- ❌ Can be chaotic without discipline
- ❌ Scope creep risk
- ❌ Less documentation

### 🎯 Khi Nào Dùng Agile
- ✅ Startup projects
- ✅ requirements change frequently
- ✅ Need rapid feedback
- ✅ Innovative/new technologies
- ✅ Small to medium teams
- ✅ SaaS / Web projects

### ❌ Khi Nào KHÔNG Dùng
- ❌ Fixed requirements, fixed scope
- ❌ Regulated industries (strict docs needed)
- ❌ Large distributed teams (hard to communicate)
- ❌ Hardware-dependent projects

---

## 3️⃣ Scrum (스크럼)

### Định Nghĩa
**Scrum** là một **Agile Framework** (not a full SDLC methodology) nhấn mạnh **Team Collaboration** & **Iterative Development**. Nó quy định cách tổ chức team, processes, artifacts.

### Scrum Framework Components

#### 👥 Roles (3 roles)

| Role | Trách Nhiệm |
|------|-----------|
| **Product Owner** | ✅ Manage product backlog<br>✅ Prioritize features<br>✅ Talk to customers<br>✅ Decide release dates |
| **Scrum Master** | ✅ Facilitate Scrum ceremonies<br>✅ Remove blockers/impediments<br>✅ Coach team on Scrum<br>✅ Shield team from distractions |
| **Development Team** | ✅ Design, develop, test<br>✅ Self-organize<br>✅ Deliver increment each sprint<br>✅ 5-9 people ideal |

#### 📋 Artifacts (3 artifacts)

| Artifact | Mô Tả |
|----------|-------|
| **Product Backlog** | ✅ Prioritized list of features/user stories<br>✅ Maintained by Product Owner<br>✅ Example: "Create vocabulary dashboard" |
| **Sprint Backlog** | ✅ Tasks selected for current sprint<br>✅ Committed by team<br>✅ Updated daily |
| **Increment** | ✅ Working software at end of sprint<br>✅ Must be potentially shippable<br>✅ Demo to customer |

#### 🔄 Ceremonies (4 ceremonies)

| Ceremony | Duration | Purpose |
|----------|----------|---------|
| **Sprint Planning** | 2-4 hours | Plan sprint: What will we do? |
| **Daily Standup** | 15 minutes | Sync: What did I do? What will I do? Any blockers? |
| **Sprint Review** | 1-2 hours | Demo increment to customer, get feedback |
| **Sprint Retrospective** | 1-1.5 hours | Team reflection: What went well? What to improve? |

### Ví Dụ: MyEnglish Scrum Sprint

```
Sprint 1: Vocabulary Feature (2 weeks)

📌 Sprint Planning (Day 1, 3 hours)
├── Product Owner presents backlog items
├── Team discusses & estimates (story points)
└── Commitment: "Complete vocabulary CRUD + flashcard"

📊 Task Breakdown (Sprint Backlog)
├── [ ] Create Vocabulary model & repository (5 points)
├── [ ] Develop VocabularyService (3 points)
├── [ ] Build vocabulary UI (5 points)
├── [ ] Flashcard logic (5 points)
├── [ ] Unit tests (5 points)
└── [ ] Integration tests (3 points)
    Total: 26 story points

🔄 Daily Standup (Every morning, 15 min)
├── Dev 1: "Completed model & repo. Working on service. No blockers."
├── Dev 2: "Completed UI design. Starting flashcard logic. Need DB schema clarification."
├── Scrum Master: "Will help with DB schema today."

✅ Sprint Review (Day 15, 1.5 hours)
├── Demo: Vocabulary CRUD, flashcard working
├── Customer feedback: "Good! Please add word pronunciation feature"
├── Sprint velocity: 24 points completed (2 not done)

🤔 Sprint Retrospective (Day 15, 1 hour)
├── What went well: "Good communication, great teamwork"
├── What needs improvement: "DB schema docs earlier"
├── Action items:
│   ├── Document DB schema before coding
│   ├── Pair programming for complex features
│   └── Add pronunciation feature to next sprint backlog
```

### ✅ Ưu Điểm
- ✅ Clear structure & roles
- ✅ Regular feedback loops
- ✅ Team velocity tracking
- ✅ Predictable sprints
- ✅ Easy to onboard new members
- ✅ Works for co-located & distributed teams

### ❌ Nhược Điểm
- ❌ Scrum Master needed (additional cost)
- ❌ Can be bureaucratic for small teams
- ❌ Ceremonies take time
- ❌ Not suitable for very fast-moving projects
- ❌ Product Owner must be 100% available

### 🎯 Khi Nào Dùng Scrum
- ✅ Medium to large teams (8-50 people)
- ✅ Need structure & predictability
- ✅ Regular customer feedback important
- ✅ Corp environments (well-defined roles)
- ✅ SaaS, mobile app, web projects

---

## 4️⃣ V Model (V形模型)

### Định Nghĩa
**V Model** là phương pháp kết hợp **Waterfall + Rigorous Testing**. Mỗi Development Phase có tương ứng một **Testing Phase**. Hình chữ V: Going down = development, Going up = testing.

### Cấu Trúc V Model

```
Requirements ----------- Acceptance Testing
    ↓                            ↑
System Design ---------- System Testing
    ↓                            ↑
Module Design --------- Integration Testing
    ↓                            ↑
Implementation ------- Unit Testing
    ↓________________↑
       Code
```

### Chi Tiết

| Phase | Development | Testing Counterpart |
|-------|-------------|-------------------|
| **Requirements** | Gather & analyze | **UAT** (User Acceptance Testing) |
| **Design** | Architecture & design | **System Testing** |
| **Module Design** | Detailed design | **Integration Testing** |
| **Implementation** | Coding | **Unit Testing** |

### Ví Dụ Workflow

```
1. Requirements Phase
   ✅ Define all requirements
   ├── Test Plan created (for UAT later)
   └── Acceptance criteria defined

2. System Design
   ✅ Architecture designed
   ├── System test cases written
   └── Test environment prepared

3. Module Design
   ✅ Detailed design
   ├── Integration test cases
   └── Test data prepared

4. Implementation
   ✅ Code developed
   ├── Unit tests written & executed
   └── Code reviews

5. Integration Testing (Going UP)
   ✅ Integrate modules
   ✅ Run integration tests
   ✅ Fix issues

6. System Testing (Going UP)
   ✅ Test entire system
   ✅ Run system tests
   ✅ Fix issues

7. UAT (Going UP)
   ✅ Customer test
   ✅ Real-world scenarios
   ✅ Sign-off

8. Deployment & Maintenance
   ✅ Release & support
```

### ✅ Ưu Điểm
- ✅ Strong focus on **quality & testing**
- ✅ Test cases prepared early (before code)
- ✅ Reduces risk of bugs
- ✅ Good traceability (requirements → test cases)
- ✅ Clear phase gates
- ✅ Good for regulated industries

### ❌ Nhược Điểm
- ❌ Linear like Waterfall (not flexible)
- ❌ Testing happens late in cycle
- ❌ High resource cost (complex testing)
- ❌ Can delay delivery
- ❌ Difficult to accommodate changes
- ❌ Large documentation burden

### 🎯 Khi Nào Dùng V Model
- ✅ Safety-critical systems (medical, aerospace)
- ✅ Quality is paramount
- ✅ Requirements well-defined
- ✅ Regulated industries
- ✅ Large, fixed scope projects

### ❌ Khi Nào KHÔNG Dùng
- ❌ Agile/fast-moving projects
- ❌ Changing requirements
- ❌ Startup with limited resources
- ❌ Quick time-to-market needed

---

## 📊 So Sánh 4 Methodologies

### Bảng So Sánh Chi Tiết

| Yếu Tố | Waterfall | Agile | Scrum | V Model |
|--------|-----------|-------|-------|---------|
| **Timeline** | Fixed | Iterative | Fixed (per sprint) | Fixed (phase-based) |
| **Scope** | Fixed | Evolving | Evolving | Fixed |
| **Team Size** | Large | Small-Medium | 5-9 | Large |
| **Customer Involvement** | Low (front) | High (continuous) | High (daily) | Medium |
| **Testing** | End | Continuous | Continuous | Parallel (V-shape) |
| **Documentation** | Heavy | Light | Light | Heavy |
| **Flexibility** | Low | High | High | Low |
| **Risk** | High (late discovery) | Low (early) | Low (early) | Medium |
| **Delivery** | Once (end) | Frequently | Each sprint | Once (end) |
| **Learning Curve** | Easy | Medium | Medium-High | Medium |
| **Cost Predictability** | High | Low | Medium | High |
| **Change Management** | Difficult | Easy | Easy | Difficult |

### Diagram So Sánh

```
              Flexibility
                   ↑
                   │
        Agile (&Scrum)
              ●────●────●
             ╱         ╲
            ╱           ╲
           ╱             ╲
        Kanban         V Model
          ●               ●
                          
                          
       Waterfall          
          ●
          
          │
          └──────────────────→ Cost Predictability
          
Legend:
  ● = Each methodology
  Higher up = More flexible
  More right = More cost-predictable
```

---

## 3️⃣ Điều Gì Phù Hợp với MyEnglish Project?

### Project Characteristics
- ✅ Startup / New product
- ✅ Requirements changing (new features)
- ✅ Need fast feedback from users
- ✅ Small team (2-3 developers)
- ✅ Timeline flexible
- ✅ Budget flexible

### Recommendation: **SCRUM (Agile)**

#### 🎯 Tại Sao Scrum?

| Lý Do | Chi Tiết |
|------|---------|
| **Flexibility** | Easy to add new features (e.g., pronunciation, spaced repetition) |
| **Team Size** | Perfect for small teams |
| **User Feedback** | Get feedback every sprint (1-2 weeks) |
| **Fast Iteration** | MVP in 3-4 sprints (~8-16 weeks) |
| **Scalability** | Easy to expand team later (multiple scrum teams) |
| **Motivation** | Team sees working software frequently |

#### 📅 Scrum Plan untuk MyEnglish

```
Sprint 1 (Week 1-2): Core Infrastructure
├── Database setup & migrations
├── Authentication
└── Basic UI structure

Sprint 2 (Week 3-4): Translation Practice MVP
├── Paragraph CRUD
├── Sentence translation UI
├── Scoring integration
└── Basic testing

Sprint 3 (Week 5-6): Vocabulary Feature MVP
├── Vocabulary CRUD
├── Flashcard UI
├── Statistics tracking
└── Testing

Sprint 4 (Week 7-8): Polish & Optimization
├── UI/UX improvements
├── Performance optimization
├── Comprehensive testing
├── Deploy v1.0

Sprint 5+ (Week 9+): New Features
├── Based on user feedback
├── Consider: Pronunciation, Spaced Repetition, Gamification
```

#### 🏃 How to Implement Scrum for MyEnglish

```
Roles:
├── Product Owner: You (decide features & priorities)
├── Scrum Master: Team lead or self (facilitate process)
└── Dev Team: [Whoever codes]

Artifacts:
├── Product Backlog: [FEATURES_ROADMAP.md]
├── Sprint Backlog: [Create in GitHub Issues or Trello]
└── Increment: Working software each sprint

Ceremonies:
├── Sprint Planning: Monday morning 1 hour
├── Daily Standup: 15 min (async in Slack or video)
├── Sprint Review: Friday afternoon 1 hour
└── Retrospective: Friday afternoon 1 hour
```

---

## 📚 Quick Reference Table

```
Need Fixed Budget & Timeline?        → Waterfall
Need Flexibility & Quick Feedback?   → Agile / Scrum
Need Strong Testing & Quality?       → V Model
Small Team, Startup?                 → Agile / Scrum
Large Corporate Project?             → Waterfall / V Model
Safety-Critical System?              → V Model
Fast-Moving Market?                  → Agile / Scrum
```

---

## 🔗 SDLC Relationship

```
SDLC (Software Development Lifecycle)
  ├── 7 Phases (Generic)
  │   ├── 1. Planning
  │   ├── 2. Analysis
  │   ├── 3. Design
  │   ├── 4. Development
  │   ├── 5. Testing
  │   ├── 6. Deployment
  │   └── 7. Maintenance
  │
  └── Methodologies (Ways to execute phases)
      ├── Waterfall (Sequential)
      ├── Agile (Iterative)
      │   ├── Scrum ← Most popular
      │   ├── Kanban
      │   ├── XP
      │   └── Lean
      └── V Model (Test-driven Sequential)
```

---

**Last Updated:** February 9, 2026  
**For MyEnglish:** Recommend using **Scrum** (Agile Framework)
