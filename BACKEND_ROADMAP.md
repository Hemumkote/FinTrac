# FinTrac Backend - Step-by-Step Implementation Roadmap

**Created:** February 10, 2026
**Focus:** Financial Tracking (income, expenses, budgets, debt/credit)
**Current State:** User module complete (register, login, profile, settings)
**Architecture:** Routes -> Services -> Repositories -> SQLAlchemy ORM

---

## Your Codebase Patterns (Reference)

Before you start, here's a summary of the conventions already established:

| Layer | Location | Pattern |
|-------|----------|---------|
| Models | `app/models/` | SQLAlchemy `Base`, `Mapped`, `mapped_column` |
| Schemas | `app/schemas/` | Pydantic `BaseModel`, `Field`, enums as `str, Enum` |
| Repositories | `app/repositories/` | Class with `AsyncSession`, raw `select()` queries |
| Services | `services/` | Class with `AsyncSession`, creates repo internally |
| Routes | `api/routes/` | `APIRouter` with `Depends(get_async_session)` and `Depends(get_current_user)` |
| Migrations | `alembic/versions/` | Auto-generated via `alembic revision --autogenerate` |
| Auth | `app/dependencies.py` | `get_current_user` dependency extracts user from JWT |

---

## Phase 1: Categories (Foundation) - PREDEFINED ONLY

Categories are system-level predefined data. Users **cannot** create, update, or delete categories.
They can only read the predefined categories seeded into the database.

### Design Decision

Categories are **not** user-specific. They are global, predefined records shared by all users.
This simplifies the data model, prevents category sprawl, and ensures consistency across
transactions, budgets, and analytics.

### Step 1.1 - Category Model

**File:** `app/models/category.py`

System-level model with **no user_id foreign key**:

```
Table: categories
- id              (Integer, PK, indexed)
- name            (String(100), nullable=False, indexed)
- type            (String(50), nullable=False)  # 'income' or 'expense'
- color           (String(7))                    # hex color like #F97316
- icon            (String(50))                   # icon name
- parent_id       (Integer, FK -> categories.id, nullable=True)
- is_active       (Boolean, default=True)
- created_at      (DateTime, default=now)
- updated_at      (DateTime, default=now, onupdate=now)
```

**Constraints:**
- `UniqueConstraint("name", "type")` - no duplicate category names per type

### Step 1.2 - Category Schemas (Read-Only)

**File:** `app/schemas/category.py`

Only a response schema is needed (no Create/Update schemas):

```python
class CategoryType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class CategoryResponse(BaseModel):
    id: int
    name: str
    type: CategoryType
    color: str | None
    icon: str | None
    parent_id: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Step 1.3 - Category Repository (Read-Only)

**File:** `app/repositories/category_repository.py`

```python
class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_category_by_id(self, category_id: int) -> Category | None
    async def get_all_categories(self, type: str | None = None) -> list[Category]
    async def get_category_by_name_and_type(self, name: str, type: str) -> Category | None
```

### Step 1.4 - Category Service (Read-Only)

**File:** `services/category_service.py`

```python
class CategoryService:
    def __init__(self, session: AsyncSession):
        self.repository = CategoryRepository(session)

    async def get_categories(self, type: CategoryType | None = None) -> list[CategoryResponse]
    async def get_category_by_id(self, category_id: int) -> CategoryResponse
