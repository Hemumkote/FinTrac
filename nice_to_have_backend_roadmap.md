# FinTrac Backend - Nice-to-Have Features Implementation Roadmap

**Created:** February 14, 2026
**Prerequisite:** MVP backend complete (Phases 1-8 from BACKEND_ROADMAP.md)
**Architecture:** Routes -> Services -> Repositories -> SQLAlchemy ORM (same as core)
**Reference:** See `nice_to_have.md` for full feature descriptions

---

## Your Codebase Patterns (Same as Core)

| Layer | Location | Pattern |
|-------|----------|---------|
| Models | `app/models/` | SQLAlchemy `Base`, `Mapped`, `mapped_column` |
| Schemas | `app/schemas/` | Pydantic `BaseModel`, `Field`, enums as `str, Enum` |
| Repositories | `app/repositories/` | Class with `AsyncSession`, raw `select()` queries |
| Services | `services/` | Class with `AsyncSession`, creates repo internally |
| Routes | `api/routes/` | `APIRouter` with `Depends(get_async_session)` and `Depends(get_current_user)` |
| Migrations | `alembic/versions/` | Auto-generated via `alembic revision --autogenerate` |

---

## Post-MVP Phase 1: Group Expense Splitting

### Step 1.1 - Group Model

**File:** `app/models/group.py`

```
Table: groups
- id              (Integer, PK, indexed)
- name            (String(100), nullable=False)
- description     (String(255), nullable=True)
- created_by      (Integer, FK -> users.id)
- invite_code     (String(20), unique, indexed)   # shareable invite code
- image_url       (String(500), nullable=True)
- is_active       (Boolean, default=True)
- created_at      (DateTime, default=now)
- updated_at      (DateTime, default=now, onupdate=now)
```

### Step 1.2 - GroupMember Model

**File:** `app/models/group_member.py`

```
Table: group_members
- id              (Integer, PK)
- group_id        (Integer, FK -> groups.id, indexed)
- user_id         (Integer, FK -> users.id, indexed)
- role            (String(20), default='member')   # 'admin', 'member'
- joined_at       (DateTime, default=now)
- is_active       (Boolean, default=True)
```

**Constraints:**
- `UniqueConstraint("group_id", "user_id")` - user can only join a group once

### Step 1.3 - GroupExpense Model

**File:** `app/models/group_expense.py`

```
Table: group_expenses
- id              (Integer, PK, indexed)
- group_id        (Integer, FK -> groups.id, indexed)
- paid_by         (Integer, FK -> users.id)         # who paid
- description     (String(255), nullable=False)
- total_amount    (Numeric(12, 2), nullable=False)
- currency        (String(10), default='INR')
- category_id     (Integer, FK -> categories.id, nullable=True)
- split_method    (String(20), nullable=False)       # 'equal', 'unequal', 'percentage', 'shares'
- date            (Date, nullable=False)
- notes           (Text, nullable=True)
- receipt_url     (String(500), nullable=True)
- created_at      (DateTime)
- updated_at      (DateTime)
```

### Step 1.4 - ExpenseSplit Model

**File:** `app/models/expense_split.py`

```
Table: expense_splits
- id              (Integer, PK)
- group_expense_id (Integer, FK -> group_expenses.id, indexed)
- user_id         (Integer, FK -> users.id, indexed)
- amount_owed     (Numeric(12, 2))                   # what this user owes for this expense
- is_settled      (Boolean, default=False)
- created_at      (DateTime)
```

### Step 1.5 - GroupSettlement Model

**File:** `app/models/group_settlement.py`

```
Table: group_settlements
- id              (Integer, PK)
- group_id        (Integer, FK -> groups.id, indexed)
- paid_by         (Integer, FK -> users.id)          # who paid the settlement
- paid_to         (Integer, FK -> users.id)          # who received
- amount          (Numeric(12, 2))
- payment_method  (String(50), nullable=True)
- notes           (Text, nullable=True)
- settled_at      (DateTime, default=now)
- created_at      (DateTime)
```

### Step 1.6 - Group Schemas

**File:** `app/schemas/group.py`

```python
class SplitMethod(str, Enum):
    EQUAL = "equal"
    UNEQUAL = "unequal"
    PERCENTAGE = "percentage"
    SHARES = "shares"

class GroupCreate(BaseModel):
    name: str                          # min 1, max 100
    description: str | None = None

class GroupResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_by: int
    invite_code: str
    image_url: str | None
    is_active: bool
    member_count: int
    created_at: datetime
    updated_at: datetime

class GroupExpenseCreate(BaseModel):
    description: str
    total_amount: Decimal              # > 0
    category_id: int | None = None
    split_method: SplitMethod
    date: date
    notes: str | None = None
    splits: list[SplitDetail]          # who owes what

class SplitDetail(BaseModel):
    user_id: int
    amount: Decimal | None = None      # for unequal splits
    percentage: float | None = None    # for percentage splits
    shares: int | None = None          # for share-based splits

class GroupExpenseResponse(BaseModel):
    id: int
    group_id: int
    paid_by: int
    paid_by_name: str
    description: str
    total_amount: Decimal
    split_method: str
    date: date
    splits: list[SplitResponse]
    created_at: datetime

class SplitResponse(BaseModel):
    user_id: int
    user_name: str
    amount_owed: Decimal
    is_settled: bool

class SettlementCreate(BaseModel):
    paid_to: int                       # user_id of recipient
    amount: Decimal                    # > 0
    payment_method: str | None = None
    notes: str | None = None

class GroupBalanceResponse(BaseModel):
    group_id: int
    balances: list[MemberBalance]      # per-member net balance
    simplified_debts: list[SimplifiedDebt]  # minimized transactions

class MemberBalance(BaseModel):
    user_id: int
    user_name: str
    net_balance: Decimal               # positive = owed money, negative = owes money

class SimplifiedDebt(BaseModel):
    from_user_id: int
    from_user_name: str
    to_user_id: int
    to_user_name: str
    amount: Decimal
```

### Step 1.7 - Group Repository

