# Product Requirements Document (PRD)

## Daily Tracker - Work & Finance Management App

---

## 1. Executive Summary

**Product Name:** Daily Tracker

**Version:** 1.0  
**Document Date:** January 22, 2026  
**Status:** Draft - Pending Review

**Vision:** A comprehensive React Native mobile application that empowers users to gain control over their time and money through intuitive tracking of daily activities and financial transactions.

**Target Users:**

- Freelancers and gig workers
- Students managing time and budgets
- Professionals seeking work-life balance
- Anyone wanting to build better productivity and financial habits

**Core Value Proposition:** Unlike separate time-tracking and expense apps, Daily Tracker provides a unified view of how users spend their time AND money, enabling insights into productivity patterns and financial health from a single interface.

---

## 2. Product Overview

### 2.1 Problem Statement

Users struggle to:

- Understand where their time actually goes each day
- Track financial transactions consistently
- Connect productivity patterns with financial outcomes
- Manage multiple tracking apps with inconsistent data
- Export and analyze their personal data effectively

### 2.2 Solution

A unified mobile app that:

- Simplifies time tracking with smart categorization
- Streamlines financial transaction logging
- Provides actionable insights through data visualization
- Works offline-first for reliability
- Exports data for external analysis
- Offers a single source of truth for personal productivity and finance data

### 2.3 Key Differentiators

- **Unified Experience:** Time + Finance in one app
- **Offline-First:** Works without internet connection
- **Privacy-Focused:** Data stored locally by default
- **Flexible Export:** Multiple format options for data portability
- **Customizable:** User-defined categories and workflows

---

## 3. User Roles & Personas

### Primary User Role: Individual User

**Persona 1: Alex - The Freelance Developer**

- **Age:** 28
- **Location:** Urban area
- **Tech Savviness:** High
- **Needs:** Track billable hours, manage project income/expenses, invoice clients
- **Pain Points:** Switching between multiple apps, forgetting to log time, unclear profitability per project
- **Goals:** Increase billable hours, reduce overhead costs, simplify tax filing
- **Quote:** _"I need to know exactly how much time I'm spending on each client to price my work correctly."_

**Persona 2: Maya - The Graduate Student**

- **Age:** 24
- **Location:** College town
- **Tech Savviness:** Medium
- **Needs:** Balance study time, part-time work, tight budget management
- **Pain Points:** Overspending on food delivery, procrastination, unclear time allocation across subjects
- **Goals:** Graduate on time, stay within monthly budget, build emergency savings
- **Quote:** _"I want to see if I'm actually studying as much as I think I am, and where my money is really going."_

**Persona 3: Rajesh - The Small Business Owner**

- **Age:** 35
- **Location:** Tier-2 city
- **Tech Savviness:** Medium
- **Needs:** Track business activities, separate personal/business finances, manage cash flow
- **Pain Points:** Tax preparation complexity, unclear which activities drive revenue, mixing personal and business expenses
- **Goals:** Optimize time on high-value activities, improve profitability, simplify accounting
- **Quote:** _"I need clear reports for my CA and insights on where I should focus my energy."_

---

## 4. Feature Specifications

### 4.1 PART 1: Work/Time Tracking

#### 4.1.1 Predefined Category System

**Feature ID:** F1.1  
**Priority:** P0 (MVP Critical)

**Description:** Default work categories for quick selection without setup friction.

**Predefined Categories:**

**Professional Work:**

- Meetings
- Deep Work / Focus Time
- Email & Admin
- Client Calls
- Planning & Strategy

**Personal Development:**

- Learning / Courses
- Reading
- Exercise
- Meditation / Mindfulness

**Household:**

- Cleaning
- Cooking
- Errands
- Childcare

**Leisure:**

- Entertainment
- Social Activities
- Hobbies
- Rest / Breaks

**Other:**

- Commute / Travel
- Miscellaneous

**User Stories:**

- As a user, I can select from predefined categories to quickly start tracking without setup
- As a user, I can see color-coded categories for easy visual identification
- As a user, I can view icons next to each category for quick recognition

**Acceptance Criteria:**

- [ ] System provides at least 15 predefined categories on first launch
- [ ] Each category has a unique color (hex code defined)
- [ ] Each category has an associated icon from react-native-vector-icons
- [ ] Categories are organized in logical groups
- [ ] User can still create custom categories (see F1.2)

