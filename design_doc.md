# FinTrac - UI/UX Design Specification

## Mobile App Design Document

**Version:** 1.1
**Date:** February 10, 2026
**Design Inspiration:** Modern Finance Tracking App Aesthetics
**Platform:** React Native (iOS & Android)

---

## Table of Contents

1. [Design Philosophy](#design-philosophy)
2. [Visual Design System](#visual-design-system)
3. [Screen-by-Screen Specifications](#screen-specifications)
4. [Component Library](#component-library)
5. [Interactions & Animations](#interactions-animations)
6. [Responsive Layouts](#responsive-layouts)
7. [Accessibility](#accessibility)
8. [Design Assets](#design-assets)

---

## 1. Design Philosophy

### 1.1 Core Design Principles

**Clarity Over Complexity**

- Information hierarchy that guides the eye naturally
- Progressive disclosure of advanced features
- Clear visual feedback for all user actions

**Data-Driven Aesthetics**

- Charts and visualizations as primary design elements
- Color-coded categories for instant recognition
- Progress indicators integrated throughout

**Modern & Professional**

- Clean, contemporary interface inspired by modern finance apps
- Card-based layouts with generous white space
- Subtle shadows and depth for visual hierarchy

**Finance-Focused**

- Quick access to frequent actions via FAB (Floating Action Button)
- Minimal taps to complete core tasks
- Smart defaults to reduce decision fatigue

### 1.2 Design Inspiration Elements

Inspired by modern finance tracking applications, our design incorporates:

- **Card-Based Layout:** Information grouped in rounded cards with subtle shadows
- **Bold Typography:** Clear headers with strong visual hierarchy
- **Progress Visualization:** Circular progress indicators, budget bars, horizontal bars
- **Color Psychology:** Strategic use of color to convey income, expense, and status
- **Clean Navigation:** Bottom tab bar with clear iconography
- **Data-Rich Dashboards:** Multiple metrics visible at a glance without overwhelming

---

## 2. Visual Design System

### 2.1 Color Palette

#### Primary Colors

**Primary Blue** - `#2563EB`

- Usage: Primary actions, active states, navigation highlights
- Represents: Trust, focus, reliability
- Accessibility: WCAG AAA compliant on white

**Secondary Blue** - `#60A5FA`

- Usage: Secondary actions, hover states
- Lighter variant for backgrounds and accents

**Dark Blue** - `#1E40AF`

- Usage: Headers, important text, dark mode primary

#### Semantic Colors

**Success Green** - `#10B981`

- Usage: Income, positive balance, under-budget indicators
- Icon: ✓ checkmarks, upward arrows

**Warning Yellow/Amber** - `#F59E0B`

- Usage: Budget warnings (75% spent), upcoming due dates
- Icon: ⚠ alerts, reminders

**Danger Red** - `#EF4444`

- Usage: Expenses, overspending, overdue items
- Icon: × errors, downward trends

**Info Cyan** - `#06B6D4`

- Usage: Debt (receivable), informational messages

**Alert Orange** - `#F97316`

- Usage: Credit/loans (payable), urgent actions

#### Category Colors (Predefined Palette)

**Expense Categories:**

- Food & Dining: `#F97316` (Orange)
- Housing: `#7C3AED` (Violet)
- Transport: `#0EA5E9` (Sky)
- Shopping: `#EC4899` (Pink)
- Entertainment: `#8B5CF6` (Purple)
- Utilities: `#06B6D4` (Cyan)
- Healthcare: `#EF4444` (Red)
- Education: `#F59E0B` (Amber)
- Subscriptions: `#6366F1` (Indigo)
- Groceries: `#10B981` (Green)

**Income Categories:**

- Salary: `#10B981` (Green)
- Freelance: `#3B82F6` (Blue)
- Investments: `#6366F1` (Indigo)
- Business: `#14B8A6` (Teal)
- Gifts: `#EC4899` (Pink)
- Other Income: `#6B7280` (Gray)

#### Neutral Colors

**Gray Scale:**

- `#111827` - Primary text (Dark mode safe)
- `#374151` - Secondary text
- `#6B7280` - Tertiary text, disabled states
- `#9CA3AF` - Placeholder text
- `#D1D5DB` - Borders, dividers
- `#E5E7EB` - Background (light)
- `#F3F4F6` - Card backgrounds
- `#F9FAFB` - Page background
- `#FFFFFF` - White

**Dark Mode Palette:**

- `#0F172A` - Background
- `#1E293B` - Card background
- `#334155` - Borders
- `#E2E8F0` - Primary text
- `#94A3B8` - Secondary text

### 2.2 Typography

#### Font Family

**Primary Font:** SF Pro (iOS) / Roboto (Android)

- System fonts for optimal performance and native feel
- Fallback: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif

#### Type Scale

**Display:**

- Font Size: 32px
- Font Weight: Bold (700)
- Line Height: 40px
- Usage: Splash screens, empty states

**H1 - Page Headers:**

- Font Size: 24px
- Font Weight: Bold (700)
- Line Height: 32px
- Letter Spacing: -0.5px
- Usage: Screen titles

**H2 - Section Headers:**

- Font Size: 20px
- Font Weight: Semibold (600)
- Line Height: 28px
- Usage: Card titles, section dividers

**H3 - Card Headers:**

- Font Size: 18px
- Font Weight: Semibold (600)
- Line Height: 24px
- Usage: Individual cards, list items

**Body - Regular:**

- Font Size: 16px
- Font Weight: Regular (400)
- Line Height: 24px
- Usage: Main content, descriptions

**Body - Small:**

- Font Size: 14px
- Font Weight: Regular (400)
- Line Height: 20px
- Usage: Supporting text, labels

**Caption:**

- Font Size: 12px
- Font Weight: Regular (400)
- Line Height: 16px
- Color: `#6B7280`
- Usage: Timestamps, metadata

**Numeric Display (Amounts):**

- Font Size: Variable (18-32px based on context)
- Font Weight: Semibold (600)
- Font Variant: Tabular numbers
- Usage: Money amounts, percentages

### 2.3 Spacing System

Based on 8px grid for consistent alignment:

- `xs: 4px` - Tight spacing within components
- `sm: 8px` - Default spacing between related elements
- `md: 16px` - Card padding, spacing between sections
- `lg: 24px` - Major section spacing
- `xl: 32px` - Page margins (horizontal)
- `2xl: 48px` - Large vertical spacing

### 2.4 Border Radius

- `sm: 4px` - Buttons, input fields
- `md: 8px` - Cards, modals
- `lg: 12px` - Large cards, bottom sheets
- `xl: 16px` - Floating action buttons
- `full: 999px` - Pills, circular elements

### 2.5 Shadows & Elevation

**Card Shadow (Elevation 1):**

```css
shadow:
  0px 1px 3px rgba(0, 0, 0, 0.1),
  0px 1px 2px rgba(0, 0, 0, 0.06);
```

**Modal Shadow (Elevation 2):**

```css
shadow:
  0px 4px 6px rgba(0, 0, 0, 0.1),
  0px 2px 4px rgba(0, 0, 0, 0.06);
```

**FAB Shadow (Elevation 3):**

```css
shadow:
  0px 10px 15px rgba(0, 0, 0, 0.1),
  0px 4px 6px rgba(0, 0, 0, 0.05);
```

### 2.6 Iconography

**Icon Library:** React Native Vector Icons (MaterialCommunityIcons, Ionicons)

**Icon Sizes:**

- Small: 16px (inline with text)
- Medium: 24px (standard UI elements)
- Large: 32px (feature icons, empty states)
- XLarge: 48px (onboarding, placeholders)

**Icon Style:**

- Outline style for inactive/secondary actions
- Filled style for active/primary actions
- Consistent 2px stroke width for outline icons

---

## 3. Screen-by-Screen Specifications

### 3.1 Splash Screen

**Purpose:** Brand introduction while app initializes

**Layout:**

```
┌─────────────────────────┐
│                         │
│                         │
│       [App Logo]        │
│                         │
│       FinTrac           │
│                         │
│  [Loading Indicator]    │
│                         │
│                         │
└─────────────────────────┘
```

**Elements:**

- App logo: 120x120px, centered
- App name: Display font, 32px, centered below logo
- Tagline (optional): "Smart Money Management."
- Loading spinner: Small, below tagline
- Background: Gradient from Primary Blue to Secondary Blue

**Duration:** 1.5-2 seconds (or until data loaded)

---

### 3.2 Onboarding Screens (3 Slides)

**Slide 1: Welcome**

```
┌─────────────────────────┐
│    [Skip]          1/3  │
│                         │
│   [Illustration]        │
│   Track Your Money      │
│                         │
│   Log income, expenses, │
│   and track your        │
│   financial health      │
│                         │
│   ● ○ ○                 │
│        [Next →]         │
└─────────────────────────┘
```

**Slide 2: Budgets & Debts**

```
┌─────────────────────────┐
│    [Skip]          2/3  │
│                         │
│   [Illustration]        │
│   Budgets & Debts       │
│                         │
│   Set spending limits,  │
│   manage debts, and     │
│   stay on top of bills  │
│                         │
│   ○ ● ○                 │
│        [Next →]         │
└─────────────────────────┘
```

**Slide 3: Insights**

```
┌─────────────────────────┐
│    [Skip]          3/3  │
│                         │
│   [Illustration]        │
│   Powerful Insights     │
│                         │
│   Visualize spending    │
│   patterns, export      │
│   reports, and achieve  │
│   your financial goals  │
│                         │
│   ○ ○ ●                 │
│     [Get Started]       │
└─────────────────────────┘
```

**Design Specs:**

- Illustrations: 240x240px, custom or from illustration library
- Page indicators: 8px circles, 4px apart
- Buttons: Full-width minus 32px margin, 48px height
- Swipeable horizontally
- Auto-advance option: 3 seconds per slide

---

### 3.3 Dashboard (Home Screen)

**Navigation:** Bottom Tab Bar > Home Icon (active)

**Purpose:** Overview of financial status and quick actions

**Layout:**

```
┌─────────────────────────────┐
│ ☰  FinTrac            [👤]  │ ← Header
├─────────────────────────────┤
│                             │
│ ┌─────────────────────────┐ │
│ │ Today - Feb 10, 2026    │ │ ← Date Header
│ └─────────────────────────┘ │
│                             │
│ ┌─── Balance Overview ───┐  │
│ │ Current Balance         │  │
│ │                         │  │
│ │    ₹12,450              │  │ ← Large green
│ │                         │  │
│ │ ↗️ Income:  ₹5,000     │  │
│ │ ↘️ Expense: ₹2,340     │  │
│ │                         │  │
│ │ Net: +₹2,660           │  │ ← Green color
│ └─────────────────────────┘ │
│                             │
│ ┌─── Budget Alerts ──────┐  │
│ │ 🔴 Transport    117%   │  │
│ │ [██████████████] Over   │  │
│ │                         │  │
│ │ 🟡 Food        84%     │  │
│ │ [████████████░] Warning │  │
│ └─────────────────────────┘ │
│                             │
│ ┌─── Recent Transactions ┐  │
│ │ 🍔 Groceries  -₹450    │  │
│ │    11:30 AM             │  │
│ │                         │  │
│ │ 💼 Freelance   +₹5,000 │  │
│ │    09:00 AM             │  │
│ │                         │  │
│ │ [View All →]            │  │
│ └─────────────────────────┘ │
│                             │
└─────────────────────────────┘
         [+]  ← FAB
┌──────────────────────────────┐
│ [🏠] [💰] [📊] [⚙️]         │ ← Bottom Nav
└──────────────────────────────┘
```

**Header (Fixed):**

- Height: 56px
- Background: White (light mode) / `#1E293B` (dark mode)
- Left: Hamburger menu icon (24px) - Opens drawer
- Center: "FinTrac" (H2 font)
- Right: Profile avatar (32px circle)
- Shadow: Elevation 1

**Date Header:**

- Card style, 8px margin
- "Today - [Date]" in Body font
- Tap to open date picker

**Balance Overview Card:**

- Margin: 8px horizontal, 4px vertical
- Padding: 16px
- Border radius: 12px
- Background: White / `#1E293B`
- Shadow: Elevation 1
- Balance: Large font (28px), bold
- Green if positive, red if negative
- Income/Expense: Icons with arrows, aligned left
- Net: Bold, color-coded

**Budget Alerts Card:**

- Shows budgets at warning (75%+) or over budget (100%+)
- Each budget: Category name, percentage, progress bar
- Color-coded: Yellow for warning, Red for over
- Tap: Navigate to Budgets screen
- Hidden if no alerts

**Recent Transactions Card:**

- List of 3-5 latest transactions
- Each entry:
  - Left: Category color dot (12px circle) or category icon
  - Title: Description or category name, H3 font
  - Subtitle: Timestamp, Caption font
  - Right: Amount, color-coded (green +, red -)
- "View All" button at bottom

**FAB (Floating Action Button):**

- Position: Bottom right, 16px from edge, above tab bar
- Size: 56px diameter
- Background: Primary Blue gradient
- Icon: "+" (24px, white)
- Shadow: Elevation 3
- Tap: Opens quick action bottom sheet

**Bottom Navigation Bar:**

- Height: 60px (iOS), 56px (Android)
- Background: White / `#1E293B`
- 4 tabs evenly spaced
- Icons: 24px, with labels (10px font)
- Active: Primary Blue, filled icon
- Inactive: Gray, outline icon

**Tabs:**

1. Home (🏠)
2. Finance (💰)
3. Analytics (📊)
4. Settings (⚙️)

---

### 3.4 Quick Action Bottom Sheet

**Trigger:** Tap FAB on Dashboard

**Layout:**

```
┌─────────────────────────────┐
│ [────] Handle               │
│                             │
│ Quick Actions               │
│                             │
│ ┌─────────────────────────┐ │
│ │ ➕  Add Income          │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ ➖  Add Expense         │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 💳  Record Debt/Credit  │ │
│ └─────────────────────────┘ │
│                             │
│        [Cancel]             │
│                             │
└─────────────────────────────┘
```

**Design Specs:**

- Slides up from bottom with spring animation
- Handle: 32px wide, 4px tall, gray, centered
- Background: White / `#1E293B`
- Border radius: 16px (top corners only)
- Max height: 60% of screen

**Action Buttons:**

- Full width minus 16px margin each side
- Height: 56px
- Border radius: 8px
- Icon left, text left-aligned
- Hover/Press: Background tint of Primary Blue
- Tap: Navigate to respective screen

---

### 3.5 Finance Screen

**Navigation:** Bottom Tab Bar > Finance Icon

**Layout:**

```
┌─────────────────────────────┐
│ Finance               [🔍]  │
├─────────────────────────────┤
│                             │
│ ┌─ Balance Overview ──────┐ │
│ │ Current Balance         │ │
│ │                         │ │
│ │    ₹12,450              │ │ ← Large green
│ │                         │ │
│ │ ↗️ +₹5,000  ↘️ -₹2,340 │ │
│ └─────────────────────────┘ │
│                             │
│ [All] [Income] [Expense]    │
│ [Debt] [Credit]             │ ← Filter chips
│                             │
│ Today - Feb 10              │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🍔 Groceries            │ │
│ │ Food & Dining           │ │
│ │ 11:30 AM                │ │
│ │               -₹450     │ │ ← Red
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 💼 Freelance Payment    │ │
│ │ Freelance Work          │ │
│ │ 09:00 AM                │ │
│ │              +₹5,000    │ │ ← Green
│ └─────────────────────────┘ │
│                             │
│ Yesterday - Feb 9           │
│                             │
│ ┌─────────────────────────┐ │
│ │ ⚡ Electricity Bill     │ │
│ │ Utilities               │ │
│ │ 02:30 PM                │ │
│ │              -₹1,890    │ │
│ └─────────────────────────┘ │
│                             │
└─────────────────────────────┘
         [+]
```

**Balance Card:**

- Prominent placement at top
- Large numeric display (32px)
- Green if positive, red if negative
- Income/Expense summary below with icons and arrows

**Filter Chips:**

- Horizontally scrollable
- Pill-shaped buttons
- Active: Filled Primary Blue
- Inactive: Outline gray
- Tap to filter transactions

**Transaction Cards:**

- Icon or category emoji
- Transaction name (H3)
- Category name (Caption, gray)
- Timestamp (Caption)
- Amount: Right-aligned, color-coded
  - Income: Green with +
  - Expense: Red with -
  - Debt: Blue with +
  - Credit: Orange with -

**Date Dividers:**

- Day name + date, Caption font, uppercase
- Subtle horizontal line below

---

### 3.6 Add Transaction Screen

**Trigger:** Quick Action > Add Income/Expense OR FAB on Finance tab

**Layout:**

```
┌─────────────────────────────┐
│ ← Add Expense         [Save]│
├─────────────────────────────┤
│                             │
│ [Income] [Expense] [Debt]   │
│         [Credit]            │ ← Type selector
│                             │
│ Amount *                    │
│ ┌─────────────────────────┐ │
│ │ ₹                       │ │
│ │       2,450             │ │ ← Large input
│ └─────────────────────────┘ │
│                             │
│ Category *                  │
│ ┌─────────────────────────┐ │
│ │ 🍔 Groceries        [▼] │ │
│ └─────────────────────────┘ │
│                             │
│ Date *                      │
│ ┌─────────────────────────┐ │
│ │ Feb 10, 2026        [📅]│ │
│ └─────────────────────────┘ │
│                             │
│ Payment Method              │
│ ┌─────────────────────────┐ │
│ │ Credit Card         [▼] │ │
│ └─────────────────────────┘ │
│                             │
│ Description                 │
│ ┌─────────────────────────┐ │
│ │ Monthly groceries       │ │
│ └─────────────────────────┘ │
│                             │
│ Notes                       │
│ ┌─────────────────────────┐ │
│ │                         │ │
│ └─────────────────────────┘ │
│                             │
│ [📷 Add Receipt]            │
│                             │
└─────────────────────────────┘
```

**Type Selector:**

- Chip-style buttons
- Changes form color scheme based on selection
- Income: Green accent
- Expense: Red accent
- Debt: Blue accent
- Credit: Orange accent

**Amount Input:**

- Centered, large font (32px)
- Currency symbol prefix
- Numeric keyboard
- Comma separators auto-added

**Category Dropdown:**

- Shows icon + name
- Opens bottom sheet with grouped categories
- Search at top of bottom sheet

**Receipt Upload:**

- Opens camera or gallery
- Thumbnail preview shown after upload
- X button to remove

---

### 3.7 Analytics Screen

**Navigation:** Bottom Tab Bar > Analytics Icon

**Layout:**

```
┌─────────────────────────────┐
│ Analytics            [Export]│
├─────────────────────────────┤
│                             │
│ [This Week ▼]              │ ← Period selector
│                             │
│ ┌─ Income vs Expense ────┐  │
│ │                         │  │
│ │   Net Savings           │  │
│ │      +₹6,550            │  │ ← Large number
│ │                         │  │
│ │   ↑ 12% vs last week    │  │
│ │                         │  │
│ │ [Bar Chart]             │  │
│ │  ↗️ ₹15,000 Income     │  │
│ │  ↘️ ₹8,450 Expense     │  │
│ └─────────────────────────┘ │
│                             │
│ ┌─ Expense Breakdown ────┐  │
│ │                         │  │
│ │ [Pie Chart]             │  │
│ │                         │  │
│ │ 🍔 Food        35%     │  │
│ │ 🏠 Housing     25%     │  │
│ │ 🚗 Transport   20%     │  │
│ │ 🎮 Other       20%     │  │
│ └─────────────────────────┘ │
│                             │
│ ┌─ Spending Trend ───────┐  │
│ │                         │  │
│ │ [Line Graph]            │  │
│ │ Daily spending this week│  │
│ │                         │  │
│ └─────────────────────────┘ │
│                             │
│ ┌─ Budget Status ────────┐  │
│ │ 🔴 Transport    117%   │  │
│ │ 🟡 Food         84%    │  │
│ │ 🟢 Shopping     53%    │  │
│ │ [View All Budgets →]   │  │
│ └─────────────────────────┘ │
│                             │
└─────────────────────────────┘
```

**Period Selector:**

- Dropdown: Today, This Week, This Month, Last Month, Custom
- Prominent at top
- All data below updates based on selection

**Income vs Expense Card:**

- Large net savings display (32px font)
- Comparison to previous period with arrow and percentage
- Color-coded: Green for positive, Red for negative
- Bar chart: Dual bars for Income (Green) vs Expense (Red)

**Expense Breakdown Card:**

- Pie/Donut chart
- Interactive: Tap slice to drill down
- Legend below with percentages
- Top 4 categories, rest grouped as "Other"
- Vibrant category colors

**Spending Trend Card:**

- Line graph showing daily/weekly spending
- Smooth curved line with gradient fill
- Data points: Tappable to show exact value

**Budget Status Card:**

- Quick summary of active budgets
- Color-coded progress bars
- "View All Budgets" link

**Export Button:**

- Top right header
- Opens export options modal

---

### 3.8 Analytics Detail Screen (Drill-down)

**Trigger:** Tap on pie chart slice or category in analytics

**Layout:**

```
┌─────────────────────────────┐
│ ← Food & Dining Analytics   │
├─────────────────────────────┤
│                             │
│ This Week                   │
│                             │
│ ┌─────────────────────────┐ │
│ │   Total Spent            │ │
│ │     ₹2,950               │ │
│ │                         │ │
│ │   35% of total expenses │ │
│ │   ↑ ₹450 vs last week  │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─ Daily Breakdown ───────┐ │
│ │                         │ │
│ │ Mon  ████████  ₹620     │ │
│ │ Tue  ██████    ₹480     │ │
│ │ Wed  ██████████ ₹780    │ │
│ │ Thu  ████       ₹320    │ │
│ │ Fri  ██████     ₹500    │ │
│ │ Sat  ███        ₹250    │ │
│ │ Sun  ░░░░       ₹0      │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─ Payment Methods ──────┐  │
│ │ UPI              ₹1,200 │  │
│ │ Credit Card      ₹980   │  │
│ │ Cash             ₹770   │  │
│ └─────────────────────────┘ │
│                             │
│ ┌─ Recent Transactions ──┐  │
│ │ Groceries - ₹450       │  │
│ │ Today, 11:30 AM        │  │
│ │                         │  │
│ │ Restaurant - ₹780       │  │
│ │ Yesterday, 7:30 PM     │  │
│ └─────────────────────────┘ │
│                             │
└─────────────────────────────┘
```

**Design Notes:**

- Category color accent throughout
- Horizontal bars for daily breakdown
- Payment method breakdown for additional insight
- Tappable transactions link to transaction detail

---

### 3.9 Budget Screen

**Navigation:** Finance Tab > "Budgets" or Analytics > View All Budgets

**Layout:**

```
┌─────────────────────────────┐
│ ← Budgets           [+ Add] │
├─────────────────────────────┤
│                             │
│ February 2026               │
│                             │
│ ┌─ Overall Budget ─────────┐ │
│ │ ₹25,000 / ₹30,000       │ │
│ │ [████████████░░] 83%    │ │
│ │                         │ │
│ │ ₹5,000 remaining        │ │
│ │ 18 days left             │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─ Food & Dining ─────────┐ │
│ │ ₹4,200 / ₹5,000         │ │
│ │ [████████████░] 84%     │ │
│ │ On track 🎯             │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─ Transportation ────────┐ │
│ │ ₹3,500 / ₹3,000         │ │
│ │ [██████████████] 117%   │ │ ← Red
│ │ ⚠️ Over budget          │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─ Entertainment ─────────┐ │
│ │ ₹800 / ₹2,000           │ │
│ │ [████░░░░░░] 40%        │ │
│ │ Under budget 👍         │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─ Shopping ──────────────┐ │
│ │ ₹2,100 / ₹4,000         │ │
│ │ [██████░░░░] 53%        │ │
│ │ On track 🎯             │ │
│ └─────────────────────────┘ │
│                             │
└─────────────────────────────┘
```

**Budget Cards:**

- Progress bar with gradient:
  - Green: 0-75%
  - Yellow: 75-90%
  - Orange: 90-100%
  - Red: 100%+
- Status indicators:
  - 🎯 On track (50-90%)
  - 👍 Under budget (<50%)
  - ⚠️ Over budget (100%+)
  - 🔥 Way over (120%+)

**Add Budget Flow:**

- Select category
- Enter monthly limit
- Optional: Set rollover preference
- Optional: Set alert threshold (default 75%)

---

### 3.10 Debt/Credit Management Screen

**Navigation:** Finance Tab > Filter > Debt/Credit

**Layout:**

```
┌─────────────────────────────┐
│ ← Debts & Credits    [+ Add]│
├─────────────────────────────┤
│                             │
│ ┌─ Summary ───────────────┐ │
│ │ Money Owed to You       │ │
│ │      ₹15,000            │ │ ← Blue
│ │                         │ │
│ │ Money You Owe           │ │
│ │      ₹42,000            │ │ ← Orange
│ │                         │ │
│ │ Net: -₹27,000           │ │
│ └─────────────────────────┘ │
│                             │
│ [Debts] [Credits]           │ ← Tabs
│                             │
│ OVERDUE                     │
│                             │
│ ┌─────────────────────────┐ │
│ │ 💳 Credit Card          │ │
│ │ Bank of America         │ │
│ │ ₹12,000 / ₹15,000       │ │
│ │ [████████░░] 80%        │ │
│ │                         │ │
│ │ Due: Jan 15 (26 days ago)│ │
│ │ 🔴 OVERDUE              │ │
│ │                         │ │
│ │ [Pay Now] [View Details]│ │
│ └─────────────────────────┘ │
│                             │
│ UPCOMING                    │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🏠 Home Loan EMI        │ │
│ │ HDFC Bank               │ │
│ │ ₹25,000 due             │ │
│ │                         │ │
│ │ Due: Feb 28 (18 days)   │ │
│ │ 🟡 UPCOMING             │ │
│ │                         │ │
│ │ [Pay Now] [View Details]│ │
│ └─────────────────────────┘ │
│                             │
└─────────────────────────────┘
```

**Card Design:**

- Overdue: Red accent border
- Due soon (<7 days): Yellow accent border
- On time: No special styling
- Progress bar for installment loans
- Contact info with tap-to-call/message

**Detail View:**

- Full payment history
- Amortization schedule
- Interest breakdown
- Edit due date/amount
- Mark as settled

---

### 3.11 Settings Screen

**Navigation:** Bottom Tab Bar > Settings Icon

**Layout:**

```
┌─────────────────────────────┐
│ Settings                    │
├─────────────────────────────┤
│                             │
│ ┌─ Profile ───────────────┐ │
│ │ [Avatar]  John Doe      │ │
│ │           john@mail.com │ │
│ └─────────────────────────┘ │
│                             │
│ PREFERENCES                 │
│                             │
│ Currency                    │
│ INR (₹)                 [→] │
│                             │
│ Week Starts On              │
│ Monday                  [→] │
│                             │
│ Date Format                 │
│ DD/MM/YYYY              [→] │
│                             │
│ Theme                       │
│ System Default          [→] │
│                             │
│ CATEGORIES                  │
│                             │
│ View Categories          [→]│
│                             │
│ NOTIFICATIONS               │
│                             │
│ Budget Alert Notifications  │
│ [Toggle ON]             [→] │
│                             │
│ Due Date Reminders          │
│ [Toggle ON]             [→] │
│                             │
│ DATA & BACKUP               │
│                             │
│ Export All Data         [→] │
│                             │
│ Backup to Cloud         [→] │
│ Last backup: 2 hours ago    │
│                             │
│ Import Data             [→] │
│                             │
│ SECURITY                    │
│                             │
│ App Lock                    │
│ [Toggle ON]             [→] │
│                             │
│ ABOUT                       │
│                             │
│ Privacy Policy          [→] │
│ Terms of Service        [→] │
│ App Version: 1.0.0          │
│                             │
└─────────────────────────────┘
```

**Design Notes:**

- Grouped sections with headers (Caption, uppercase, gray)
- List items: 56px height
- Right arrow (→) for navigation items
- Toggle switches for boolean settings
- Subtle divider lines between items
- Tap ripple effect on Android

---

### 3.12 Category View Screen (Read-Only)

**Trigger:** Settings > View Expense/Income Categories

**Note:** Categories are predefined and cannot be created, edited, or deleted by users.
Users can only browse the available categories. Categories are managed via a backend seed script.

**Layout:**

```
┌─────────────────────────────┐
│ ← Categories                │
├─────────────────────────────┤
│                             │
│ [All] [Expense] [Income]    │ <- Filter chips
│                             │
│ EXPENSE                     │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🍔 Food & Dining        │ │
│ │ #F97316                  │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🏠 Housing              │ │
│ │ #7C3AED                  │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🚗 Transport            │ │
│ │ #0EA5E9                  │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🛍️ Shopping             │ │
│ │ #EC4899                  │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🎮 Entertainment        │ │
│ │ #8B5CF6                  │ │
│ └─────────────────────────┘ │
│                             │
│ INCOME                      │
│                             │
│ ┌─────────────────────────┐ │
│ │ 💼 Salary               │ │
│ │ #10B981                  │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 💻 Freelance            │ │
│ │ #3B82F6                  │ │
│ └─────────────────────────┘ │
│                             │
└─────────────────────────────┘
```

**Design Notes:**

- No "Add" button - categories are predefined
- No edit/delete actions - read-only view
- Color dot indicator next to each category name
- Filter chips to switch between All / Expense / Income

---

### 3.13 Export Screen

**Trigger:** Analytics > Export OR Settings > Export All Data

**Layout:**

```
┌─────────────────────────────┐
│ ← Export Data       [Export]│
├─────────────────────────────┤
│                             │
│ Data Type                   │
│ ┌─────────────────────────┐ │
│ │ ☑️ Transactions         │ │
│ │ ☑️ Budgets              │ │
│ │ ☑️ Debts & Credits      │ │
│ └─────────────────────────┘ │
│                             │
│ Date Range                  │
│ ┌─────────────────────────┐ │
│ │ This Month          [▼] │ │
│ └─────────────────────────┘ │
│                             │
│ Custom Range                │
│ ┌───────────┬─────────────┐ │
│ │ Start Date│  End Date   │ │
│ │ Feb 1     │  Feb 10     │ │
│ └───────────┴─────────────┘ │
│                             │
│ Format                      │
│ ┌─────────────────────────┐ │
│ │ ○ CSV                   │ │
│ │ ● PDF Report            │ │
│ │ ○ Excel                 │ │
│ └─────────────────────────┘ │
│                             │
│ Options                     │
│ ┌─────────────────────────┐ │
│ │ ☑️ Include Notes        │ │
│ │ ☑️ Include Categories   │ │
│ │ ☑️ Include Summary      │ │
│ │ ☐ Include Charts        │ │
│ └─────────────────────────┘ │
│                             │
│ Preview                     │
│ Approx. 234 entries         │
│ Est. file size: 145 KB      │
│                             │
└─────────────────────────────┘
```

**Export Button Action:**

- Generates file (with loading spinner)
- Opens system share sheet
- Options: Email, Save to Files, Cloud storage

---

### 3.14 Recurring Transaction Setup

**Trigger:** Add Transaction > Toggle "Recurring"

**Additional Fields:**

```
┌─────────────────────────────┐
│                             │
│ Recurring                   │
│ [Toggle ON]                 │
│                             │
│ Frequency                   │
│ ┌─────────────────────────┐ │
│ │ Monthly             [▼] │ │
│ └─────────────────────────┘ │
│                             │
│ Start Date                  │
│ ┌─────────────────────────┐ │
│ │ Feb 1, 2026         [📅]│ │
│ └─────────────────────────┘ │
│                             │
│ End Condition               │
│ ┌─────────────────────────┐ │
│ │ ○ Never                 │ │
│ │ ● After 12 occurrences  │ │
│ │ ○ On specific date      │ │
│ └─────────────────────────┘ │
│                             │
│ Next Occurrence             │
│ Mar 1, 2026                 │
│                             │
│ ☑️ Notify when created     │
│                             │
└─────────────────────────────┘
```

---

## 4. Component Library

### 4.1 Buttons

**Primary Button**

- Background: Primary Blue `#2563EB`
- Text: White, Semibold
- Height: 48px
- Border radius: 8px
- Padding: 16px horizontal
- Shadow: Elevation 1
- States:
  - Default: Solid color
  - Pressed: Darker shade `#1E40AF`
  - Disabled: Gray `#9CA3AF`, 50% opacity

**Secondary Button**

- Background: White
- Border: 2px Primary Blue
- Text: Primary Blue, Semibold
- Same dimensions as primary
- States:
  - Default: Outlined
  - Pressed: Light blue background tint
  - Disabled: Gray border and text

**Text Button**

- No background or border
- Text: Primary Blue, Semibold
- Padding: 8px horizontal
- States:
  - Default: Blue text
  - Pressed: Darker blue, slight scale down (0.95)
  - Disabled: Gray text

**Icon Button**

- Size: 40x40px
- Border radius: 20px (circular)
- Icon: 24px, centered
- Background: Transparent
- Pressed: Gray background tint `#F3F4F6`

**FAB (Floating Action Button)**

- Size: 56x56px
- Border radius: 28px (circular)
- Background: Gradient Primary to Secondary Blue
- Icon: White, 24px
- Shadow: Elevation 3
- Pressed: Slight scale up (1.05)

**Chip/Tag Button**

- Height: 32px
- Border radius: 16px (pill)
- Padding: 12px horizontal
- Active: Filled Primary Blue, White text
- Inactive: Outlined gray, Gray text
- Icon optional (left side, 16px)

### 4.2 Input Fields

**Text Input**

- Height: 48px
- Border: 1px `#D1D5DB`
- Border radius: 8px
- Padding: 12px horizontal
- Font: Body (16px)
- States:
  - Default: Gray border
  - Focus: 2px Primary Blue border, blue label
  - Error: Red border, red label
  - Disabled: Gray background, gray text

**Label**

- Font: Body Small (14px), `#374151`
- Margin bottom: 8px
- Required indicator: Red asterisk \*

**Helper Text**

- Font: Caption (12px), `#6B7280`
- Margin top: 4px
- Error text: Red `#EF4444`

**Search Input**

- Same as text input
- Left icon: Magnifying glass, 20px, gray
- Right icon: X to clear (when text present)
- Placeholder: "Search..."

**Numeric Input (Amount)**

- Text align: Center or Right
- Font: Numeric display (18-32px), tabular
- Currency symbol: Prefix, gray
- Decimal places: 2, auto-formatted

**Textarea**

- Min height: 96px (3 lines)
- Max height: 192px (6 lines)
- Scrollable if exceeds max
- Resize: Vertical only (iOS)

### 4.3 Cards

**Standard Card**

- Background: White / `#1E293B` (dark)
- Border radius: 12px
- Padding: 16px
- Margin: 8px horizontal, 4px vertical
- Shadow: Elevation 1

**Stat Card (Dashboard)**

- Larger padding: 20px
- Contains:
  - Icon or emoji (32px) - top left
  - Label (Caption) - below icon
  - Value (H1 or Display) - prominent
  - Trend indicator - bottom right
- Tap: Navigate to detail view

**List Item Card**

- Height: Variable (min 72px)
- Padding: 12px
- Border bottom: 1px `#E5E7EB` (except last)
- Tap: Ripple effect, navigate
- Swipe: Reveal actions (edit, delete)

**Progress Card**

- Contains:
  - Header with title and amount
  - Progress bar
  - Footer with status text
- Color-coded progress bar

### 4.4 Progress Indicators

**Linear Progress Bar**

- Height: 8px
- Border radius: 4px (rounded ends)
- Background: `#E5E7EB`
- Fill: Gradient based on status
  - Green: Under budget
  - Yellow: Warning
  - Red: Over budget
- Animated fill on load

**Circular Progress (Pie Chart Style)**

- Size: 120px diameter (standard), 200px (large)
- Stroke width: 8px
- Background ring: Light gray
- Foreground: Category color(s)
- Center text: Percentage or value
- Animated stroke-dashoffset

**Loading Spinner**

- Size: 24px (small), 40px (medium), 56px (large)
- Color: Primary Blue
- Animation: Continuous rotation
- Usage: Page load, data fetch, export generation

### 4.5 Charts

**Pie Chart**

- Library: react-native-chart-kit or Victory Native
- Size: 200x200px
- Segments: Up to 5 (combine rest as "Other")
- Colors: Category color palette
- Labels: Outside with lines to segments
- Center hole: 40% diameter (donut style)
- Interactive: Tap segment to drill down

**Bar Chart**

- Height: 200px
- Bar width: Variable (based on # of bars)
- Gap between bars: 8px
- Y-axis: Amount, auto-scaled
- X-axis: Time periods (days, weeks, months)
- Grid lines: Horizontal only, subtle gray
- Colors: Income (green) / Expense (red)
- Hover/Tap: Show exact value in tooltip

**Line Chart**

- Height: 200px
- Line: 3px width, smooth curve
- Area fill: Gradient from line color to transparent
- Data points: 6px circles on line
- Grid: Both axes, subtle
- Multiple series: Different colors with legend
- Tap point: Show tooltip with value and date

**Horizontal Bar (Budget Progress)**

- Height: 24px per bar
- Full width minus padding
- Rounded ends
- Label: Left side (category name)
- Value: Right side (amount/total)
- Percentage inside bar

### 4.6 Modals & Bottom Sheets

**Modal (Full Screen)**

- Slides up from bottom
- Header:
  - Left: Close X or Back ←
  - Center: Title
  - Right: Action button (Save, Done)
- Content: Scrollable
- Background: White / Dark
- Safe area insets respected

**Bottom Sheet**

- Max height: 80% of screen
- Draggable handle at top (32x4px rounded)
- Backdrop: Semi-transparent black (60%)
- Tap backdrop: Dismiss
- Drag down: Dismiss
- Spring animation on open/close
- Keyboard avoiding: Pushes up when keyboard shown

**Alert Dialog**

- Centered overlay
- Max width: 90% of screen width
- Background: White / Dark
- Border radius: 16px
- Shadow: Elevation 2
- Contents:
  - Title (H2)
  - Message (Body)
  - Actions (1-3 buttons)
- Buttons: Horizontal if ≤2, vertical if >2

**Toast / Snackbar**

- Position: Bottom, 16px from edge
- Background: Dark gray `#374151`
- Text: White
- Border radius: 8px
- Padding: 12px 16px
- Max width: 90% screen
- Auto-dismiss: 3 seconds
- Optional action button (right side)
- Swipe down: Dismiss

### 4.7 Lists

**Flat List**

- Item height: 72px (single line), 96px (two line)
- Dividers: 1px `#E5E7EB` between items
- Pull to refresh: Spinner at top
- Scroll to top: Tap status bar (iOS)
- Empty state: Centered illustration + text

**Section List**

- Section headers:
  - Background: `#F9FAFB` / `#0F172A`
  - Padding: 8px 16px
  - Font: Caption, uppercase, semibold
  - Sticky: Yes
- Items: Same as flat list

**Swipeable List Item**

- Swipe left: Reveal actions (Edit, Delete)
- Swipe right: Quick action (Mark paid, etc.)
- Action button: 72px width, full height
- Icons: 24px, centered
- Colors: Blue (edit), Red (delete), Green (paid)

### 4.8 Date & Time Pickers

**Date Picker**

- Type: Calendar view (iOS), Spinner (Android), or unified
- Selected date: Highlighted in Primary Blue
- Today: Outlined in blue
- Quick options: Today, Yesterday, Start of Week/Month
- Buttons: Cancel, Done

**Date Range Picker**

- Two date pickers: Start and End
- Visual: Calendar with range highlighted
- Validation: End must be after start

### 4.9 Category Selector

**Layout:**

```
┌─────────────────────────────┐
│ Select Category             │
│                             │
│ [🔍 Search]                 │
│                             │
│ RECENT                      │
│ 🍔 Food & Dining            │
│ 🚗 Transport                │
│                             │
│ ESSENTIALS                  │
│ 🍔 Food & Dining            │
│ 🏠 Housing                  │
│ 🚗 Transport                │
│ ⚡ Utilities                │
│                             │
│ LIFESTYLE                   │
│ 🛍️ Shopping                 │
│ 🎮 Entertainment            │
│ 📚 Education                │
│                             │
└─────────────────────────────┘
```

**Design:**

- Bottom sheet style
- Search at top: Filters categories in real-time
- Grouped by parent category
- Recent: Top 3 most used
- Color dot + icon + name
- Tap row: Select and dismiss
- Scroll: Smooth with momentum

### 4.10 Empty States

**No Data Empty State**

```
┌─────────────────────────────┐
│                             │
│       [Large Icon]          │
│          128x128            │
│                             │
│   No transactions yet       │
│                             │
│   Tap + to start tracking   │
│   your finances             │
│                             │
│      [Get Started]          │
│                             │
└─────────────────────────────┘
```

**Error State**

```
┌─────────────────────────────┐
│                             │
│       [Error Icon]          │
│          ⚠️                 │
│                             │
│   Something went wrong      │
│                             │
│   Unable to load data.      │
│   Please try again.         │
│                             │
│      [Retry]                │
│                             │
└─────────────────────────────┘
```

**Search No Results**

```
┌─────────────────────────────┐
│                             │
│       [Search Icon]         │
│          🔍                 │
│                             │
│   No results found          │
│                             │
│   Try different keywords    │
│                             │
│    [Clear Search]           │
│                             │
└─────────────────────────────┘
```

**Design Specs:**

- Centered vertically and horizontally
- Icon: 96-128px, gray or brand color
- Heading: H2, gray
- Description: Body, lighter gray
- Button: Primary style (optional)
- Overall tone: Encouraging, not negative

---

## 5. Interactions & Animations

### 5.1 Micro-interactions

**Button Press**

- Scale: 0.95 on press, spring back to 1.0
- Duration: 100ms
- Timing: Ease-out
- Haptic: Light impact (iOS)

**Card Tap**

- Opacity: 0.7 on press
- Duration: 100ms
- Navigate: Slide transition
- Android: Ripple effect from tap point

**Toggle Switch**

- Thumb slides with spring animation
- Background color transitions
- Duration: 200ms
- Haptic: Medium impact on state change

**Pull to Refresh**

- Drag resistance after 80px
- Release threshold: 100px
- Spinner appears with fade + scale
- Auto-scroll back on complete

**Swipe to Delete**

- Threshold: 30% of width
- Reveal actions with slide animation
- Delete: Slide out with fade
- Undo toast appears at bottom

### 5.2 Page Transitions

**Tab Navigation**

- Fade transition between tabs
- Duration: 200ms
- No slide animation (instant feel)

**Stack Navigation**

- Push: Slide from right (iOS), fade from bottom (Android)
- Pop: Reverse of push
- Duration: 300ms
- Curve: Ease-in-out

**Modal Present**

- Slide up from bottom
- Duration: 300ms
- Backdrop fades in simultaneously
- Spring effect on final position

**Modal Dismiss**

- Slide down to bottom
- Backdrop fades out
- Duration: 250ms
- Gesture: Swipe down to dismiss

### 5.3 Loading States

**Skeleton Screens**

- Use for initial page loads
- Gray placeholders matching content layout
- Shimmer animation (light sweep from left to right)
- Duration: Continuous until content loads
- Replace: Fade in real content

**Spinner Overlay**

- For actions that block UI (export, save)
- Semi-transparent backdrop
- Centered spinner
- Optional loading text below spinner

**Progressive Loading**

- Load critical content first (fold)
- Below-fold content loads afterward
- Smooth scroll enabled even during load

**Optimistic Updates**

- Update UI immediately on user action
- Revert if server/validation fails
- Show subtle success indicator

### 5.4 Chart Animations

**Pie Chart**

- Animate segments sequentially
- Each segment: Grow from 0° to final angle
- Duration: 600ms total
- Stagger: 50ms between segments
- Curve: Ease-out

**Bar Chart**

- Bars grow from 0 to final height
- All bars animate simultaneously
- Duration: 500ms
- Curve: Ease-out cubic

**Line Chart**

- Line draws from left to right
- Area fill follows line
- Duration: 800ms
- Curve: Ease-in-out
- Data points fade in after line complete

**Number Counting**

- Large numbers count up from 0
- Duration: 1000ms
- Easing: Ease-out
- Format updates during count (commas, decimals)

### 5.5 Gesture Interactions

**Swipe Gestures**

- Horizontal swipe on list items: Reveal actions
- Vertical swipe on bottom sheet: Dismiss
- Swipe on charts: Navigate between periods
- Threshold: 30% of component width/height
- Velocity: 0.5 units/ms minimum

**Pinch to Zoom**

- On charts (optional advanced feature)
- Min scale: 1.0 (default)
- Max scale: 3.0
- Double tap: Reset to 1.0

**Long Press**

- Duration: 500ms
- Trigger: Context menu or additional options
- Haptic: Medium impact on trigger
- Visual: Subtle scale up during press

### 5.6 Haptic Feedback

**iOS Haptic Types:**

- Light: Button taps, toggle switches
- Medium: Selections, confirmations
- Heavy: Errors, deletions
- Success: Completed actions
- Warning: Budget alerts
- Error: Validation failures

**Android Vibration:**

- Short (50ms): Tap feedback
- Medium (100ms): Confirmations
- Long (200ms): Errors, alerts

---

## 6. Responsive Layouts

### 6.1 Breakpoints

**Mobile (Portrait)**

- Width: 320px - 428px
- Primary orientation
- Single column layouts
- Bottom tab navigation

**Mobile (Landscape)**

- Height: 320px - 428px
- Consider larger horizontal elements
- Stack adjusts to side-by-side where space allows

**Tablet (Portrait)**

- Width: 768px - 1024px
- Two-column layouts where appropriate
- Larger cards, more content per screen
- Consider side drawer navigation

**Tablet (Landscape)**

- Width: 1024px+
- Master-detail layout patterns
- Side navigation + main content
- Multiple cards side-by-side

### 6.2 Adaptive Components

**Dashboard**

- Mobile: Single column, stacked cards
- Tablet: 2x2 grid for stat cards
- Landscape: Horizontal scroll for charts

**Analytics**

- Mobile: Stacked charts, scroll vertically
- Tablet: Charts side-by-side, 2 per row
- Detailed view: Larger charts with more data points

**Forms**

- Mobile: Full width inputs
- Tablet: Max width 600px, centered
- Two-column for related fields (start/end date)

**Lists**

- Mobile: Single column, 72px row height
- Tablet: Increase to 96px, show more info per row
- Consider grid view for category selections

### 6.3 Typography Scaling

**Base Font Size:**

- Mobile: 16px
- Tablet: 18px

**Scale Factor:**

- Headers scale up 1.1x on tablet
- Body text scales up 1.125x
- Maintain line height ratios

**Dynamic Type (iOS)**

- Support user's preferred text size
- Test at all accessibility sizes
- Ensure layout doesn't break at 200% scale

### 6.4 Safe Areas & Notches

**iOS Notch/Island:**

- Use `SafeAreaView` for top/bottom
- Header starts below notch/island
- Tab bar respects bottom safe area
- Full-screen modals: Padding for notch

**Android Navigation:**

- Respect gesture navigation area (bottom)
- System navigation bar: Transparent with padding

---

## 7. Accessibility

### 7.1 Color Contrast

**WCAG AAA Compliance:**

- All text: Minimum 7:1 contrast ratio
- Large text (18px+): Minimum 4.5:1
- Interactive elements: 3:1 against background

**Color Blind Friendly:**

- Don't rely on color alone for information
- Use icons, patterns, labels in addition to color
- Test with color blindness simulators
- Provide alternative views (e.g., list vs chart)

### 7.2 Touch Targets

**Minimum Size:**

- 44x44pt (iOS)
- 48x48dp (Android)
- Applies to all interactive elements

**Spacing:**

- 8px minimum between adjacent touch targets
- Prefer 16px for critical actions

**Hit Areas:**

- Extend beyond visible button if needed
- Use padding to increase touch area
- Especially important for small icons

### 7.3 Screen Reader Support

**Labels:**

- All images: Meaningful alt text or decorative flag
- All buttons: Clear labels (not just icons)
- Form fields: Associated labels
- Links: Descriptive text (not "click here")

**Focus Order:**

- Logical reading order (top to bottom, left to right)
- Skip navigation option for long lists
- Group related elements

**Announcements:**

- Success messages read aloud
- Error messages read with focus to field
- Loading states announced
- Dynamic content changes announced

**React Native:**

- Use `accessible={true}`
- `accessibilityLabel` for meaningful names
- `accessibilityHint` for additional context
- `accessibilityRole` for semantic meaning

### 7.4 Keyboard Navigation

**Focus Visible:**

- Clear focus indicators (2px blue outline)
- Focus moves logically through page
- Tab order matches visual order

**Keyboard Shortcuts (Optional):**

- Space: Toggle selection
- Enter: Activate button
- Esc: Close modal/bottom sheet
- Arrow keys: Navigate lists

### 7.5 Motion & Animation

**Reduce Motion:**

- Respect system preference
- Disable decorative animations
- Keep functional animations (page transitions)
- Instant transitions instead of animated

**Epilepsy Considerations:**

- No flashing more than 3 times per second
- Avoid high-contrast flickering
- Option to disable all non-essential animations

---

## 8. Dark Mode

### 8.1 Color Adaptations

**Background Colors:**

- Light: `#FFFFFF` (white)
- Dark: `#0F172A` (very dark blue)

**Card Backgrounds:**

- Light: `#F9FAFB` (off-white)
- Dark: `#1E293B` (dark slate)

**Text Colors:**

- Primary Light: `#111827` (almost black)
- Primary Dark: `#E2E8F0` (light gray)
- Secondary Light: `#6B7280` (gray)
- Secondary Dark: `#94A3B8` (lighter gray)

**Borders:**

- Light: `#E5E7EB` (light gray)
- Dark: `#334155` (dark gray)

**Semantic Colors (Same in both modes):**

- Success: `#10B981`
- Warning: `#F59E0B`
- Error: `#EF4444`
- Info: `#06B6D4`
- Primary: `#2563EB`

### 8.2 Images & Icons

**Icons:**

- Use single color (adapt to theme)
- White in dark mode, dark in light mode
- Exception: Category icons use fixed brand colors

**Illustrations:**

- Provide dark variants for complex illustrations
- Use transparent backgrounds
- Reduce brightness in dark mode

**Photos/Receipts:**

- No modification
- Display as-is in both modes

### 8.3 Shadows in Dark Mode

**Elevation:**

- Reduce shadow opacity by 50%
- Use subtle highlight on top edge instead
- Elevation 1: 1px highlight `rgba(255,255,255,0.05)`
- Elevation 2: 2px highlight
- Elevation 3: 3px highlight

### 8.4 Charts in Dark Mode

**Background:**

- Transparent or match card background
- Grid lines: Lighter in dark mode (#475569)

**Data Colors:**

- Keep vibrant category colors
- Increase saturation slightly for visibility
- Ensure 4.5:1 contrast with dark background

---

## 9. Design Assets

### 9.1 App Icon

**Sizes Required:**

- iOS: 1024x1024 (App Store), 180x180 (iPhone), 167x167 (iPad)
- Android: 512x512 (Play Store), 192x192 (xxxhdpi)

**Design:**

- Symbol: Stylized rupee/dollar symbol with chart element
- Background: Gradient Primary to Secondary Blue
- Style: Rounded square (iOS), circle/square (Android)
- No text in icon (doesn't scale well)

### 9.2 Splash Screen

**Assets:**

- Logo: 512x512 PNG with transparency
- Background: Solid color or simple gradient
- Safe area: Keep content in center 60%

**Platforms:**

- iOS: Storyboard with constraints
- Android: Drawable with layer-list

### 9.3 Illustrations

**Onboarding Illustrations:**

- Finance tracking: Person with wallet/charts
- Budgets: Person with budget dashboard
- Insights: Person looking at analytics

- Style: Flat, minimal, 2-3 colors max
- Format: SVG for scalability

**Empty States:**

- Wallet with magnifying glass (no transactions)
- Chart with zero data (no analytics)
- Piggy bank (no budgets set)
- Style: Simple line art, 1-2 colors

### 9.4 Icons

**System Icons:**

- Use React Native Vector Icons
- Libraries: MaterialCommunityIcons, Ionicons
- Sizes: 16, 20, 24, 32, 48
- Format: Vector (scales perfectly)

**Custom Icons:**

- Category icons: Emoji or custom SVG
- Consistent style if using SVG
- Optimized file sizes

### 9.5 Export Templates

**PDF Report Header:**

```
┌────────────────────────────────┐
│ [App Logo]  FinTrac            │
│                                │
│ Financial Report               │
│ February 1 - February 10, 2026│
│                                │
│ Generated: Feb 10, 2026        │
│ For: John Doe                  │
└────────────────────────────────┘
```

**Professional Styling:**

- Font: System serif (Times New Roman fallback)
- Colors: Grayscale for print-friendliness
- Charts: Black & white with patterns
- Logo: Grayscale version

---

## 10. Design Handoff

### 10.1 Design Files

**Format:**

- Figma (recommended for collaboration)
- Sketch (alternative)
- Adobe XD (alternative)

**Organization:**

- Pages: Overview, Screens, Components, Styles
- Artboards named clearly (e.g., "Dashboard - Default State")
- States: Default, Hover/Pressed, Disabled, Error
- Variants for mobile/tablet

### 10.2 Developer Resources

**Style Guide Export:**

- Colors: Hex codes, RGB values, semantic names
- Typography: Font families, sizes, weights, line heights
- Spacing: 8px grid values
- Shadows: CSS/React Native shadow properties

**Assets Export:**

- Icons: @1x, @2x, @3x (iOS), mdpi, hdpi, xhdpi, xxhdpi, xxxhdpi (Android)
- Images: Same density buckets
- Format: PNG (raster), SVG (vector)

**Component Specs:**

- Dimensions: Width, height, padding, margin
- States: All interactive states documented
- Variants: Dark mode, different sizes
- Code: Suggested React Native component structure

### 10.3 Design Tokens

**JSON Format:**

```json
{
  "colors": {
    "primary": "#2563EB",
    "success": "#10B981",
    "error": "#EF4444"
  },
  "spacing": {
    "xs": 4,
    "sm": 8,
    "md": 16,
    "lg": 24
  },
  "typography": {
    "h1": {
      "fontSize": 24,
      "fontWeight": "700",
      "lineHeight": 32
    }
  }
}
```

**Usage:**

- Import tokens in React Native app
- Ensures consistency
- Easy to update globally

### 10.4 Prototype

**Interactive Prototype:**

- Key user flows: Onboarding, Add transaction, View analytics, Manage budgets
- Transitions: Realistic navigation
- States: Show interactions (button press, form validation)
- Annotations: Explain complex interactions
- Share link: For stakeholder review

**User Testing:**

- Test prototype with target users
- Gather feedback on usability
- Iterate based on findings
- Document changes and rationale

---

## 11. Design QA Checklist

### Before Development

- [ ] All screens designed at required sizes (mobile, tablet)
- [ ] Dark mode variants for all screens
- [ ] All states documented (default, active, error, empty)
- [ ] Component library complete and organized
- [ ] Color contrast meets WCAG AAA (7:1)
- [ ] Touch targets minimum 44x44 (iOS) / 48x48 (Android)
- [ ] Typography scale is consistent
- [ ] Spacing follows 8px grid
- [ ] Icons are consistent style and size
- [ ] Illustrations are high quality and on-brand
- [ ] Export assets at all required densities
- [ ] Prototype tested with users
- [ ] Design tokens exported
- [ ] Handoff documentation complete

### During Development

- [ ] Designs match implementation pixel-perfect
- [ ] Animations match intended duration and easing
- [ ] Dark mode switches correctly
- [ ] Screen reader labels are meaningful
- [ ] Keyboard navigation works logically
- [ ] Loading states implemented
- [ ] Error states handled gracefully
- [ ] Empty states are encouraging
- [ ] Forms validate properly with clear errors
- [ ] Haptic feedback on key interactions

### Before Launch

- [ ] Test on minimum supported iOS version
- [ ] Test on minimum supported Android version
- [ ] Test on various screen sizes
- [ ] Test with large accessibility text sizes
- [ ] Test with reduce motion enabled
- [ ] Test in landscape orientation
- [ ] Test with slow network connection
- [ ] Test offline functionality
- [ ] Gather internal feedback
- [ ] Conduct final user testing round

---

## 12. Future Design Considerations

### Phase 2 Enhancements

**Widgets:**

- Home screen widget showing balance and recent transactions
- Lock screen widget for quick expense entry

**Collaboration Features:**

- Shared budgets: Family/team view
- Avatars for multiple users
- Comments/notes on shared entries
- Permissions UI (view only, edit, admin)

**AI Insights:**

- Smart suggestions section on dashboard
- Conversational UI for insights
- Predictive analytics visualizations
- Spending pattern detection

**Integrations:**

- Bank connection UI
- UPI auto-import settings
- Third-party app connections (Google Pay, PhonePe)

### Accessibility Improvements

- Voice control support
- High contrast mode
- Larger touch targets option
- Simplified UI mode for cognitive accessibility

### Platform-Specific

**iOS:**

- Siri shortcuts for adding expense
- iMessage app for quick logging
- Apple Watch app
- iPad split-view support

**Android:**

- Widget customization
- Quick settings tile for expense entry
- Wear OS app
- Tablet multi-window support

---

## Appendix

### A. Design Glossary

- **Elevation:** Visual hierarchy using shadows/depth
- **Haptic:** Touch feedback through device vibration
- **Safe Area:** Screen area not obscured by notches, navigation
- **Semantic Color:** Color with specific meaning (success, error, etc.)
- **Skeleton Screen:** Placeholder content during loading
- **Toast:** Temporary notification message
- **Touch Target:** Tappable area of an interactive element

### B. Resources

**Design Tools:**

- Figma: https://figma.com
- React Native Vector Icons: https://oblador.github.io/react-native-vector-icons/
- Material Icons: https://fonts.google.com/icons
- Coolors (color palette): https://coolors.co
- Contrast Checker: https://webaim.org/resources/contrastchecker/

**Inspiration:**

- Dribbble: Finance app designs
- Mobbin: Mobile design patterns
- Behance: UI/UX case studies

**React Native UI Libraries:**

- React Native Paper (Material Design)
- React Native Elements
- NativeBase
- UI Kitten

**Chart Libraries:**

- Victory Native
- React Native Chart Kit
- react-native-svg-charts

### C. Design Version History

**Version 1.0**

- Initial design specification
- All screens including time tracking and finance

**Version 1.1 (Current)**

- Focused on financial tracking only
- Removed time tracking screens (timer, time entries)
- Updated navigation from 5 tabs to 4 tabs
- Updated dashboard to finance-only layout
- Updated analytics to finance-only charts
- Updated categories to income/expense types
- Updated onboarding to finance-focused slides

---

**End of Design Document**

**Document Prepared By:** Design Team
**Date:** February 10, 2026
**Status:** Ready for Development
**Next Review:** After MVP completion

---

This design specification provides the blueprint for building a modern, accessible, and user-friendly financial tracking application. All designs should be implemented with attention to detail, ensuring a consistent and delightful user experience across all platforms and use cases.