**File:** `app/repositories/group_repository.py`

```python
class GroupRepository:
    async def create_group(self, group: Group) -> Group
    async def get_group_by_id(self, group_id: int) -> Group | None
    async def get_group_by_invite_code(self, code: str) -> Group | None
    async def get_user_groups(self, user_id: int) -> list[Group]
    async def add_member(self, group_id: int, user_id: int, role: str) -> GroupMember
    async def remove_member(self, group_id: int, user_id: int) -> None
    async def get_group_members(self, group_id: int) -> list[GroupMember]
    async def is_member(self, group_id: int, user_id: int) -> bool
```

**File:** `app/repositories/group_expense_repository.py`

```python
class GroupExpenseRepository:
    async def create_expense(self, expense: GroupExpense) -> GroupExpense
    async def create_splits(self, splits: list[ExpenseSplit]) -> list[ExpenseSplit]
    async def get_group_expenses(self, group_id: int) -> list[GroupExpense]
    async def get_expense_by_id(self, expense_id: int) -> GroupExpense | None
    async def delete_expense(self, expense_id: int) -> None
    async def create_settlement(self, settlement: GroupSettlement) -> GroupSettlement
    async def get_group_settlements(self, group_id: int) -> list[GroupSettlement]
    async def get_member_balances(self, group_id: int) -> list[dict]
```

### Step 1.8 - Group Service

**File:** `services/group_service.py`

```python
class GroupService:
    async def create_group(self, user_id: int, data: GroupCreate) -> GroupResponse
    async def join_group(self, user_id: int, invite_code: str) -> GroupResponse
    async def leave_group(self, user_id: int, group_id: int) -> None
    async def get_user_groups(self, user_id: int) -> list[GroupResponse]
    async def get_group_detail(self, user_id: int, group_id: int) -> GroupResponse
    async def add_expense(self, user_id: int, group_id: int, data: GroupExpenseCreate) -> GroupExpenseResponse
    async def delete_expense(self, user_id: int, expense_id: int) -> None
    async def record_settlement(self, user_id: int, group_id: int, data: SettlementCreate) -> dict
    async def get_group_balances(self, user_id: int, group_id: int) -> GroupBalanceResponse
    async def simplify_debts(self, group_id: int) -> list[SimplifiedDebt]
```

**Key business logic:**

**Split calculation (in service):**
```python
def calculate_splits(total: Decimal, method: SplitMethod, members: list, split_details: list) -> list:
    if method == SplitMethod.EQUAL:
        per_person = total / len(members)
        return [{user_id: m.user_id, amount: per_person} for m in members]
    elif method == SplitMethod.UNEQUAL:
        # Validate: sum of amounts == total
        return split_details
    elif method == SplitMethod.PERCENTAGE:
        # Validate: sum of percentages == 100
        return [{user_id: s.user_id, amount: total * s.percentage / 100} for s in split_details]
    elif method == SplitMethod.SHARES:
        total_shares = sum(s.shares for s in split_details)
        return [{user_id: s.user_id, amount: total * s.shares / total_shares} for s in split_details]
```

**Debt simplification algorithm (greedy):**
```python
def simplify_debts(balances: list[MemberBalance]) -> list[SimplifiedDebt]:
    # 1. Calculate net balance for each member (total owed - total owes)
    # 2. Separate into creditors (positive balance) and debtors (negative balance)
    # 3. Sort creditors descending, debtors ascending
    # 4. Match largest debtor with largest creditor
    # 5. Transfer min(debt, credit), adjust balances, repeat
    # Result: Minimal number of transactions to settle all debts
```

### Step 1.9 - Group Routes

**File:** `api/routes/groups.py`

```
POST   /api/v1/groups                              -> create_group
GET    /api/v1/groups                              -> get_user_groups
GET    /api/v1/groups/{id}                         -> get_group_detail
PUT    /api/v1/groups/{id}                         -> update_group
DELETE /api/v1/groups/{id}                         -> delete_group (admin only)
POST   /api/v1/groups/join                         -> join_group (body: {invite_code})
POST   /api/v1/groups/{id}/leave                   -> leave_group
GET    /api/v1/groups/{id}/members                 -> get_members
POST   /api/v1/groups/{id}/expenses                -> add_group_expense
GET    /api/v1/groups/{id}/expenses                -> get_group_expenses
DELETE /api/v1/groups/{id}/expenses/{expense_id}   -> delete_expense
POST   /api/v1/groups/{id}/settlements             -> record_settlement
GET    /api/v1/groups/{id}/settlements             -> get_settlements
GET    /api/v1/groups/{id}/balances                -> get_balances (includes simplified debts)
```

**Total endpoints: 14**

### Step 1.10 - Migration & Testing

1. Generate migration: `alembic revision --autogenerate -m "add_group_splitting_tables"`
2. Run migration: `alembic upgrade head`
3. Test all endpoints via Swagger
4. Test split calculations with edge cases (rounding, odd splits)

---

## Post-MVP Phase 2: SMS Auto-Import

### Step 2.1 - SMS Template Model

**File:** `app/models/sms_template.py`

```
Table: sms_templates
- id              (Integer, PK)
- bank_name       (String(100))
- sender_id       (String(20))          # e.g., "HDFCBK", "SBIINB"
- template_regex  (Text)                 # regex pattern to extract data
- transaction_type (String(20))          # 'debit' or 'credit'
- is_active       (Boolean, default=True)
- created_at      (DateTime)
```

### Step 2.2 - PendingTransaction Model

**File:** `app/models/pending_transaction.py`

```
Table: pending_transactions
- id              (Integer, PK, indexed)
- user_id         (Integer, FK -> users.id, indexed)
- raw_message     (Text)                 # original SMS text
- parsed_amount   (Numeric(12, 2), nullable=True)
- parsed_merchant (String(200), nullable=True)
- parsed_account  (String(50), nullable=True)
- parsed_date     (DateTime, nullable=True)
- suggested_category_id (Integer, FK -> categories.id, nullable=True)
- suggested_type  (String(20), nullable=True)  # income or expense
- status          (String(20), default='pending')  # pending, confirmed, dismissed, duplicate
- confidence      (Numeric(3, 2), nullable=True)   # 0.00 to 1.00
- created_at      (DateTime)
- updated_at      (DateTime)
```