---

#### 4.1.2 Custom Category Creation

**Feature ID:** F1.2  
**Priority:** P0 (MVP Critical)

**Description:** Users can create unlimited custom categories to match their unique workflows.

**Capabilities:**

- Custom category name (3-50 characters, alphanumeric + spaces)
- Custom color selection from color picker or predefined palette
- Custom icon selection from icon library (500+ icons available)
- Optional parent category assignment for hierarchical organization
- Archive/delete custom categories

**User Stories:**

- As a freelancer, I can create categories for each client project (e.g., "Client - Acme Corp")
- As a student, I can create categories for each course (e.g., "CS101 - Data Structures")
- As a user, I can organize custom categories under predefined parent categories
- As a user, I can archive categories I no longer use without losing historical data

**Acceptance Criteria:**

- [ ] User can create unlimited custom categories
- [ ] Category creation form validates name uniqueness
- [ ] Color picker provides at least 20 preset colors + custom RGB selection
- [ ] Icon library provides search and browse functionality
- [ ] Archived categories don't appear in selection but remain in historical data
- [ ] Deleted categories prompt user to reassign existing entries

**UI/UX Notes:**

- Access via Settings → Categories → "Add Custom Category"
- Real-time preview of category appearance
- Confirmation dialog before deletion

---

#### 4.1.3 Time Tracking Modes

**Feature ID:** F1.3  
**Priority:** P0 (MVP Critical)

**Description:** Multiple modes to accommodate different tracking preferences and use cases.

##### Mode 1: Manual Entry

**Use Case:** Logging activities after they've been completed

**Flow:**

1. Tap "Add Time Entry" button
2. Select category from list (with search)
3. Set start date & time using date/time picker
4. Set end date & time using date/time picker
5. System calculates duration automatically
6. Add optional notes (max 500 characters)
7. Save entry

**Validation:**

- End time must be after start time
- Cannot exceed 24 hours in single entry
- Warn if entry overlaps with existing entry

##### Mode 2: Timer Mode (Real-time Tracking)

**Use Case:** Tracking activities as they happen

**Flow:**

1. Tap "Start Timer" FAB button
2. Select category from quick-access list
3. Timer starts immediately, showing elapsed time
4. App shows persistent notification with running timer
5. User can:
   - Pause (timer stops but entry remains active)
   - Resume (timer continues from paused time)
   - Stop (end timer and prepare to save)
6. On stop, user can add notes
7. Save entry with auto-calculated duration

**Features:**

- Background timer continues even if app is closed
- Lock screen notification shows elapsed time
- Quick action from notification to stop timer
- Multiple timers NOT supported (must stop current before starting new)

##### Mode 3: Quick Log

**Use Case:** Rapidly logging routine activities with standard durations

**Flow:**

1. Tap "Quick Log" button
2. Select category
3. Select duration from preset buttons: 15m, 30m, 1h, 2h, 4h
4. Entry auto-created with current timestamp and selected duration
5. Optional: Add notes after creation

**Configuration:**

- User can customize preset duration buttons in Settings
- Maximum 6 preset buttons

**User Stories:**

- As a user, I can start a timer when I begin a task and let it run in the background
- As a user, I can manually log past activities I forgot to track
- As a user, I can quickly log routine activities with preset durations
- As a user, I can see a running timer notification even when the app is closed

**Acceptance Criteria:**

- [ ] All three modes are accessible from Dashboard
- [ ] Timer runs accurately in background
- [ ] Manual entry prevents invalid time ranges
- [ ] Quick log creates entries instantly (< 500ms)
- [ ] User can switch default mode in Settings

---

#### 4.1.4 Time Entry Management

**Feature ID:** F1.4  
**Priority:** P0 (MVP Critical)

**Description:** View, edit, search, and manage all time tracking entries.

**Capabilities:**

**View Entries:**

- Daily timeline view (vertical list grouped by date)
- Weekly calendar view with time blocks
- Monthly summary view
- List view with filters

**Edit Entries:**

- Tap any entry to open edit modal
- Modify category, start/end time, notes
- See edit history (who/when modified)
- Validation same as creation

