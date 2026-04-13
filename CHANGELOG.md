# Changelog

All notable changes to the Commission Calculator will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] - 2026-04-12

### Initial Release

#### Core Features
- Login and session management for the ERS (ourers.com) platform
- Scrapes transaction pay page for all dollar amounts
- Reads subtotal directly from ERS page for accurate commission base
- Scrapes order logs to determine rep assignment and split commissions

#### Commission Formula
- Damage waiver calculated as 10% of subtotal
- Commissionable revenue = subtotal + park fee + surface fee + misc fee
- Commission = commissionable revenue × 10%
- Tax, travel fee, and damage waiver excluded per policy
- Coupons and discounts reflected in subtotal automatically

#### Fee Support
- Tax (`ers_line_item_tax`)
- Travel fee (`ers_line_item_travel_fee`)
- Surface fee (`ers_line_item_option_surface_fee`)
- Park / Business / Non-Residential fee (`ers_line_item_option_park-business-non-residential`)
- Miscellaneous fees (`ers_line_item_miscellaneous_fees`)
- Coupon (`ers_line_item_coupon`)
- General discount (`ers_line_item_general_discount`)

#### Split Commission Logic
- Scans full order log to find all reps who touched the order
- Filters exempt accounts (Online Customer, autopay, Admin)
- 1 known rep → 100% commission
- 2 known reps → 50/50 split, flagged for verification
- Exempt accounts configurable via `EXEMPT_ACTIVATORS` in `.env`

#### Unpaid Order Handling
- Checks `ers_payment_line_due` — skips commission if balance > $0
- Unpaid orders still included in report, highlighted in red
- No commission calculated for unpaid rows
- Provides built-in follow-up list for outstanding balances

#### Input Modes
- **Interactive mode** (default) — enter order IDs one at a time, type `q` to finish
- **Batch mode** (`--batch orders.txt`) — process a file of order IDs
- **Month mode** (`--month "March 2026"`) — stub in place, requires Playwright (coming)

#### Export Formats
- **Excel (.xlsx)** — formatted with header, alternating rows, red unpaid rows, totals
- **PDF** — landscape, clean columns, ready to email
- **CSV** — plain text with all columns including split/flag reference columns
- **All** — export all three formats at once
- Files named: `jeff_commission_March_2026_20260412_1845.xlsx`

#### Date Handling
- Supports both old format (`12/6/2025`) and new format (`Mar 14`) event dates
- Commission period determined by earliest event date in results
- Commission based on event date, not payment date (per policy)

#### Security
- Credentials stored in `.env` only
- Dedicated read-only scraper account (separate from main admin)
- `.env` excluded from Git via `.gitignore`

---

## [Unreleased]

### Planned for 1.1.0
- Month mode via Playwright for automatic order discovery
- Startup validation of required `.env` variables
- Streamlit web UI

### Planned for 1.2.0
- Email integration — send report directly from the app
- YTD running total
- Month-over-month comparison

### Planned for 2.0.0
- Multi-user support
- Manager dashboard
- SaaS packaging for other ERS party rental operators