### Step 2.3 - MerchantCategoryMapping Model

**File:** `app/models/merchant_mapping.py`

```
Table: merchant_category_mappings
- id              (Integer, PK)
- merchant_pattern (String(200), indexed)   # e.g., "SWIGGY", "ZOMATO", "UBER"
- category_id     (Integer, FK -> categories.id)
- is_global       (Boolean, default=True)   # system-level mapping
- user_id         (Integer, FK -> users.id, nullable=True)  # user-specific override
- created_at      (DateTime)
```

**Constraints:**
- `UniqueConstraint("merchant_pattern", "user_id")` - one mapping per merchant per user

### Step 2.4 - SMS Schemas

**File:** `app/schemas/sms_import.py`

```python
class SMSPayload(BaseModel):
    sender: str                        # SMS sender ID (e.g., "HDFCBK")
    message: str                       # full SMS text
    received_at: datetime

class SMSBatchPayload(BaseModel):
    messages: list[SMSPayload]         # batch upload from mobile

class PendingTransactionResponse(BaseModel):
    id: int
    raw_message: str
    parsed_amount: Decimal | None
    parsed_merchant: str | None
    parsed_date: datetime | None
    suggested_category_id: int | None
    suggested_category_name: str | None
    suggested_type: str | None
    confidence: float | None
    status: str
    created_at: datetime

class PendingTransactionAction(BaseModel):
    action: str                        # "confirm", "dismiss", "edit"
    category_id: int | None = None     # override category
    type: str | None = None            # override type
    amount: Decimal | None = None      # override amount
    description: str | None = None
```

### Step 2.5 - SMS Parser Service

**File:** `services/sms_parser_service.py`

```python
class SMSParserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.template_repo = SMSTemplateRepository(session)
        self.merchant_repo = MerchantMappingRepository(session)

    async def parse_sms(self, user_id: int, sms: SMSPayload) -> PendingTransactionResponse:
        # 1. Match sender ID to bank template
        # 2. Extract amount, merchant, account, date using regex
        # 3. Lookup merchant -> category mapping
        # 4. Check for duplicates (same amount, same date, within 5 min window)
        # 5. Create PendingTransaction record
        # 6. Return parsed result with confidence score

    async def parse_batch(self, user_id: int, batch: SMSBatchPayload) -> list[PendingTransactionResponse]

    async def confirm_pending(self, user_id: int, pending_id: int, action: PendingTransactionAction) -> dict:
        # If "confirm": Create real transaction from pending, mark as confirmed
        # If "dismiss": Mark as dismissed
        # If "edit": Apply overrides, then create transaction

    async def get_pending_transactions(self, user_id: int) -> list[PendingTransactionResponse]

    async def update_merchant_mapping(self, user_id: int, merchant: str, category_id: int) -> None:
        # Learn from user corrections
```

**Key regex patterns for Indian banks:**
```python
SMS_PATTERNS = {
    "HDFCBK": {
        "debit": r"Rs\.?(\d+[\d,]*\.?\d*) debited from a/c \*(\d+) .* to (.+?) on (\d{2}-\d{2}-\d{2})",
        "credit": r"Rs\.?(\d+[\d,]*\.?\d*) credited to a/c \*(\d+)"
    },
    "SBIINB": {
        "debit": r"debited by Rs\.?(\d+[\d,]*\.?\d*) .* A/c no\. XX(\d+)",
        "credit": r"credited by Rs\.?(\d+[\d,]*\.?\d*)"
    },
    "ICICIB": {
        "debit": r"Acct XX(\d+) debited with INR (\d+[\d,]*\.?\d*) .* Info: (.+)",
        "credit": r"Acct XX(\d+) credited with INR (\d+[\d,]*\.?\d*)"
    }
    # Add more banks...
}
```

### Step 2.6 - SMS Routes

**File:** `api/routes/sms_import.py`

```
POST   /api/v1/import/sms                          -> parse_sms           (single SMS)
POST   /api/v1/import/sms/batch                    -> parse_batch         (multiple SMS)
GET    /api/v1/import/pending                       -> get_pending         (list pending transactions)
POST   /api/v1/import/pending/{id}/action           -> process_pending    (confirm/dismiss/edit)
POST   /api/v1/import/pending/bulk-action           -> bulk_process       (confirm/dismiss multiple)
GET    /api/v1/import/merchant-mappings              -> get_mappings
PUT    /api/v1/import/merchant-mappings/{id}         -> update_mapping
```

**Total endpoints: 7**

### Step 2.7 - Seed Default Merchant Mappings

**File:** `scripts/seed_merchant_mappings.py`

```python
DEFAULT_MAPPINGS = [
    ("SWIGGY", "Food & Dining"),
    ("ZOMATO", "Food & Dining"),
    ("UBER", "Transport"),
    ("OLA", "Transport"),
    ("AMAZON", "Shopping"),
    ("FLIPKART", "Shopping"),
    ("NETFLIX", "Subscriptions"),
    ("SPOTIFY", "Subscriptions"),
    ("IRCTC", "Travel"),
    ("MAKEMYTRIP", "Travel"),
    ("BIGBASKET", "Groceries"),
    ("BLINKIT", "Groceries"),
    ("ZEPTO", "Groceries"),
    ("APOLLO", "Healthcare"),
    ("PHONEPE", "Other Expense"),    # UPI - needs context
    ("GPAY", "Other Expense"),
    # ... add 50+ common merchants
]
```

---

## Post-MVP Phase 3: Financial Goals

### Step 3.1 - FinancialGoal Model

**File:** `app/models/financial_goal.py`

