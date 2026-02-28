# FinTrac - Nice-to-Have Features

**Created:** February 14, 2026
**Purpose:** Features that would differentiate FinTrac from Splitwise, PhonePe Money Tracker, and other personal finance apps
**Status:** Proposed - Pending Prioritization

---

## Priority Legend

| Priority | Meaning |
|----------|---------|
| P1 | High Impact - Build after MVP core is done |
| P2 | Medium Impact - Strong differentiator |
| P3 | Nice to Have - Polish & delight |

---

## 1. Group Expense Splitting (P1 - Splitwise Killer)

**Why:** Splitwise only does splitting, not personal tracking. FinTrac can do both.

### Features

- **Create Groups:** Roommates, Trip to Goa, Office Lunch, etc.
- **Split Methods:**
  - Equal split
  - Unequal (custom amounts per person)
  - By percentage
  - By shares (e.g., 2:1:1)
  - By items (line-item splitting)
- **Debt Simplification:** Minimize the number of transactions to settle
  - A owes B ₹500, B owes C ₹500 → A pays C ₹500 directly
- **Settlement Tracking:**
  - Mark as settled
  - UPI deep links for instant payment
  - Record partial settlements
- **Activity Feed:** Per-group timeline of expenses, settlements, and comments
- **Invite Members:** Via phone number, link, or QR code
- **Group Analytics:** Who spends most, category breakdown per group

### User Stories

- As a roommate, I can create a "Flat Expenses" group and split rent, groceries, and utilities
- As a trip organizer, I can add group expenses and see who owes whom at the end
- As a user, I can settle debts via UPI directly from the app
- As a user, I can see simplified debts so I make fewer transactions

---

## 2. SMS / Notification Auto-Import (P1 - PhonePe Killer)

**Why:** Removes the biggest friction in expense tracking - manual entry.

### Features

- **Bank SMS Parsing:**
  - Read incoming bank SMS (with user permission)
  - Parse amount, merchant, account, date from standard Indian bank formats
  - Support major banks: SBI, HDFC, ICICI, Axis, Kotak, etc.
- **UPI Notification Parsing:**
  - Detect UPI payment confirmations
  - Extract amount, merchant/payee, UPI ID
- **Auto-Categorization:**
  - Rule-based: Swiggy/Zomato → Food, Uber/Ola → Transport, Amazon → Shopping
  - ML-based: Learn from user corrections over time
- **User Confirmation Flow:**
  - Show pending transactions for review
  - User confirms, edits category, or dismisses
  - Not fully automatic - builds trust
- **Duplicate Detection:** Don't create duplicates if user also logs manually

### User Stories

- As a user, I get a notification "₹450 spent at Swiggy - categorized as Food. Confirm?"
- As a user, I can review all auto-detected transactions before they're saved
- As a user, I can teach the app that "IRCTC" means Travel, and it remembers

---

## 3. AI-Powered Smart Features (P1)

**Why:** Makes the app feel intelligent and reduces manual effort.

### 3a. Natural Language Input

- Type or speak: "Spent 450 on dinner with Raj at Barbeque Nation"
- AI extracts: amount (₹450), category (Food & Dining), payee (Barbeque Nation), notes (with Raj)
- User confirms and saves

### 3b. Receipt OCR

- Scan receipt photo → extract amount, date, merchant, line items
- Auto-fill transaction form
- Store extracted data alongside the receipt image

### 3c. Anomaly Detection

- Flag unusual spending: "₹12,000 at Electronics - 5x your monthly average"
- Detect potential fraud: Transaction at unusual time/location
- Push notification for high-value transactions

### 3d. Spending Predictions

- "At your current rate, you'll exceed your Food budget by Feb 22"
- "Based on your pattern, expect ₹3,200 in subscriptions next week"
- Monthly forecast vs actual comparison

### 3e. AI Financial Advisor

- Weekly personalized tips based on actual data
- "You spent ₹8,400 on food delivery this month. Cooking 3 meals/week could save ₹4,000"
- "Your savings rate is 12%. Aim for 20% by reducing Entertainment spending"
- Actionable, specific, not generic

---

## 4. Financial Goals & Savings Tracker (P1)

**Why:** Gives users a reason to keep tracking - purpose beyond just logging.

### Features

- **Create Goals:**
  - Name: "Vacation to Bali"
  - Target amount: ₹1,50,000
  - Target date: December 2026
  - Auto-calculate monthly savings needed
- **Goal Types:**
  - Savings goal (accumulate money)
  - Debt payoff goal (linked to debt/credit entries)
  - Emergency fund goal (3-6 months of expenses)
  - Custom goal
- **Progress Tracking:**
  - Visual progress bar / jar filling animation
  - Percentage complete
  - "On track" / "Behind" / "Ahead" status
  - Projected completion date based on current savings rate
- **Auto-Allocation Rules:**
  - "Save 20% of every freelance payment toward Vacation goal"
  - "Round up every transaction and save the difference"
  - "Save ₹100 every day automatically"