**Delete Entries:**

- Swipe-to-delete gesture
- Confirmation dialog before deletion
- Undo option (5-second toast)
- Bulk delete by date range or category

**Duplicate Entries:**

- Long-press entry to show context menu
- "Duplicate" creates new entry with same category/duration
- User adjusts time before saving

**Search Entries:**

- Search bar at top of Time Tracking tab
- Search by: category name, notes content, date range
- Auto-complete suggestions
- Filter results by category, date range

**User Stories:**

- As a user, I can view all my time entries in a clean timeline
- As a user, I can edit mistakes in past entries
- As a user, I can search for entries from last month for a specific project
- As a user, I can duplicate yesterday's 2-hour coding session for today

**Acceptance Criteria:**

- [ ] Timeline shows entries grouped by date, sorted newest first
- [ ] Edit/delete actions require confirmation
- [ ] Search returns results in < 1 second for 1000 entries
- [ ] Undo delete works for 5 seconds after deletion
- [ ] Duplicate preserves category, notes, duration but sets current timestamp

---

#### 4.1.5 Time Data Export

**Feature ID:** F1.5  
**Priority:** P1 (Important)

**Description:** Export time tracking data in multiple formats for external analysis, billing, or archival.

**Export Formats:**

**1. CSV (Comma-Separated Values)**

- Columns: Date, Start Time, End Time, Duration, Category, Subcategory, Notes
- Compatible with Excel, Google Sheets, billing software
- UTF-8 encoding with BOM for special characters

**2. PDF (Formatted Report)**

- Professional layout with logo/branding area
- Summary statistics at top
- Detailed entry table
- Category breakdown chart
- Page numbers and generation date

**3. JSON (Raw Data)**

- Complete data structure including metadata
- ISO 8601 date/time format
- Useful for developers/advanced users
- Includes category IDs and color codes

**Export Options:**

- Date range selection (This Week, This Month, Last Month, Custom Range)
- Category filtering (All, Selected Categories)
- Include/exclude notes checkbox
- Include summary statistics checkbox
- Group by day/week/month/category

**Delivery Methods:**

- Share via system share sheet (Email, WhatsApp, Slack, etc.)
- Save to device storage (Documents folder)
- Auto-upload to Google Drive (if connected)
- Auto-upload to iCloud Drive (iOS only)

**User Stories:**

- As a freelancer, I can export my billable hours as CSV to import into my invoicing software
- As a user, I can generate a PDF report for the past month to review my productivity
- As a developer, I can export JSON to build custom analytics scripts

**Acceptance Criteria:**

- [ ] All export formats generate correctly with sample data
- [ ] CSV opens properly in Excel/Sheets without encoding issues
- [ ] PDF is professional quality, under 5MB for 1 month of data
- [ ] JSON validates against schema
- [ ] Export completes in < 5 seconds for 1 year of data
- [ ] User can preview before sharing/saving

---

#### 4.1.6 Time Analytics & Insights

**Feature ID:** F1.6  
**Priority:** P1 (Important)

**Description:** Visual analytics and insights to help users understand their time allocation patterns.

**Dashboard Widgets:**

**1. Time Period Selector**

- Today, This Week, This Month, Last Month, Custom Range
- Quick navigation between periods

**2. Total Time Tracked**

- Large number display (e.g., "42.5 hours")
- Comparison to previous period (↑ 12% vs last week)

**3. Category Breakdown - Pie Chart**

- Visual representation of time distribution
- Top 5 categories shown, rest grouped as "Other"
- Tap slice to drill down
- Percentage and hours shown per category

**4. Daily/Weekly Trend - Line Graph**

- X-axis: Days or weeks
- Y-axis: Hours tracked
- Identify patterns (productive days, low-activity days)
- Optional: Overlay multiple categories

**5. Productivity Score**

- Algorithm: (Work categories time / Total time) × 100
- User can define which categories count as "productive"
- Visual gauge (0-100%)
- Trend indicator (improving/declining)

**6. Statistics Cards**

- Longest single session (category, duration, date)
- Shortest session
- Most tracked category
- Least tracked category
- Average daily tracking
- Streak (consecutive days with entries)

**7. Goal Tracking**