```
Table: financial_goals
- id              (Integer, PK, indexed)
- user_id         (Integer, FK -> users.id, indexed)
- name            (String(100), nullable=False)
- description     (String(255), nullable=True)
- goal_type       (String(20))              # 'savings', 'debt_payoff', 'emergency_fund', 'custom'
- target_amount   (Numeric(12, 2))
- current_amount  (Numeric(12, 2), default=0)
- currency        (String(10), default='INR')
- target_date     (Date, nullable=True)
- linked_debt_id  (Integer, FK -> debt_credit_entries.id, nullable=True)
- color           (String(7), nullable=True)
- icon            (String(50), nullable=True)
- is_active       (Boolean, default=True)
- is_completed    (Boolean, default=False)
- completed_at    (DateTime, nullable=True)
- created_at      (DateTime)
- updated_at      (DateTime)
```

### Step 3.2 - GoalContribution Model

**File:** `app/models/goal_contribution.py`

```
Table: goal_contributions
- id              (Integer, PK)
- goal_id         (Integer, FK -> financial_goals.id, indexed)
- amount          (Numeric(12, 2))
- contribution_date (Date)
- notes           (Text, nullable=True)
- source          (String(50), nullable=True)   # 'manual', 'auto_rule', 'round_up'
- created_at      (DateTime)
```

### Step 3.3 - GoalAutoRule Model (Optional - for auto-allocation)

**File:** `app/models/goal_auto_rule.py`

```
Table: goal_auto_rules
- id              (Integer, PK)
- goal_id         (Integer, FK -> financial_goals.id)
- user_id         (Integer, FK -> users.id)
- rule_type       (String(30))              # 'percentage_of_income', 'fixed_daily', 'round_up'
- rule_value      (Numeric(12, 2))          # percentage or fixed amount
- is_active       (Boolean, default=True)
- created_at      (DateTime)
```

### Step 3.4 - Goal Schemas

**File:** `app/schemas/financial_goal.py`

```python
class GoalType(str, Enum):
    SAVINGS = "savings"
    DEBT_PAYOFF = "debt_payoff"
    EMERGENCY_FUND = "emergency_fund"
    CUSTOM = "custom"

class GoalCreate(BaseModel):
    name: str
    description: str | None = None
    goal_type: GoalType
    target_amount: Decimal              # > 0
    target_date: date | None = None
    linked_debt_id: int | None = None
    color: str | None = None
    icon: str | None = None

class GoalUpdate(BaseModel):
    name: str | None = None
    target_amount: Decimal | None = None
    target_date: date | None = None
    is_active: bool | None = None

class GoalResponse(BaseModel):
    id: int
    name: str
    description: str | None
    goal_type: str
    target_amount: Decimal
    current_amount: Decimal
    currency: str
    target_date: date | None
    percentage_complete: float          # current / target * 100
    remaining_amount: Decimal
    monthly_target: Decimal | None      # how much per month to hit target_date
    status: str                         # 'on_track', 'behind', 'ahead', 'completed'
    projected_completion: date | None   # based on current savings rate
    is_active: bool
    is_completed: bool
    created_at: datetime

class ContributionCreate(BaseModel):
    amount: Decimal                     # > 0
    contribution_date: date | None = None
    notes: str | None = None

class ContributionResponse(BaseModel):
    id: int
    goal_id: int
    amount: Decimal
    contribution_date: date
    source: str
    notes: str | None
    created_at: datetime
```

### Step 3.5 - Goal Repository, Service, Routes

**Repository:** `app/repositories/goal_repository.py`

```python
class GoalRepository:
    async def create_goal(self, goal: FinancialGoal) -> FinancialGoal
    async def get_user_goals(self, user_id: int, active_only: bool = True) -> list[FinancialGoal]
    async def get_goal_by_id(self, goal_id: int) -> FinancialGoal | None
    async def update_goal(self, goal: FinancialGoal) -> FinancialGoal
    async def delete_goal(self, goal_id: int) -> None
    async def add_contribution(self, contribution: GoalContribution) -> GoalContribution
    async def get_contributions(self, goal_id: int) -> list[GoalContribution]
```

**Service:** `services/goal_service.py`

```python
class GoalService:
    async def create_goal(self, user_id: int, data: GoalCreate) -> GoalResponse
    async def get_goals(self, user_id: int) -> list[GoalResponse]
    async def get_goal_detail(self, user_id: int, goal_id: int) -> GoalResponse
    async def update_goal(self, user_id: int, goal_id: int, data: GoalUpdate) -> GoalResponse
    async def delete_goal(self, user_id: int, goal_id: int) -> None
    async def add_contribution(self, user_id: int, goal_id: int, data: ContributionCreate) -> ContributionResponse
    async def get_contributions(self, user_id: int, goal_id: int) -> list[ContributionResponse]
```

**Key business logic:**
- `monthly_target` = (target_amount - current_amount) / months_remaining
- `status`:
  - `"completed"` if current_amount >= target_amount
  - `"on_track"` if current savings rate >= monthly_target
  - `"ahead"` if current savings rate > monthly_target * 1.1
  - `"behind"` if current savings rate < monthly_target * 0.9
- `projected_completion`: Based on average monthly contributions, calculate expected date
- On contribution: Update `current_amount`, check if goal completed

**Routes:** `api/routes/goals.py`

```
POST   /api/v1/goals                               -> create_goal
GET    /api/v1/goals                               -> get_goals
GET    /api/v1/goals/{id}                          -> get_goal_detail
PUT    /api/v1/goals/{id}                          -> update_goal
DELETE /api/v1/goals/{id}                          -> delete_goal
POST   /api/v1/goals/{id}/contributions            -> add_contribution
GET    /api/v1/goals/{id}/contributions            -> get_contributions
```

**Total endpoints: 7**

---

## Post-MVP Phase 4: Gamification

### Step 4.1 - Models

**File:** `app/models/gamification.py`