- **Goal Insights:**
  - "You've saved ₹45,000 of ₹1,50,000 (30%). At this rate, you'll reach your goal by October 2026"

### User Stories

- As a user, I can set a goal to save ₹1 lakh for an emergency fund
- As a user, I can see how much I need to save per month to hit my target
- As a user, I can link a debt payoff plan to see when I'll be debt-free

---

## 5. Subscription Manager (P2)

**Why:** Neither Splitwise nor PhonePe tracks subscriptions well.

### Features

- **Track Active Subscriptions:**
  - Name, amount, billing cycle (monthly/yearly)
  - Category, payment method
  - Next renewal date
- **Dashboard:**
  - Total monthly subscription cost
  - Total yearly cost
  - Cost trend over time
- **Smart Alerts:**
  - Renewal reminders (3 days, 1 day before)
  - Free trial expiry alerts
  - Price increase detection
- **Usage Insights:**
  - "You're paying for 3 streaming services (₹1,200/month). You only used Netflix last month"
  - "Cancel unused subscriptions to save ₹800/month"
- **Auto-Detection:** Link with SMS parsing to auto-detect recurring charges

### User Stories

- As a user, I can see all my subscriptions and their total cost in one place
- As a user, I get reminded before a free trial expires
- As a user, I can see which subscriptions I'm not using

---

## 6. Net Worth Tracker (P2)

**Why:** Elevates FinTrac from "expense tracker" to "financial management" app.

### Features

- **Assets:**
  - Bank accounts (savings, FD)
  - Investments (mutual funds, stocks, PPF)
  - Property (manual valuation)
  - Other assets (gold, crypto, etc.)
- **Liabilities:**
  - Loans (linked from debt/credit module)
  - Credit card outstanding
  - EMIs
- **Net Worth Calculation:** Total Assets - Total Liabilities
- **Trend Chart:** Net worth over months/years
- **Breakdown:** Asset allocation pie chart
- **Manual or Linked:** Users update values manually (or via API integrations later)

### User Stories

- As a user, I can see my total net worth at a glance
- As a user, I can track how my net worth changes month over month
- As a user, I can see my asset allocation breakdown

---

## 7. Gamification & Behavioral Nudges (P2)

**Why:** Makes people want to track expenses - builds habit through rewards.

### Features

- **Streaks:**
  - Daily logging streak counter
  - "15-day streak! Keep it going"
  - Streak freeze (1 miss forgiven per week)
- **Badges / Achievements:**
  - "Budget Boss" - Stayed under budget for 3 consecutive months
  - "Debt Crusher" - Settled all outstanding debts
  - "Century Club" - Logged 100 transactions
  - "Savings Star" - Hit a savings goal
  - "First Steps" - Logged first transaction
  - "Consistent" - 30-day streak
- **Financial Health Score (0-100):**
  - Savings rate (weight: 30%)
  - Budget adherence (weight: 25%)
  - Debt-to-income ratio (weight: 20%)
  - Emergency fund coverage (weight: 15%)
  - Logging consistency (weight: 10%)
  - Visual gauge with color coding
- **Savings Challenges:**
  - 52-week savings challenge (₹100, ₹200, ₹300... increasing weekly)
  - No-spend day challenges
  - Round-up savings challenge
  - Custom challenges
- **Weekly/Monthly Report Cards:**
  - Push notification with summary
  - "This week: ₹4,200 spent, ₹800 under budget, 7-day streak"
  - Shareable card for social media

### User Stories

- As a user, I feel motivated to log expenses daily to maintain my streak
- As a user, I can see my financial health score and tips to improve it
- As a user, I can take on savings challenges with friends

---

## 8. Shared / Family Budgets (P2)

**Why:** Household financial management is underserved.

### Features

- **Link Accounts:** Invite family members to shared space
- **Shared Budget:**
  - Create household budgets (rent, groceries, utilities)
  - Individual contributions visible
  - Joint spending vs personal spending views
- **Family Dashboard:**
  - Total household spending
  - Per-member breakdown
  - "Family spent ₹45,000 this month - Mom: 40%, Dad: 35%, You: 25%"
- **Permission Levels:**
  - Admin: Full control
  - Editor: Add/edit transactions
  - Viewer: View only
- **Individual Privacy:** Personal transactions stay private unless shared

### User Stories

- As a couple, we can track shared household expenses together
- As a parent, I can see my family's total monthly spending
- As a user, my personal expenses remain private from shared members

---

## 9. Tax Helper - India Specific (P2)

**Why:** Tax season is painful. Auto-generating tax data from tracked expenses is high value.

### Features

- **Tax-Deductible Tagging:**
  - Mark expenses as tax-deductible
  - Common deduction categories pre-configured
- **Section 80C Tracker:**
  - PPF, ELSS, LIC, NPS, tuition fees
  - Track against ₹1.5 lakh limit
  - Progress bar showing utilization