- Set target hours per category (e.g., "Exercise: 5h/week")
- Progress bar showing actual vs target
- Red/yellow/green status indicators
- Weekly/monthly goal periods

**Insights (Auto-generated):**

- "You spent 35% more time in Meetings this week compared to last week"
- "Your most productive day was Tuesday with 8.5 hours tracked"
- "You're on track to meet your Exercise goal this week"

**User Stories:**

- As a user, I can see how I spent my time this week at a glance
- As a user, I can identify which activities consume most of my time
- As a user, I can set goals for specific categories and track progress
- As a user, I can compare this month's time allocation to last month

**Acceptance Criteria:**

- [ ] Charts render smoothly with up to 1000 data points
- [ ] Pie chart shows accurate percentages summing to 100%
- [ ] Goal progress updates in real-time as entries are added
- [ ] All analytics recalculate when date range changes
- [ ] Insights update daily at midnight
- [ ] Analytics work offline with cached data

---

### 4.2 PART 2: Financial Tracking

#### 4.2.1 Transaction Types

**Feature ID:** F2.1  
**Priority:** P0 (MVP Critical)

**Description:** Four fundamental transaction types to cover all financial activities.

**Transaction Types:**

**1. Income** 💰

- Definition: Money received/earned
- Examples: Salary, freelance payment, gift received
- Impact: Increases net balance
- Color: Green (#10B981)

**2. Expense** 💸

- Definition: Money spent/paid
- Examples: Groceries, rent, subscription
- Impact: Decreases net balance
- Color: Red (#EF4444)

**3. Debt (Receivable)** 📥

- Definition: Money others owe to you
- Examples: Loan given to friend, invoice not yet paid
- Impact: Tracked separately, doesn't affect current balance
- Color: Blue (#3B82F6)

**4. Credit/Loan (Payable)** 📤

- Definition: Money you owe to others
- Examples: Credit card balance, personal loan, mortgage
- Impact: Tracked separately, liability
- Color: Orange (#F97316)

**User Stories:**

- As a user, I can record my monthly salary as Income
- As a user, I can track money I lent to a friend as Debt
- As a user, I can monitor my credit card balance as Credit
- As a user, I can see my net worth considering all transaction types

**Acceptance Criteria:**

- [ ] All four types available in transaction creation screen
- [ ] Type selection is prominent and clear
- [ ] Balance calculations respect type logic
- [ ] Each type has distinct visual styling

---

#### 4.2.2 Predefined Financial Categories

**Feature ID:** F2.2  
**Priority:** P0 (MVP Critical)

**Description:** Comprehensive predefined categories covering common financial transactions.

**Income Categories:**

- 💼 Salary/Wages
- 💻 Freelance/Contract Work
- 📈 Investment Returns (Dividends, Interest, Capital Gains)
- 🏠 Rental Income
- 🎁 Gifts Received
- 💵 Refunds
- 🔄 Reimbursements
- 📦 Product Sales
- 🎯 Bonus/Commission
- 🌟 Other Income

**Expense Categories:**

_Housing:_

- 🏡 Rent/Mortgage
- ⚡ Utilities (Electric, Water, Gas)
- 🔧 Home Maintenance
- 🪴 Home Improvement
- 🏘️ Property Tax

_Food & Dining:_

- 🛒 Groceries
- 🍽️ Restaurants
- ☕ Café/Coffee Shop
- 🚚 Food Delivery
- 🍺 Bars/Nightlife

_Transportation:_

- ⛽ Fuel/Petrol
- 🚇 Public Transit
- 🚗 Vehicle Maintenance
- 🅿️ Parking
- 🚕 Taxi/Rideshare
- ✈️ Travel/Flights

_Healthcare:_

- 🏥 Medical (Doctor visits, procedures)
- 🦷 Dental
- 💊 Medications/Pharmacy
- 🏥 Health Insurance
- 👓 Vision/Optical

_Shopping:_

- 👕 Clothing/Apparel
- 👠 Footwear
- 💻 Electronics
- 📚 Books
- 🎮 Gadgets
- 🛍️ Personal Items

_Entertainment:_

- 🎬 Movies/Theatre
- 📺 Streaming Subscriptions
- 🎮 Gaming
- 🎪 Events/Concerts
- 🏋️ Sports/Recreation
- 🎨 Hobbies

_Education:_

- 📖 Tuition/Fees
- 📚 Books/Supplies
- 💻 Online Courses
- 🎓 Certifications

_Subscriptions & Bills:_

- 📱 Phone/Mobile
- 🌐 Internet
- 🔌 Utilities
- 📺 Streaming Services (Netflix, Spotify, etc.)
- 💾 Software/SaaS
- 🏋️ Gym Membership
- 📰 News/Magazines

_Personal Care:_

- 💇 Salon/Barber
- 💅 Beauty/Cosmetics
- 🧴 Personal Hygiene
- 🏋️ Fitness/Wellness

_Gifts & Donations:_

- 🎁 Gifts Given
- ❤️ Charity/Donations
- 🙏 Religious Contributions

_Financial:_

- 🏦 Bank Fees
- 💳 Credit Card Fees
- 📊 Investment Fees
- 💸 Loan Interest

_Other:_

- 📦 Miscellaneous
- 🐾 Pet Care
- 🧒 Childcare
- ⚖️ Legal Fees
- 🔧 Repairs (non-home)

**Debt (Receivable) Categories:**

- 👤 Personal Loans Given
- 💼 Business Receivables
- 📋 Pending Invoices
- 🤝 Other Debts Owed to You

**Credit/Loan (Payable) Categories:**

- 💳 Credit Card
- 🏦 Personal Loan
- 💼 Business Payable
- 🏠 Mortgage/Home Loan
- 🚗 Auto Loan/EMI
- 🎓 Student Loan
- 👥 Family/Friends Loan
- 🔧 Other Debts You Owe

**User Stories:**

- As a user, I can quickly categorize transactions without thinking too hard
- As a user, I have granular subcategories for major expense areas like Food and Housing
- As a user, I can see what percentage of income goes to each major category

**Acceptance Criteria:**

- [ ] System provides 60+ predefined categories across all types
- [ ] Categories are logically grouped by theme
- [ ] Each category has appropriate icon and color
- [ ] Categories cover 90% of common transactions without customization
- [ ] Hierarchy supports parent categories with subcategories

---

#### 4.2.3 Transaction Entry

**Feature ID:** F2.3  
**Priority:** P0 (MVP Critical)

**Description:** Comprehensive transaction entry form with required and optional fields.

**Entry Flow:**

1. **Select Transaction Type** (Required)
   - Income / Expense / Debt / Credit
   - Large button selection with icons
   - Changes form fields based on type

2. **Enter Amount** (Required)
   - Numeric keypad input
   - Currency symbol auto-displayed (based on Settings)
   - Supports 2 decimal places
   - Validation: > 0, < 1,000,000,000

3. **Select Category** (Required)
   - Searchable dropdown
   - Recent categories shown first
   - Grouped by parent category
   - Create custom category inline

4. **Select Date** (Required, defaults to Today)
   - Date picker (calendar view)
   - Quick options: Today, Yesterday, Custom
   - Cannot select future dates

5. **Optional Fields:**

   **Payee/Payer Name:**
   - Text input, 50 character max
   - Autocomplete from previous entries
   - Examples: "Amazon", "John Doe", "Acme Corp"

   **Payment Method:**
   - Dropdown: Cash, Debit Card, Credit Card, UPI, Bank Transfer, Check, Other
   - Stored for reporting

   **Notes:**
   - Multi-line text area
   - 500 character max
   - Placeholder: "Add notes (optional)"

   **Receipt Attachment:**
   - Camera button to take photo
   - Gallery button to select existing image
   - Preview thumbnail shown
   - Compressed to < 2MB

   **Tags:**
   - Multi-select chips
   - Examples: "Tax Deductible", "Business", "Client: Acme"
   - Create new tags inline

   **Location:**
   - Auto-detect using GPS (with permission)
   - Manual text entry
   - Stored for expense reports

6. **Save Transaction**
   - Validation check
   - Success toast message
   - Return to transaction list or Dashboard

**Special Fields for Debt/Credit:**

- Due Date (optional)
- Interest Rate (optional, percentage)
- Installment Amount (for recurring payments)
- Contact (link to phone contact)

**User Stories:**

- As a user, I can log an expense in under 10 seconds with just amount and category
- As a user, I can attach a receipt photo for record-keeping
- As a user, I can tag transactions for tax purposes
- As a user, I can set a due date when recording a debt

**Acceptance Criteria:**

- [ ] Form validates all required fields before save
- [ ] Amount input prevents invalid characters
- [ ] Category search shows results as user types
- [ ] Photo attachments are compressed and stored locally
- [ ] Form remembers last-used payment method per category
- [ ] Save completes in < 500ms
- [ ] Keyboard dismisses appropriately between fields

---

#### 4.2.4 Custom Financial Categories

**Feature ID:** F2.4  
**Priority:** P0 (MVP Critical)

**Description:** Create custom categories within each transaction type.

**Capabilities:**

- Create categories within Income, Expense, Debt, or Credit types
- Assign custom name (3-50 characters)
- Choose icon from library (500+ options)
- Select color from palette or custom picker
- Set optional monthly budget limit (Expense categories only)
- Assign to parent category (optional)

**Budget Limit Feature:**

- Only available for Expense categories
- Set monthly spending limit (e.g., "Dining Out: ₹5000/month")
- Visual warning at 75% spent
- Alert at 100% spent
- Option to allow overspending or block entry

**User Stories:**

- As a freelancer, I can create "Client: Acme Corp" income category
- As a user, I can create "Coffee Shop" expense category with ₹2000/month limit
- As a user, I can organize custom categories under predefined parents

**Acceptance Criteria:**

- [ ] User can create unlimited custom categories
- [ ] Budget limit validation (> 0 if set)
- [ ] Budget warning triggers at correct percentage
- [ ] Custom categories persist across app restarts
- [ ] Deleted categories prompt reassignment of historical transactions

---

#### 4.2.5 Recurring Transactions

**Feature ID:** F2.5  
**Priority:** P1 (Important)

**Description:** Automate entry of recurring income and expenses.

**Setup Flow:**

1. Create transaction as normal
2. Toggle "Make Recurring" switch
3. Select frequency: Daily, Weekly, Bi-weekly, Monthly, Yearly
4. Set start date
5. Optional: Set end date or number of occurrences
6. Save recurring template

**Frequency Options:**

- **Daily:** Every day
- **Weekly:** Every week on same day (e.g., every Monday)
- **Bi-weekly:** Every 2 weeks
- **Monthly:** Same date each month (e.g., 1st of month)
- **Yearly:** Same date each year

**Automation:**

- System checks daily for due recurring transactions
- Auto-creates transactions at midnight (local time)
- Notification sent when transaction created
- User can edit/delete individual occurrences
- User can skip specific occurrence

**Management:**

- View all recurring templates in separate tab
- Edit template (affects future occurrences only)
- Pause template (stop creating without deleting)
- Delete template (with option to delete past occurrences)

**User Stories:**

- As a salaried user, I can set my monthly salary as recurring income
- As a user, I can set my rent as monthly recurring expense
- As a user, I can skip my gym membership payment for one month when traveling
- As a user, I can see all my recurring transactions in one place

**Acceptance Criteria:**

- [ ] Recurring transactions generate accurately on schedule
- [ ] User receives notification for auto-created transactions
- [ ] Editing template doesn't affect past occurrences
- [ ] Skipped occurrences don't appear in transaction list
- [ ] Paused templates can be resumed
- [ ] Maximum 100 active recurring templates per user

---

#### 4.2.6 Debt & Credit Management

**Feature ID:** F2.6  
**Priority:** P1 (Important)

**Description:** Advanced tracking and management of money owed to/by user.

**Debt (Receivable) Features:**

**Initial Entry:**

- Record principal amount
- Set due date
- Add debtor name (with contact link)
- Optional interest rate
- Notes

**Partial Payment Recording:**

- Record payment received
- Update outstanding balance automatically
- Track payment history
- Send reminder to debtor (SMS/WhatsApp integration)

**Settlement:**

- Mark as "Paid in Full"
- Record settlement date
- Option to record if settled for less than full amount
- Archive debt

**Debt Dashboard:**

- Total outstanding debt
- List of active debts sorted by due date
- Overdue debts highlighted in red
- Next due debt prominently shown

**Credit/Loan (Payable) Features:**

**Initial Entry:**

- Record principal amount
- Set due date
- Add creditor name (with contact link)
- Interest rate (simple or compound)
- EMI amount (if applicable)
- Notes

**Payment Recording:**

- Record payment made
- Splits payment into principal + interest
- Updates remaining balance
- Tracks payment history

**EMI Calculator:**

- Calculate EMI based on principal, rate, tenure
- Amortization schedule display
- Shows total interest payable

**Reminders:**

- Due date notifications (1 week, 1 day before)
- Overdue alerts
- EMI payment reminders

**Credit Dashboard:**

- Total outstanding credit/loans
- List sorted by due date
- Overdue amounts highlighted
- Credit utilization if credit card
- Next payment due prominently shown

**Contact Integration:**

- Link debt/credit to phone contact
- Quick call/message from app
- Sync contact details

**User Stories:**

- As a user, I can track money I lent to my friend and record partial payments
- As a user, I can see all my credit card balances in one place
- As a user, I get reminded before my loan EMI is due
- As a user, I can calculate how much interest I'll pay on my loan

**Acceptance Criteria:**

- [ ] Interest calculations are accurate for simple and compound
- [ ] Partial payment correctly updates balance
- [ ] Reminders trigger at correct times
- [ ] Settlement marks debt/credit as complete
- [ ] Contact integration works on both iOS and Android
- [ ] Overdue items show in Dashboard with visual indicator

---

#### 4.2.7 Financial Analytics & Reports

**Feature ID:** F2.7  
**Priority:** P1 (Important)

**Description:** Comprehensive analytics and reporting for financial insights.

**Dashboard Overview:**

**1. Current Balance**

- Formula: Total Income - Total Expenses
- Prominent display at top
- Color-coded (green if positive, red if negative)
- Comparison to last period

**2. Monthly Cash Flow**

- Side-by-side Income vs Expense bars
- Net cash flow calculated
- Trend line over past 6 months

**3. Outstanding Balances**

- Total Debt (receivable)
- Total Credit (payable)
- Net position (Debt - Credit)

**4. Quick Stats Cards**

- Largest expense this month
- Top spending category
- Savings rate (%)
- Days until next paycheck

**Detailed Reports:**

**Income vs Expense Trends**

- Line graph over time
- Selectable period: Week, Month, Quarter, Year
- Multiple series (Income, Expense, Net)
- Identify surplus/deficit months

**Category-wise Spending Breakdown**

- Pie chart showing expense distribution
- Top 10 categories listed with amounts
- Drill-down to subcategories
- Compare periods (This Month vs Last Month)

**Budget vs Actual Comparison**

- Only for categories with budgets set
- Progress bars showing spent / budgeted
- Red/yellow/green indicators
- Projected overspending based on current rate

**Debt/Credit Aging Report**

- Table showing all outstanding amounts
- Columns: Creditor/Debtor, Principal, Interest, Due Date, Days Outstanding
- Sort by amount, due date, or age
- Filter by overdue only

**Custom Date Range Analysis**

- User selects any start and end date
- Summary statistics for period
- Category breakdown
- Comparison to previous equal period

**Export Options:**

- Same as Time Tracking exports (CSV, PDF, JSON)
- Tax-ready format (income, expenses by deductible categories)
- Bank statement format

**User Stories:**

- As a user, I can see my spending trends over the past 6 months
- As a user, I can identify which category I overspend in
- As a user, I can track if I'm staying within my budgets
- As a user, I can export a year-end summary for tax filing

**Acceptance Criteria:**

- [ ] All charts render correctly with real data
- [ ] Calculations are accurate (verified with sample data)
- [ ] Reports generate in < 5 seconds for 1 year of data
- [ ] PDF exports are professional and printer-friendly
- [ ] Comparison periods calculate correctly (accounting for month lengths)
- [ ] Zero-state designs for users with no data

---

#### 4.2.8 Budgeting

**Feature ID:** F2.8  
**Priority:** P1 (Important)

**Description:** Set and track monthly budgets per expense category.

**Budget Creation:**

- Navigate to Budgets tab
- Select expense category
- Enter monthly limit amount
- Optionally set budget period (monthly, quarterly, yearly)
- Save budget

\*\*Budget Tracking