```
Table: user_streaks
- id              (Integer, PK)
- user_id         (Integer, FK -> users.id, unique, indexed)
- current_streak  (Integer, default=0)
- longest_streak  (Integer, default=0)
- last_active_date (Date, nullable=True)
- streak_freezes_remaining (Integer, default=1)   # resets weekly
- updated_at      (DateTime)

Table: badges
- id              (Integer, PK)
- code            (String(50), unique)       # 'budget_boss', 'debt_crusher', etc.
- name            (String(100))
- description     (String(255))
- icon            (String(50))
- category        (String(50))               # 'budgeting', 'saving', 'consistency', 'milestone'
- criteria_type   (String(50))               # 'streak_days', 'transactions_count', 'budget_months', etc.
- criteria_value  (Integer)                  # threshold to earn badge
- is_active       (Boolean, default=True)

Table: user_badges
- id              (Integer, PK)
- user_id         (Integer, FK -> users.id, indexed)
- badge_id        (Integer, FK -> badges.id, indexed)
- earned_at       (DateTime)

Table: financial_health_scores
- id              (Integer, PK)
- user_id         (Integer, FK -> users.id, indexed)
- score           (Integer)                  # 0-100
- savings_rate_score     (Integer)           # 0-30
- budget_adherence_score (Integer)           # 0-25
- debt_ratio_score       (Integer)           # 0-20
- emergency_fund_score   (Integer)           # 0-15
- consistency_score      (Integer)           # 0-10
- calculated_at   (DateTime)
- period          (String(20))               # 'monthly'

Table: savings_challenges
- id              (Integer, PK)
- user_id         (Integer, FK -> users.id, indexed)
- challenge_type  (String(50))               # '52_week', 'no_spend', 'round_up', 'custom'
- name            (String(100))
- target_amount   (Numeric(12, 2), nullable=True)
- current_amount  (Numeric(12, 2), default=0)
- start_date      (Date)
- end_date        (Date, nullable=True)
- is_active       (Boolean, default=True)
- is_completed    (Boolean, default=False)
- created_at      (DateTime)
```

**Constraints:**
- `UniqueConstraint("user_id", "badge_id")` on user_badges - earn each badge once

### Step 4.2 - Gamification Schemas

**File:** `app/schemas/gamification.py`

```python
class StreakResponse(BaseModel):
    current_streak: int
    longest_streak: int
    last_active_date: date | None
    streak_freezes_remaining: int

class BadgeResponse(BaseModel):
    id: int
    code: str
    name: str
    description: str
    icon: str
    category: str
    earned: bool
    earned_at: datetime | None

class FinancialHealthResponse(BaseModel):
    score: int                          # 0-100
    grade: str                          # A, B, C, D, F
    savings_rate_score: int
    budget_adherence_score: int
    debt_ratio_score: int
    emergency_fund_score: int
    consistency_score: int
    tips: list[str]                     # personalized improvement tips
    trend: str                          # 'improving', 'stable', 'declining'
    calculated_at: datetime

class ChallengeCreate(BaseModel):
    challenge_type: str
    name: str | None = None
    target_amount: Decimal | None = None
    start_date: date

class ChallengeResponse(BaseModel):
    id: int
    challenge_type: str
    name: str
    target_amount: Decimal | None
    current_amount: Decimal
    percentage_complete: float
    start_date: date
    end_date: date | None
    is_active: bool
    is_completed: bool
```

### Step 4.3 - Gamification Service

**File:** `services/gamification_service.py`

```python
class GamificationService:
    # Streaks
    async def update_streak(self, user_id: int) -> StreakResponse
        # Called whenever user logs a transaction
        # If last_active_date == yesterday: increment streak
        # If last_active_date == today: no change
        # If last_active_date < yesterday: check freeze, reset or use freeze

    # Badges
    async def check_and_award_badges(self, user_id: int) -> list[BadgeResponse]
        # Check all badge criteria against user's data
        # Award any newly earned badges

    async def get_user_badges(self, user_id: int) -> list[BadgeResponse]

    # Financial Health
    async def calculate_health_score(self, user_id: int) -> FinancialHealthResponse
        # Savings rate (30 pts): (income - expense) / income
        # Budget adherence (25 pts): % of budgets under limit
        # Debt ratio (20 pts): total_debt / monthly_income
        # Emergency fund (15 pts): savings / (monthly_expense * 3)
        # Consistency (10 pts): streak / 30

    async def generate_tips(self, score: FinancialHealthResponse) -> list[str]
        # Generate personalized tips based on weakest scores

    # Challenges
    async def create_challenge(self, user_id: int, data: ChallengeCreate) -> ChallengeResponse
    async def get_active_challenges(self, user_id: int) -> list[ChallengeResponse]
    async def update_challenge_progress(self, user_id: int, challenge_id: int, amount: Decimal) -> ChallengeResponse
```

### Step 4.4 - Gamification Routes

**File:** `api/routes/gamification.py`

```
GET    /api/v1/gamification/streak                  -> get_streak
GET    /api/v1/gamification/badges                  -> get_badges (all, with earned status)
GET    /api/v1/gamification/health-score             -> get_health_score
POST   /api/v1/gamification/challenges               -> create_challenge
GET    /api/v1/gamification/challenges               -> get_challenges
GET    /api/v1/gamification/summary                  -> get_gamification_summary (streak + badges + score)
```

**Total endpoints: 6**

### Step 4.5 - Seed Default Badges

**File:** `scripts/seed_badges.py`

```python
DEFAULT_BADGES = [
    # Consistency
    ("first_steps", "First Steps", "Logged your first transaction", "consistency", "transactions_count", 1),
    ("getting_started", "Getting Started", "Logged 10 transactions", "consistency", "transactions_count", 10),
    ("century_club", "Century Club", "Logged 100 transactions", "consistency", "transactions_count", 100),
    ("streak_7", "Week Warrior", "7-day logging streak", "consistency", "streak_days", 7),
    ("streak_30", "Monthly Master", "30-day logging streak", "consistency", "streak_days", 30),
    ("streak_100", "Unstoppable", "100-day logging streak", "consistency", "streak_days", 100),

    # Budgeting
    ("budget_set", "Budget Beginner", "Created your first budget", "budgeting", "budgets_created", 1),
    ("budget_boss", "Budget Boss", "Stayed under budget for 3 months", "budgeting", "budget_months_under", 3),
    ("budget_master", "Budget Master", "Stayed under budget for 6 months", "budgeting", "budget_months_under", 6),

    # Savings
    ("first_goal", "Goal Setter", "Created your first financial goal", "saving", "goals_created", 1),
    ("goal_achieved", "Goal Crusher", "Completed a financial goal", "saving", "goals_completed", 1),
    ("savings_star", "Savings Star", "Saved over ₹10,000 toward goals", "saving", "total_saved", 10000),

    # Debt
    ("debt_free", "Debt Free", "Settled all outstanding debts", "milestone", "all_debts_settled", 1),
    ("debt_crusher", "Debt Crusher", "Made 10 debt payments", "milestone", "debt_payments", 10),

    # Health Score
    ("health_a", "Financial Ace", "Achieved A grade financial health score", "milestone", "health_grade_a", 1),
]
```