```

### Step 1.5 - Category Routes (Read-Only)

**File:** `api/routes/category.py`

```
GET    /api/v1/categories          -> get_categories   (auth required, query param: ?type=income)
GET    /api/v1/categories/{id}     -> get_category     (auth required)
```

No POST, PUT, or DELETE endpoints. Categories are managed via the seed script only.

### Step 1.6 - Seed Default Categories

**File:** `seed_categories.py`

Run once to populate the database with predefined categories:

```bash
python seed_categories.py
```

**Default Expense Categories (15):**
- Food & Dining (#F97316), Housing (#7C3AED), Transport (#0EA5E9), Shopping (#EC4899)
- Entertainment (#8B5CF6), Utilities (#06B6D4), Healthcare (#EF4444), Education (#F59E0B)
- Subscriptions (#6366F1), Groceries (#10B981), Personal Care (#A855F7)
- Insurance (#64748B), Gifts & Donations (#F43F5E), Travel (#0891B2), Other Expense (#6B7280)

**Default Income Categories (8):**
- Salary (#10B981), Freelance (#3B82F6), Investments (#6366F1), Business (#14B8A6)
- Rental Income (#8B5CF6), Gifts (#EC4899), Refunds (#F59E0B), Other Income (#6B7280)

### Step 1.7 - Register Routes & Run Migration

1. **Router already registered** in `app/main.py`

2. **Generate migration:**

   ```bash
   alembic revision --autogenerate -m "create_categories_table"
   ```

3. **Run migration:**

   ```bash
   alembic upgrade head
   ```

4. **Seed categories:**

   ```bash
   python seed_categories.py
   ```

5. **Test endpoints** via Swagger UI at `/docs`

---

## Phase 2: Financial Transactions

### Step 2.1 - Transaction Model

**File:** `app/models/transaction.py`

```
Table: transactions
- id              (Integer, PK, indexed)
- user_id         (Integer, FK -> users.id)
- type            (String(20))              # 'income', 'expense', 'debt', 'credit'
- category_id     (Integer, FK -> categories.id)
- amount          (Numeric(12, 2))          # use Numeric for money, NOT Float
- currency        (String(10), default='INR')
- date            (Date, nullable=False)
- description     (String(255), nullable=True)
- payee_payer     (String(100), nullable=True)
- payment_method  (String(50), nullable=True)   # cash, upi, credit_card, etc.
- notes           (Text, nullable=True)
- receipt_url     (String(500), nullable=True)
- is_recurring    (Boolean, default=False)
- created_at      (DateTime)
- updated_at      (DateTime)
```

**Important:** Use `Numeric(12, 2)` from `sqlalchemy` for money fields, never `Float`.

**Relationships:**
- `user` -> User
- `category` -> Category

### Step 2.2 - Transaction Schemas

**File:** `app/schemas/transaction.py`

```python
class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    DEBT = "debt"
    CREDIT = "credit"

class PaymentMethod(str, Enum):
    CASH = "cash"
    UPI = "upi"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    OTHER = "other"

class TransactionCreate(BaseModel):
    type: TransactionType
    category_id: int
    amount: Decimal               # use Decimal, validate > 0
    currency: str = "INR"
    date: date
    description: str | None = None
    payee_payer: str | None = None
    payment_method: PaymentMethod | None = None
    notes: str | None = None

class TransactionUpdate(BaseModel):
    type: TransactionType | None = None
    category_id: int | None = None
    amount: Decimal | None = None
    currency: str | None = None
    date: date | None = None
    description: str | None = None
    payee_payer: str | None = None
    payment_method: PaymentMethod | None = None
    notes: str | None = None

class TransactionResponse(BaseModel):
    id: int
    user_id: int
    type: TransactionType
    category_id: int
    category_name: str | None = None
    category_color: str | None = None
    amount: Decimal
    currency: str
    date: date
    description: str | None
    payee_payer: str | None
    payment_method: str | None
    notes: str | None
    receipt_url: str | None
    is_recurring: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TransactionFilter(BaseModel):
    type: TransactionType | None = None
    category_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    payment_method: PaymentMethod | None = None
```

### Step 2.3 - Transaction Repository

**File:** `app/repositories/transaction_repository.py`

```python
class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_transaction(self, txn: Transaction) -> Transaction
    async def get_transaction_by_id(self, txn_id: int) -> Transaction | None
    async def get_transactions_by_user(self, user_id: int, filters...) -> list[Transaction]
    async def update_transaction(self, txn: Transaction) -> Transaction
    async def delete_transaction(self, txn_id: int) -> None
    async def get_balance_summary(self, user_id: int, start_date, end_date) -> dict
```

**Key query - balance summary:**
```sql
SELECT
    SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
    SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense
FROM transactions
WHERE user_id = ? AND date BETWEEN ? AND ?
```

**Other queries:**
- `get_transactions_by_user`: Support filtering by type, category, date range, payment method. Order by `date DESC, created_at DESC`
- Use `selectinload(Transaction.category)` for eager loading category info

### Step 2.4 - Transaction Service

**File:** `services/finance_service.py`

```python
class FinanceService:
    def __init__(self, session: AsyncSession):
        self.repository = TransactionRepository(session)
        self.session = session

    async def create_transaction(self, user_id: int, data: TransactionCreate) -> dict
    async def get_transactions(self, user_id: int, filters...) -> list[dict]
    async def get_transaction(self, user_id: int, txn_id: int) -> dict
    async def update_transaction(self, user_id: int, txn_id: int, data: TransactionUpdate) -> dict
    async def delete_transaction(self, user_id: int, txn_id: int) -> None
    async def get_balance_summary(self, user_id: int, start_date, end_date) -> dict
```

**Business logic:**
- Validate `amount > 0`
- Validate category exists and is active (categories are predefined, not user-specific)
- Validate category type matches transaction type (expense category for expense transaction, etc.)
- Ownership check on update/delete (transaction belongs to the requesting user)

### Step 2.5 - Transaction Routes

**File:** `api/routes/transactions.py`

```
POST   /api/v1/finance/transactions              -> create_transaction
GET    /api/v1/finance/transactions              -> get_transactions    (query: type, category_id, start_date, end_date, payment_method)
GET    /api/v1/finance/transactions/{id}         -> get_transaction
PUT    /api/v1/finance/transactions/{id}         -> update_transaction
DELETE /api/v1/finance/transactions/{id}         -> delete_transaction
GET    /api/v1/finance/balance                   -> get_balance_summary (query: start_date, end_date)
```

### Step 2.6 - Register & Migrate

1. Register router in `app/main.py`
2. Generate and run Alembic migration
3. Test all endpoints via Swagger

---

## Phase 3: Budgets

### Step 3.1 - Budget Model

**File:** `app/models/budget.py`

```
Table: budgets
- id              (Integer, PK)
- user_id         (Integer, FK -> users.id)
- category_id     (Integer, FK -> categories.id, nullable=True)  # null = overall budget
- monthly_limit   (Numeric(12, 2))
- alert_threshold (Numeric(3, 2), default=0.75)  # percentage (0.75 = 75%)
- period          (String(20), default='monthly')  # monthly, quarterly, yearly
- is_active       (Boolean, default=True)
- created_at      (DateTime)
- updated_at      (DateTime)
```

**Relationships:**
- `user` -> User
- `category` -> Category (nullable - null means overall budget)

### Step 3.2 - Budget Schemas

**File:** `app/schemas/budget.py`

```python
class BudgetPeriod(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"

class BudgetCreate(BaseModel):
    category_id: int | None = None        # null = overall budget
    monthly_limit: Decimal                 # validate > 0
    alert_threshold: Decimal = Decimal("0.75")  # 0.0 to 1.0
    period: BudgetPeriod = BudgetPeriod.MONTHLY

class BudgetUpdate(BaseModel):
    monthly_limit: Decimal | None = None
    alert_threshold: Decimal | None = None
    period: BudgetPeriod | None = None
    is_active: bool | None = None

class BudgetResponse(BaseModel):
    id: int
    user_id: int
    category_id: int | None
    category_name: str | None        # joined from category
    category_color: str | None
    monthly_limit: Decimal
    alert_threshold: Decimal
    period: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Returned when fetching budget with live spending data
class BudgetStatusResponse(BudgetResponse):
    spent: Decimal               # actual spending in period
    remaining: Decimal           # monthly_limit - spent
    percentage: float            # spent / monthly_limit (e.g. 0.83)
    status: str                  # "under_budget", "on_track", "warning", "over_budget"
    days_remaining: int          # days left in the budget period
```

### Step 3.3 - Budget Repository, Service, Routes

Follow the exact same layer pattern:

```
Repo:     app/repositories/budget_repository.py
Service:  services/budget_service.py
Routes:   api/routes/budgets.py
```

**Endpoints:**
```
POST   /api/v1/finance/budgets          -> create_budget
GET    /api/v1/finance/budgets          -> get_budgets          (returns list with live status)
GET    /api/v1/finance/budgets/{id}     -> get_budget_with_status
PUT    /api/v1/finance/budgets/{id}     -> update_budget
DELETE /api/v1/finance/budgets/{id}     -> delete_budget
```

**Key business logic in service:**
- `get_budget_with_status`: Query actual spending for the budget period, calculate:
  - `spent` = SUM of expenses for that category in the current period
  - `remaining` = monthly_limit - spent
  - `percentage` = spent / monthly_limit
  - `status`:
    - `"under_budget"` if percentage < 0.50
    - `"on_track"` if percentage 0.50 - 0.75
    - `"warning"` if percentage 0.75 - 1.0
    - `"over_budget"` if percentage >= 1.0
  - `days_remaining` = days left in current month/quarter/year
- Prevent duplicate budgets (same user + same category + same period)

---

## Phase 4: Debt & Credit Management

### Step 4.1 - DebtCredit Model

**File:** `app/models/debt_credit.py`

```
Table: debt_credit_entries
- id                (Integer, PK)
- user_id           (Integer, FK -> users.id)
- type              (String(20))          # 'receivable' (owed to you) or 'payable' (you owe)
- principal_amount  (Numeric(12, 2))
- outstanding_amount (Numeric(12, 2))     # decreases as payments are made
- interest_rate     (Numeric(5, 2), nullable=True)
- due_date          (Date, nullable=True)
- contact_name      (String(100))
- contact_phone     (String(20), nullable=True)
- description       (String(255), nullable=True)
- status            (String(20), default='active')  # active, settled, overdue
- created_at        (DateTime)
- updated_at        (DateTime)
```

**Relationships:**
- `user` -> User
- `payments` -> list[PaymentHistory] (one-to-many, cascade delete)

### Step 4.2 - PaymentHistory Model

**File:** `app/models/payment_history.py`

```
Table: payment_history
- id              (Integer, PK)
- debt_credit_id  (Integer, FK -> debt_credit_entries.id)
- amount_paid     (Numeric(12, 2))
- payment_date    (DateTime)
- notes           (Text, nullable=True)
- created_at      (DateTime)
```

**Relationship:**
- `debt_credit` -> DebtCredit (back_populates="payments")

### Step 4.3 - DebtCredit Schemas

**File:** `app/schemas/debt_credit.py`

```python
class DebtCreditType(str, Enum):
    RECEIVABLE = "receivable"   # money owed TO you
    PAYABLE = "payable"         # money YOU owe

class DebtCreditStatus(str, Enum):
    ACTIVE = "active"
    SETTLED = "settled"
    OVERDUE = "overdue"

class DebtCreditCreate(BaseModel):
    type: DebtCreditType
    principal_amount: Decimal         # validate > 0
    interest_rate: Decimal | None = None
    due_date: date | None = None
    contact_name: str                 # min_length=1, max_length=100
    contact_phone: str | None = None
    description: str | None = None

class DebtCreditUpdate(BaseModel):
    interest_rate: Decimal | None = None
    due_date: date | None = None
    contact_name: str | None = None
    contact_phone: str | None = None
    description: str | None = None

class DebtCreditResponse(BaseModel):
    id: int
    user_id: int
    type: DebtCreditType
    principal_amount: Decimal
    outstanding_amount: Decimal
    interest_rate: Decimal | None
    due_date: date | None
    contact_name: str
    contact_phone: str | None
    description: str | None
    status: DebtCreditStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    amount_paid: Decimal              # validate > 0
    payment_date: datetime | None = None  # defaults to now
    notes: str | None = None

class PaymentResponse(BaseModel):
    id: int
    debt_credit_id: int
    amount_paid: Decimal
    payment_date: datetime
    notes: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class DebtCreditSummary(BaseModel):
    total_receivable: Decimal     # total owed TO you
    total_payable: Decimal        # total YOU owe
    net: Decimal                  # receivable - payable
    overdue_count: int
```

### Step 4.4 - Repository, Service, Routes

```
Repo:     app/repositories/debt_credit_repository.py
Service:  services/debt_credit_service.py
Routes:   api/routes/debt_credit.py
```

**Endpoints:**
```
POST   /api/v1/finance/debt-credit                   -> create_entry
GET    /api/v1/finance/debt-credit                   -> list_entries    (query: type, status)
GET    /api/v1/finance/debt-credit/{id}              -> get_entry       (include payment history)
PUT    /api/v1/finance/debt-credit/{id}              -> update_entry
POST   /api/v1/finance/debt-credit/{id}/payment      -> record_payment
GET    /api/v1/finance/debt-credit/{id}/payments      -> get_payment_history
DELETE /api/v1/finance/debt-credit/{id}              -> delete_entry
GET    /api/v1/finance/debt-credit/summary            -> get_summary
```

**Key business logic:**
- `create_entry`: Set `outstanding_amount = principal_amount` on creation
- `record_payment`:
  - Validate `amount_paid <= outstanding_amount`
  - Decrease `outstanding_amount` by `amount_paid`
  - Auto-set `status = 'settled'` when `outstanding_amount` reaches 0
  - Create a `PaymentHistory` record
- Auto-detect overdue: If `due_date < today` and `status == 'active'`, mark as `'overdue'` (can be done in service or via a scheduled check)
- `get_summary`: Aggregate totals across all active entries

---

## Phase 5: Recurring Transactions

### Step 5.1 - RecurringTransaction Model

**File:** `app/models/recurring_transaction.py`

```
Table: recurring_transactions
- id                    (Integer, PK)
- user_id               (Integer, FK -> users.id)
- transaction_template  (JSON)     # stores the transaction data as a template
- frequency             (String(20))  # daily, weekly, biweekly, monthly, yearly
- start_date            (Date)
- end_date              (Date, nullable=True)
- next_occurrence       (Date)       # precomputed next date
- occurrences_count     (Integer, default=0)
- max_occurrences       (Integer, nullable=True)
- is_active             (Boolean, default=True)
- last_generated        (DateTime, nullable=True)
- created_at            (DateTime)
- updated_at            (DateTime)
```

**Relationship:**
- `user` -> User

**Note on `transaction_template` (JSON column):**
This stores the template for generating transactions:
```json
{
    "type": "expense",
    "category_id": 5,
    "amount": 1500.00,
    "currency": "INR",
    "description": "Netflix Subscription",
    "payment_method": "credit_card"
}
```

### Step 5.2 - Recurring Schemas

**File:** `app/schemas/recurring.py`

```python
class Frequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class RecurringCreate(BaseModel):
    type: TransactionType
    category_id: int
    amount: Decimal
    currency: str = "INR"
    description: str | None = None
    payment_method: PaymentMethod | None = None
    frequency: Frequency
    start_date: date
    end_date: date | None = None
    max_occurrences: int | None = None

class RecurringUpdate(BaseModel):
    amount: Decimal | None = None
    description: str | None = None
    frequency: Frequency | None = None
    end_date: date | None = None
    max_occurrences: int | None = None
    is_active: bool | None = None

class RecurringResponse(BaseModel):
    id: int
    user_id: int
    transaction_template: dict
    frequency: str
    start_date: date
    end_date: date | None
    next_occurrence: date
    occurrences_count: int
    max_occurrences: int | None
    is_active: bool
    last_generated: datetime | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Step 5.3 - Repository, Service, Routes

```
Repo:     app/repositories/recurring_repository.py
Service:  services/recurring_service.py
Routes:   api/routes/recurring.py
```

**Endpoints:**
```
POST   /api/v1/finance/recurring              -> create_recurring
GET    /api/v1/finance/recurring              -> list_recurring
GET    /api/v1/finance/recurring/{id}         -> get_recurring
PUT    /api/v1/finance/recurring/{id}         -> update_recurring
DELETE /api/v1/finance/recurring/{id}         -> delete_recurring
POST   /api/v1/finance/recurring/generate     -> manually trigger generation
```

**Key business logic:**
- On create: Build `transaction_template` JSON from input, calculate `next_occurrence` based on `start_date` and `frequency`
- `generate` endpoint: Find all recurring where `next_occurrence <= today` and `is_active = True`:
  1. Create a real transaction from the template
  2. Increment `occurrences_count`
  3. Calculate and set next `next_occurrence`
  4. If `max_occurrences` reached or `end_date` passed, set `is_active = False`
  5. Set `last_generated = now`
- Next occurrence calculation:
  - daily: +1 day
  - weekly: +7 days
  - biweekly: +14 days
  - monthly: +1 month (use `dateutil.relativedelta`)
  - yearly: +1 year
- This can later be automated with Celery or a cron job

---

## Phase 6: Analytics & Dashboard

### Step 6.1 - Analytics Service (No new model needed)

**File:** `services/analytics_service.py`

This service queries existing tables (transactions, budgets, debt_credit) to compute analytics.

```python
class AnalyticsService:
    def __init__(self, session: AsyncSession):
        self.transaction_repo = TransactionRepository(session)
        self.budget_repo = BudgetRepository(session)
        self.debt_credit_repo = DebtCreditRepository(session)
        self.session = session

    # Dashboard
    async def get_dashboard_summary(self, user_id: int, date: date) -> dict
        # Returns: balance, income/expense for today & this month, recent transactions

    # Spending breakdown
    async def get_expense_breakdown(self, user_id: int, start_date, end_date) -> dict
        # Returns: spending per category (pie chart data), top categories

    # Income breakdown
    async def get_income_breakdown(self, user_id: int, start_date, end_date) -> dict
        # Returns: income per category (pie chart data)

    # Trends over time
    async def get_finance_trends(self, user_id: int, period: str) -> dict
        # Returns: daily/weekly/monthly income & expense (bar chart data)

    # Budget overview
    async def get_budget_overview(self, user_id: int) -> dict
        # Returns: all budgets with current status (for budget screen)
```

### Step 6.2 - Analytics Schemas

**File:** `app/schemas/analytics.py`

```python
class DashboardSummary(BaseModel):
    # Today's summary
    today_income: Decimal
    today_expense: Decimal

    # This month's summary
    month_income: Decimal
    month_expense: Decimal
    month_net: Decimal

    # Overall balance
    total_balance: Decimal

    # Debt overview
    total_receivable: Decimal
    total_payable: Decimal

    # Recent transactions (last 5)
    recent_transactions: list[dict]

    # Budget alerts (budgets at warning or over)
    budget_alerts: list[dict]

class ExpenseBreakdown(BaseModel):
    total_expense: Decimal
    categories: list[dict]  # [{name, color, amount, percentage}]
    top_category: str | None
    comparison_percentage: float | None  # vs previous period

class IncomeBreakdown(BaseModel):
    total_income: Decimal
    categories: list[dict]  # [{name, color, amount, percentage}]
    top_category: str | None

class FinanceTrend(BaseModel):
    period: str  # "daily", "weekly", "monthly"
    data_points: list[dict]  # [{label: "Mon", income: 5000, expense: 3200}, ...]
    total_income: Decimal
    total_expense: Decimal
    net: Decimal
```

### Step 6.3 - Analytics Routes

**File:** `api/routes/analytics.py`

```
GET /api/v1/analytics/dashboard                -> get_dashboard          (auth required)
GET /api/v1/analytics/expense-breakdown        -> get_expense_breakdown  (query: start_date, end_date)
GET /api/v1/analytics/income-breakdown         -> get_income_breakdown   (query: start_date, end_date)
GET /api/v1/analytics/trends                   -> get_finance_trends     (query: period=daily|weekly|monthly, start_date, end_date)
GET /api/v1/analytics/budget-overview          -> get_budget_overview    (auth required)
```

**Key SQL queries for analytics:**

Expense by category:
```sql
SELECT c.name, c.color, SUM(t.amount) as total, COUNT(t.id) as count
FROM transactions t
JOIN categories c ON t.category_id = c.id
WHERE t.user_id = ? AND t.type = 'expense' AND t.date BETWEEN ? AND ?
GROUP BY c.id, c.name, c.color
ORDER BY total DESC
```

Daily trend:
```sql
SELECT t.date, t.type, SUM(t.amount) as total
FROM transactions t
WHERE t.user_id = ? AND t.date BETWEEN ? AND ?
GROUP BY t.date, t.type
ORDER BY t.date
```

---

## Phase 7: Export & Reporting

### Step 7.1 - Export Service

**File:** `services/export_service.py`

```python
class ExportService:
    def __init__(self, session: AsyncSession):
        self.transaction_repo = TransactionRepository(session)
        self.session = session

    async def export_transactions_csv(self, user_id, start_date, end_date, type) -> bytes
    async def export_transactions_excel(self, user_id, start_date, end_date, type) -> bytes
    async def generate_pdf_report(self, user_id, start_date, end_date) -> bytes
```

**Dependencies to install:**
- `reportlab` for PDF generation
- `openpyxl` for Excel
- Built-in `csv` module for CSV

### Step 7.2 - Export Schemas

**File:** `app/schemas/export.py`

```python
class ExportFormat(str, Enum):
    CSV = "csv"
    EXCEL = "excel"
    PDF = "pdf"

class ExportRequest(BaseModel):
    start_date: date
    end_date: date
    format: ExportFormat
    type: TransactionType | None = None  # filter by type, or all
    include_summary: bool = True
```

### Step 7.3 - Export Routes

**File:** `api/routes/export.py`

```
POST /api/v1/export/transactions    -> export_transactions   (body: ExportRequest)
POST /api/v1/export/report          -> generate_full_report  (body: date range, options)
```

**Response:** Return file using `StreamingResponse` from FastAPI:
```python
from fastapi.responses import StreamingResponse
import io

return StreamingResponse(
    io.BytesIO(csv_bytes),
    media_type="text/csv",
    headers={"Content-Disposition": "attachment; filename=transactions.csv"}
)
```

---

## Phase 8: Polish & Production Readiness

### Step 8.1 - Pagination

Add pagination support to all list endpoints. Create a shared utility:

**File:** `app/schemas/common.py` (extend existing)

```python
class PaginationParams(BaseModel):
    page: int = 1           # 1-indexed
    page_size: int = 20     # default 20, max 100

class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
    total_pages: int
```

Apply to: `GET /categories`, `GET /transactions`, `GET /budgets`, `GET /debt-credit`, etc.

### Step 8.2 - Error Handling Middleware

**File:** `app/middleware/error_handler.py`

Create a global exception handler that catches all unhandled exceptions and returns consistent error responses:

```python
class ErrorResponse(BaseModel):
    detail: str
    status_code: int
    error_type: str  # "validation_error", "not_found", "unauthorized", etc.
```

Register in `app/main.py` with `@app.exception_handler()`.

### Step 8.3 - Rate Limiting

Install `slowapi` and add rate limiting to sensitive endpoints:

```python
# Example: 5 login attempts per minute
@router.post("/login")
@limiter.limit("5/minute")
async def login_user(...):
```

### Step 8.4 - Redis Caching

Use Redis for caching expensive queries:
- Analytics dashboard (TTL: 5 minutes)
- Category lists (TTL: 6 hours)
- Budget status (TTL: 10 minutes)
- Balance summary (TTL: 5 minutes)

**File:** `core/cache.py`

### Step 8.5 - Structured Logging

Replace `print()` statements with proper logging:

```python
import logging
logger = logging.getLogger(__name__)

logger.info("Transaction created", extra={"user_id": user.id, "amount": amount, "type": type})
```

---

## Quick Reference: File Creation Order

Here's a checklist you can follow for each phase:

```
For each new feature module:

[ ] 1. Create the Model         -> app/models/<module>.py
[ ] 2. Import model in alembic env or base so it's detected
[ ] 3. Create the Schemas       -> app/schemas/<module>.py
[ ] 4. Create the Repository    -> app/repositories/<module>_repository.py
[ ] 5. Create the Service       -> services/<module>_service.py
[ ] 6. Create the Routes        -> api/routes/<module>.py
[ ] 7. Register router          -> app/main.py (app.include_router)
[ ] 8. Generate migration       -> alembic revision --autogenerate -m "message"
[ ] 9. Run migration            -> alembic upgrade head
[ ] 10. Test via Swagger        -> http://localhost:8000/docs
```

---

## Summary Timeline

| Phase | Module | Depends On | Endpoints |
|-------|--------|------------|-----------|
| 1 | Categories (predefined, read-only) | Seed script | 2 |
| 2 | Transactions | Categories | 6 |
| 3 | Budgets | Transactions + Categories | 5 |
| 4 | Debt & Credit | Users | 8 |
| 5 | Recurring Transactions | Transactions | 6 |
| 6 | Analytics & Dashboard | Transactions + Budgets + Debt | 5 |
| 7 | Export & Reporting | Transactions + Analytics | 2 |
| 8 | Polish | All | - |

**Total new endpoints: ~34**

---

Good luck building! Work through each phase sequentially - each one builds on the last.