- **HRA Calculation:**
  - Input rent paid, salary, city
  - Auto-calculate HRA exemption
- **Other Sections:**
  - 80D (health insurance)
  - 80E (education loan interest)
  - 24(b) (home loan interest)
- **Year-End Tax Summary:**
  - Total deductible expenses by section
  - Estimated tax savings
  - "You can save ₹46,800 in taxes. Here's how."
- **Export for CA:**
  - Generate tax-ready reports
  - Form 16 compatible format

### User Stories

- As a salaried employee, I can track my 80C investments and see remaining limit
- As a freelancer, I can tag business expenses for ITR filing
- As a user, I can generate a year-end tax report for my CA

---

## 10. Smart Widgets & Quick Actions (P3)

**Why:** Reduce friction to near zero for logging expenses.

### Features

- **Home Screen Widget:**
  - Today's balance / spending
  - Quick "Add Expense" button
  - Mini budget progress bars
- **Lock Screen Widget (iOS 16+ / Android):**
  - Running daily total
  - Last transaction
- **Voice Input:**
  - "Hey Siri, log 200 rupees for coffee" (Siri Shortcuts)
  - Google Assistant integration
- **Apple Watch / Wear OS:**
  - Quick expense entry from wrist
  - Today's spending glance
- **Share Extension:**
  - Share receipt image from gallery → opens FinTrac with OCR
- **Quick Settings Tile (Android):**
  - One-tap to open expense entry

### User Stories

- As a user, I can add an expense from my home screen without opening the app
- As a user, I can log expenses via voice while driving
- As a user, I can check today's spending from my watch

---

## 11. Additional Quick Wins (P3)

### Multi-Currency with Live Rates
- Set default currency (INR)
- Log transactions in foreign currencies
- Auto-convert using live exchange rates
- Travel mode: Set temporary default currency
- Currency conversion history

### Spending Heatmap Calendar
- Calendar view where each day is color-coded by spending amount
- Green (low spend) → Yellow → Red (high spend)
- Tap day to see transactions
- Identify spending patterns visually

### Category Month-over-Month Comparison
- Auto-generated insights: "Food up 23% vs last month"
- "Transport down 15% - great job!"
- Trend arrows on each category in analytics

### Data Import from Other Apps
- Import from Splitwise (CSV)
- Import from bank statements (CSV/PDF)
- Import from Money Manager, Walnut, etc.
- Reduces switching friction for new users

### Biometric Lock
- Face ID / Touch ID / Fingerprint
- App lock on open
- Optional: Lock specific sections (debt/credit)

### Recurring Transaction Insights
- "Your subscriptions cost ₹4,500/month - 15% of your income"
- "You have 12 active recurring expenses"
- Optimization suggestions

---

## Competitive Positioning Summary

| Feature | Splitwise | PhonePe | Money Manager | YNAB | **FinTrac** |
|---------|-----------|---------|---------------|------|-------------|
| Personal expense tracking | No | Basic | Yes | Yes | **Yes** |
| Group splitting | Yes | No | No | No | **Yes** |
| SMS auto-import | No | Yes | No | No | **Yes** |
| Budgeting | No | No | Basic | Advanced | **Yes** |
| Debt management | Basic | No | No | No | **Advanced** |
| AI insights | No | No | No | No | **Yes** |
| Financial goals | No | No | No | Yes | **Yes** |
| Subscription tracking | No | No | No | No | **Yes** |
| Net worth tracking | No | No | No | No | **Yes** |
| Gamification | No | No | No | No | **Yes** |
| Tax helper (India) | No | No | No | No | **Yes** |
| Offline-first | No | No | Yes | No | **Yes** |
| Export/Reports | No | No | Basic | Yes | **Advanced** |

**FinTrac's unique value:** The only app that combines Splitwise-level splitting + PhonePe-level auto-import + YNAB-level budgeting + AI insights + gamification in a single, India-focused app.

---

## Suggested Implementation Order

| Phase | Feature | Impact | Effort |
|-------|---------|--------|--------|
| Post-MVP 1 | Group Expense Splitting | Very High | High |
| Post-MVP 2 | SMS Auto-Import | Very High | Medium |
| Post-MVP 3 | Financial Goals | High | Medium |
| Post-MVP 4 | Gamification (Streaks, Scores) | High | Low-Medium |
| Post-MVP 5 | AI Features (NLP input, predictions) | High | High |
| Post-MVP 6 | Subscription Manager | Medium | Low |
| Post-MVP 7 | Net Worth Tracker | Medium | Medium |
| Post-MVP 8 | Shared/Family Budgets | Medium | High |
| Post-MVP 9 | Tax Helper | Medium | Medium |
| Post-MVP 10 | Receipt OCR | Medium | High |
| Post-MVP 11 | Widgets & Quick Actions | Low-Medium | Medium |
| Post-MVP 12 | Multi-Currency | Low | Low |

---

**End of Nice-to-Have Features Document**