### Step 4.6 - Integration with Transaction Service

After every transaction is created, trigger gamification updates:

```python
# In transaction_service.py -> create_transaction:
async def create_transaction(self, user_id, data):
    txn = await self.repository.create_transaction(...)

    # Trigger gamification (fire-and-forget or background task)
    gamification = GamificationService(self.session)
    await gamification.update_streak(user_id)
    await gamification.check_and_award_badges(user_id)

    return txn
```

---

## Post-MVP Phase 5: Subscription Manager

### Step 5.1 - Subscription Model

**File:** `app/models/subscription.py`

```
Table: subscriptions
- id              (Integer, PK, indexed)
- user_id         (Integer, FK -> users.id, indexed)
- name            (String(100), nullable=False)
- amount          (Numeric(12, 2))
- currency        (String(10), default='INR')
- billing_cycle   (String(20))               # 'monthly', 'yearly', 'weekly', 'quarterly'
- category_id     (Integer, FK -> categories.id, nullable=True)
- payment_method  (String(50), nullable=True)
- start_date      (Date)
- next_billing_date (Date)
- reminder_days   (Integer, default=3)        # remind N days before
- notes           (Text, nullable=True)
- is_active       (Boolean, default=True)
- is_free_trial   (Boolean, default=False)
- free_trial_end  (Date, nullable=True)
- created_at      (DateTime)
- updated_at      (DateTime)
```

### Step 5.2 - Subscription Schemas

**File:** `app/schemas/subscription.py`

```python
class BillingCycle(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class SubscriptionCreate(BaseModel):
    name: str
    amount: Decimal
    billing_cycle: BillingCycle
    category_id: int | None = None
    payment_method: str | None = None
    start_date: date
    reminder_days: int = 3
    notes: str | None = None
    is_free_trial: bool = False
    free_trial_end: date | None = None

class SubscriptionResponse(BaseModel):
    id: int
    name: str
    amount: Decimal
    billing_cycle: str
    category_name: str | None
    payment_method: str | None
    start_date: date
    next_billing_date: date
    days_until_renewal: int
    monthly_equivalent: Decimal         # normalized to monthly cost
    is_active: bool
    is_free_trial: bool
    free_trial_end: date | None
    free_trial_days_left: int | None
    created_at: datetime

class SubscriptionSummary(BaseModel):
    total_monthly_cost: Decimal
    total_yearly_cost: Decimal
    active_count: int
    upcoming_renewals: list[dict]       # next 7 days
    free_trials_expiring: list[dict]    # next 7 days
```

### Step 5.3 - Repository, Service, Routes

**Routes:** `api/routes/subscriptions.py`

```
POST   /api/v1/subscriptions                        -> create_subscription
GET    /api/v1/subscriptions                        -> get_subscriptions
GET    /api/v1/subscriptions/{id}                   -> get_subscription
PUT    /api/v1/subscriptions/{id}                   -> update_subscription
DELETE /api/v1/subscriptions/{id}                   -> delete_subscription
GET    /api/v1/subscriptions/summary                -> get_summary
POST   /api/v1/subscriptions/{id}/cancel            -> cancel_subscription
```

**Total endpoints: 7**

**Key business logic:**
- `monthly_equivalent`:
  - weekly: amount * 52 / 12
  - monthly: amount
  - quarterly: amount / 3
  - yearly: amount / 12
- `next_billing_date`: Auto-calculate based on billing_cycle and start_date
- Free trial alerts: Flag trials expiring within 7 days
- After next_billing_date passes, auto-advance to next cycle

---

## Post-MVP Phase 6: Net Worth Tracker

### Step 6.1 - Asset & Liability Models

**File:** `app/models/net_worth.py`

```
Table: assets
- id              (Integer, PK, indexed)
- user_id         (Integer, FK -> users.id, indexed)
- name            (String(100))
- asset_type      (String(50))               # 'bank_account', 'investment', 'property', 'fd', 'ppf', 'gold', 'crypto', 'other'
- current_value   (Numeric(14, 2))
- currency        (String(10), default='INR')
- institution     (String(100), nullable=True)  # bank name, broker, etc.
- notes           (Text, nullable=True)
- is_active       (Boolean, default=True)
- last_updated    (DateTime)
- created_at      (DateTime)

Table: asset_value_history
- id              (Integer, PK)
- asset_id        (Integer, FK -> assets.id, indexed)
- value           (Numeric(14, 2))
- recorded_at     (Date, indexed)
- created_at      (DateTime)

Table: net_worth_snapshots
- id              (Integer, PK)
- user_id         (Integer, FK -> users.id, indexed)
- total_assets    (Numeric(14, 2))
- total_liabilities (Numeric(14, 2))
- net_worth       (Numeric(14, 2))
- snapshot_date   (Date, indexed)
- breakdown       (JSON)                     # detailed breakdown by type
- created_at      (DateTime)
```

**Note:** Liabilities come from the existing `debt_credit_entries` table (payable type). No new model needed.

### Step 6.2 - Net Worth Schemas

**File:** `app/schemas/net_worth.py`

```python
class AssetType(str, Enum):
    BANK_ACCOUNT = "bank_account"
    INVESTMENT = "investment"
    PROPERTY = "property"
    FD = "fixed_deposit"
    PPF = "ppf"
    GOLD = "gold"
    CRYPTO = "crypto"
    OTHER = "other"

class AssetCreate(BaseModel):
    name: str
    asset_type: AssetType
    current_value: Decimal
    institution: str | None = None
    notes: str | None = None

class AssetUpdate(BaseModel):
    current_value: Decimal | None = None
    name: str | None = None
    notes: str | None = None
    is_active: bool | None = None

class AssetResponse(BaseModel):
    id: int
    name: str
    asset_type: str
    current_value: Decimal
    institution: str | None
    change_from_last: Decimal | None    # change since last update
    change_percentage: float | None
    is_active: bool
    last_updated: datetime

class NetWorthResponse(BaseModel):
    total_assets: Decimal
    total_liabilities: Decimal
    net_worth: Decimal
    assets_breakdown: list[dict]        # [{type, total, percentage}]
    liabilities_breakdown: list[dict]   # [{type, total, percentage}]
    trend: list[dict]                   # [{date, net_worth}] over time
    change_this_month: Decimal
    change_percentage: float
```

### Step 6.3 - Repository, Service, Routes

**Routes:** `api/routes/net_worth.py`

```
POST   /api/v1/net-worth/assets                     -> add_asset
GET    /api/v1/net-worth/assets                     -> get_assets
PUT    /api/v1/net-worth/assets/{id}                -> update_asset
DELETE /api/v1/net-worth/assets/{id}                -> delete_asset
GET    /api/v1/net-worth/summary                    -> get_net_worth_summary
GET    /api/v1/net-worth/history                    -> get_net_worth_history (trend over time)
POST   /api/v1/net-worth/snapshot                   -> take_snapshot (manual monthly snapshot)
```

**Total endpoints: 7**

**Key business logic:**
- When an asset value is updated, create a `asset_value_history` record
- `get_net_worth_summary`: Sum all active assets, subtract all active payable debts
- `take_snapshot`: Capture current net worth for historical tracking (auto-run monthly via cron or manual)
- Liabilities are pulled from `debt_credit_entries` where `type = 'payable'` and `status = 'active'`

---

## Post-MVP Phase 7: Shared / Family Budgets

### Step 7.1 - Models

**File:** `app/models/family.py`

```
Table: family_groups
- id              (Integer, PK)
- name            (String(100))
- created_by      (Integer, FK -> users.id)
- invite_code     (String(20), unique)
- created_at      (DateTime)
- updated_at      (DateTime)

Table: family_members
- id              (Integer, PK)
- family_group_id (Integer, FK -> family_groups.id, indexed)
- user_id         (Integer, FK -> users.id, indexed)
- role            (String(20))               # 'admin', 'editor', 'viewer'
- joined_at       (DateTime)

Table: shared_budgets
- id              (Integer, PK)
- family_group_id (Integer, FK -> family_groups.id, indexed)
- category_id     (Integer, FK -> categories.id, nullable=True)
- monthly_limit   (Numeric(12, 2))
- period          (String(20), default='monthly')
- is_active       (Boolean, default=True)
- created_at      (DateTime)

Table: shared_transactions
- id              (Integer, PK)
- family_group_id (Integer, FK -> family_groups.id, indexed)
- transaction_id  (Integer, FK -> transactions.id, indexed)   # links to existing transaction
- shared_by       (Integer, FK -> users.id)
- shared_at       (DateTime)
```

### Step 7.2 - Routes

```
POST   /api/v1/family                               -> create_family_group
GET    /api/v1/family                               -> get_family_groups
POST   /api/v1/family/join                          -> join_family
POST   /api/v1/family/{id}/budgets                  -> create_shared_budget
GET    /api/v1/family/{id}/budgets                  -> get_shared_budgets
GET    /api/v1/family/{id}/spending                 -> get_family_spending
POST   /api/v1/family/{id}/transactions/{txn_id}/share -> share_transaction_with_family
```

**Total endpoints: 7**

---

## Post-MVP Phase 8: Tax Helper (India-Specific)

### Step 8.1 - Models

**File:** `app/models/tax.py`

```
Table: tax_deductions
- id              (Integer, PK)
- user_id         (Integer, FK -> users.id, indexed)
- section         (String(20))               # '80C', '80D', '80E', '24b', 'hra'
- name            (String(100))              # e.g., "ELSS - Axis Bluechip"
- amount          (Numeric(12, 2))
- financial_year  (String(10))               # "2025-26"
- proof_url       (String(500), nullable=True)
- notes           (Text, nullable=True)
- created_at      (DateTime)
- updated_at      (DateTime)

Table: tax_summaries (computed / cached)
- id              (Integer, PK)
- user_id         (Integer, FK -> users.id, indexed)
- financial_year  (String(10), indexed)
- total_income    (Numeric(14, 2))
- total_deductions (Numeric(14, 2))
- taxable_income  (Numeric(14, 2))
- estimated_tax   (Numeric(14, 2))
- section_breakdown (JSON)              # {80C: {limit: 150000, used: 95000, items: [...]}, ...}
- generated_at    (DateTime)
```

### Step 8.2 - Tax Schemas

**File:** `app/schemas/tax.py`

```python
class TaxSection(str, Enum):
    SEC_80C = "80C"          # limit: 1,50,000
    SEC_80D = "80D"          # limit: 25,000 (self) + 25,000 (parents)
    SEC_80E = "80E"          # no limit (education loan interest)
    SEC_24B = "24b"          # limit: 2,00,000 (home loan interest)
    HRA = "hra"

class DeductionCreate(BaseModel):
    section: TaxSection
    name: str
    amount: Decimal
    financial_year: str                 # "2025-26"
    notes: str | None = None

class TaxSummaryResponse(BaseModel):
    financial_year: str
    total_income: Decimal
    sections: list[SectionSummary]
    total_deductions: Decimal
    taxable_income: Decimal
    estimated_tax_old_regime: Decimal
    estimated_tax_new_regime: Decimal
    recommended_regime: str
    savings_opportunity: Decimal        # remaining 80C limit, etc.
    tips: list[str]

class SectionSummary(BaseModel):
    section: str
    limit: Decimal
    utilized: Decimal
    remaining: Decimal
    percentage_used: float
    items: list[dict]
```

### Step 8.3 - Routes

```
POST   /api/v1/tax/deductions                       -> add_deduction
GET    /api/v1/tax/deductions                       -> get_deductions (query: financial_year, section)
PUT    /api/v1/tax/deductions/{id}                  -> update_deduction
DELETE /api/v1/tax/deductions/{id}                  -> delete_deduction
GET    /api/v1/tax/summary                          -> get_tax_summary (query: financial_year)
GET    /api/v1/tax/summary/export                   -> export_tax_report (PDF for CA)
```

**Total endpoints: 6**

**Key business logic:**
- Section limits are hardcoded (80C: ₹1,50,000, 80D: ₹25,000, 24b: ₹2,00,000)
- `total_income` pulled from transactions where type = 'income' in the financial year
- Tax calculation: Apply Indian tax slab rates for both old and new regime
- `recommended_regime`: Compare old vs new regime and recommend lower tax
- `savings_opportunity`: "You have ₹55,000 remaining in 80C. Invest in ELSS to save ₹17,160 in tax"

---

## Post-MVP Phase 9: AI Features (Advanced)

### Step 9.1 - NLP Transaction Input

**File:** `services/ai_service.py`

```python
class AIService:
    async def parse_natural_language(self, user_id: int, text: str) -> TransactionCreate:
        # Use OpenAI/Claude API or local NLP model
        # Input: "Spent 450 on dinner with Raj at Barbeque Nation"
        # Output: TransactionCreate(type=expense, amount=450, category_id=1,
        #         payee_payer="Barbeque Nation", notes="with Raj")

    async def suggest_category(self, description: str) -> int:
        # Given a transaction description, suggest the most likely category
        # Uses historical data + ML model

    async def detect_anomalies(self, user_id: int) -> list[dict]:
        # Compare recent transactions against user's historical patterns
        # Flag outliers (> 2 standard deviations from mean for category)

    async def generate_insights(self, user_id: int) -> list[str]:
        # Analyze spending patterns
        # "You spend 40% more on weekends"
        # "Your food spending has increased 25% this month"

    async def predict_monthly_spending(self, user_id: int) -> dict:
        # Based on current month's trajectory + historical data
        # Predict end-of-month totals per category
```

**Route:**
```
POST   /api/v1/ai/parse                             -> parse_natural_language
GET    /api/v1/ai/insights                          -> get_ai_insights
GET    /api/v1/ai/anomalies                         -> get_anomalies
GET    /api/v1/ai/predictions                       -> get_predictions
```

**Total endpoints: 4**

**Dependencies:**
- `openai` or `anthropic` SDK for LLM-based NLP
- `scikit-learn` or `numpy` for anomaly detection (z-score, IQR method)
- Consider running predictions as background tasks (Celery) since they may be compute-heavy

### Step 9.2 - Receipt OCR

**File:** `services/ocr_service.py`

```python
class OCRService:
    async def process_receipt(self, image_bytes: bytes) -> dict:
        # Use Google Cloud Vision, AWS Textract, or Tesseract
        # Extract: total amount, date, merchant name, line items
        # Return structured data for transaction pre-fill

    async def upload_and_process(self, user_id: int, file: UploadFile) -> dict:
        # 1. Save image to storage (S3/local)
        # 2. Run OCR
        # 3. Return parsed data + image URL
```

**Route:**
```
POST   /api/v1/ocr/receipt                          -> process_receipt (multipart/form-data)
```

**Dependencies:**
- `google-cloud-vision` or `pytesseract` or `boto3` (for AWS Textract)
- `Pillow` for image preprocessing
- File storage (S3 or local)

---

## Summary: All New Endpoints

| Phase | Feature | New Endpoints | New Tables |
|-------|---------|---------------|------------|
| Post-MVP 1 | Group Splitting | 14 | 5 |
| Post-MVP 2 | SMS Auto-Import | 7 | 3 |
| Post-MVP 3 | Financial Goals | 7 | 3 |
| Post-MVP 4 | Gamification | 6 | 5 |
| Post-MVP 5 | Subscription Manager | 7 | 1 |
| Post-MVP 6 | Net Worth Tracker | 7 | 3 |
| Post-MVP 7 | Shared/Family Budgets | 7 | 4 |
| Post-MVP 8 | Tax Helper | 6 | 2 |
| Post-MVP 9 | AI Features | 5 | 0 |
| **Total** | | **66** | **26** |

---

## File Creation Checklist (Per Phase)

Same pattern as core MVP:

```
For each new feature module:

[ ] 1. Create the Model(s)          -> app/models/<module>.py
[ ] 2. Import model in alembic env so it's detected
[ ] 3. Create the Schemas           -> app/schemas/<module>.py
[ ] 4. Create the Repository        -> app/repositories/<module>_repository.py
[ ] 5. Create the Service           -> services/<module>_service.py
[ ] 6. Create the Routes            -> api/routes/<module>.py
[ ] 7. Register router              -> app/main.py (app.include_router)
[ ] 8. Generate migration           -> alembic revision --autogenerate -m "message"
[ ] 9. Run migration                -> alembic upgrade head
[ ] 10. Seed data (if needed)       -> scripts/seed_<module>.py
[ ] 11. Test via Swagger            -> http://localhost:8000/docs
```

---

## Dependencies to Add

```
# For AI features
openai>=1.0          # or anthropic SDK
scikit-learn>=1.3    # for anomaly detection / predictions

# For Receipt OCR
pytesseract>=0.3     # local OCR (free)
# OR google-cloud-vision>=3.0   # cloud OCR (paid, more accurate)
Pillow>=10.0         # image processing

# For Tax calculations
# No external deps - pure Python math

# For SMS parsing
# No external deps - regex-based
```

---

**End of Nice-to-Have Backend Roadmap**

**Build order matters:** Complete each phase before moving to the next. Phases 1-4 are the highest impact features that will differentiate FinTrac from competitors.
