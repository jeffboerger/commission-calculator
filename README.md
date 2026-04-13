# Commission Calculator
### Built for Freedom Fun Houston South — ERS Platform

> Automates monthly sales commission calculation by scraping transaction data from the ERS booking platform, verifying rep assignment, applying the commission formula, and producing a labeled, print-ready report in Excel, PDF, and CSV formats.

---

## Why This Exists

Commission calculation at Freedom Fun was a fully manual process:

- Log into the ERS platform
- Open each transaction one by one
- Manually verify that you were the assigned rep
- Copy numbers into a spreadsheet
- Apply the commission formula by hand
- Check each order again to make sure nothing was missed

This took hours every month and was error-prone. A missed order means lost pay. A miscalculation means a dispute. And with shared commissions (two reps touching the same order), the math got complicated fast.

This tool does all of that automatically. You enter order IDs, hit `q`, and get a finished, formatted report ready to email — in under a minute.

---

## Commission Formula

Based on the Mr. Dallas Fun LLC Commission Payment Policy:

```
damageWaiver = subtotal * 0.10
commRev      = subtotal + parkFee + surfaceFee + miscFee
commission   = commRev * 0.10
```

**Non-commissionable items (excluded per policy):**
- Tax
- Travel fees
- Damage waiver

**Commissionable add-ons (included):**
- Park / Business / Non-Residential fee
- Surface fee
- Miscellaneous fees (e.g. holiday weekend surcharges)

**Coupons and discounts** are already reflected in the subtotal pulled from the page — no additional math needed.

---

## Split Commission Logic

Per Section 6 of the Commission Payment Policy:

> If one salesperson prepares the quote and another secures the deposit or payment, commission is split 50/50.

The tool enforces this automatically by scanning the order logs:

1. All usernames who touched the order are collected from the logs
2. Exempt accounts are filtered out (Online Customer, autopay, Admin, etc.)
3. Of the remaining **known sales reps**:
   - **1 rep touched it** → 100% commission
   - **2 reps touched it** → 50/50 split
4. If your username is not in the list at all → order is skipped

Split orders are **flagged in the report** so you can verify before submitting.

**Exempt accounts** (configured in `.env`):
- `Online Customer` — self-service bookings
- `autopay` — automatic payment processing
- `Admin` — operations, not sales

---

## Unpaid Orders

Per Section 4 of the Commission Payment Policy, commission is only payable when the event is **fully paid**.

- Orders with a balance due are **included in the report** but highlighted in red
- No commission is calculated for unpaid orders
- This gives you a built-in follow-up list for outstanding balances

---

## Installation

### Requirements
- Python 3.11+
- pip

### Setup

```bash
# 1. Clone or download the project
cd ~/Dev/commission-calculator

# 2. Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Mac/Linux

# 3. Install dependencies
pip install requests beautifulsoup4 python-dotenv openpyxl reportlab

# 4. Configure environment
cp .env.example .env
nano .env  # fill in your credentials
```

### `.env` Configuration

```env
BASE_URL=https://freedomhoustonsouth.ourers.com
LOGIN_URL=https://freedomhoustonsouth.ourers.com/cp/login/
LIST_URL=https://freedomhoustonsouth.ourers.com/cp/events/
SITE_USERNAME=your_scraper_account_username
SITE_PASSWORD=your_scraper_account_password
MY_USERNAME=jeff.boerger
SALES_REPS=jeff.boerger,danielle.dirkse
EXEMPT_ACTIVATORS=Online Customer,autopay,Admin
```

> **Security note:** Never commit your `.env` file to Git. It is listed in `.gitignore` by default.
>
> Use a **dedicated scraper account** with read-only access — not your main admin account. This limits risk if credentials are ever compromised.

---

## Usage

### Activate the virtual environment first
```bash
cd ~/Dev/commission-calculator
source venv/bin/activate
```

### Default mode (interactive entry)
```bash
python3 commission_calculator.py
```

Enter order IDs one at a time. Type `q` when done.

```
Logging in...
Logged in.

Enter order IDs one at a time. Type 'q' or 'quit' when done.

Order ID (or q to finish): 2409
  Order       : 2409
  Event Date  : 2026-03-07
  Creator     : jeff.boerger
  Other Reps  : none
  Your Share  : 100%
  Paid        : $  207.79
  ...
  Your Comm   : $   17.45

Order ID (or q to finish): q

─────────────────────────────────────────────
  Rep                    : jeff.boerger
  Transactions processed : 1
  Total Sales (Comm Rev) : $174.50
  Your Total Commission  : $17.45
─────────────────────────────────────────────

Save as: (1) Excel  (2) PDF  (3) CSV  (4) All  (n) Don't save
Choice:
```

### Batch mode (file of order IDs)
```bash
python3 commission_calculator.py --batch orders.txt
```

`orders.txt` — one order ID per line:
```
2409
2364
2410
2402
```

### Month mode (coming soon)
```bash
python3 commission_calculator.py --month "March 2026"
```

> ⚠️ Requires Playwright setup — the ERS order list uses a JS-driven calendar filter. See **Future Development** below.

---

## Output Files

All files are saved to the current directory with this naming format:

```
jeff_commission_March_2026_20260412_1845.xlsx
jeff_commission_March_2026_20260412_1845.pdf
jeff_commission_March_2026_20260412_1845.csv
```

### Excel (.xlsx)
- Dark blue header row
- Alternating row colors
- Red highlighted rows for unpaid orders
- Commission total at the bottom
- Split/flag columns included to the right for reference

### PDF
- Landscape orientation
- Clean columns only (split/flag columns excluded)
- Red rows for unpaid orders
- Fits on one page for standard monthly reports
- Ready to attach and email

### CSV
- Plain text, importable into any spreadsheet
- Same column structure as Excel
- Split/flag columns included

---

## Report Columns

| Column | Description |
|--------|-------------|
| orderID | ERS transaction ID |
| username | Your username |
| status | PAID or UNPAID - Due: $X.XX |
| paid | Total amount paid by customer |
| paidTax | Tax collected |
| travelFee | Travel fee charged |
| surfaceFee | Surface fee charged |
| parkFee | Park/Business/Non-Residential fee |
| miscFee | Miscellaneous fees (holiday surcharges, etc.) |
| coupon | Coupon applied (negative) |
| discount | General discount applied (negative) |
| damageWaiver | Damage waiver fee (10% of subtotal) |
| subtotal | Base rental amount (read directly from ERS) |
| commRev | Commissionable revenue |
| Commission | Your commission (after split if applicable) |
| sharePct | Your share percentage (100% or 50%) |
| splitFlag | Split details or verification notes |
| otherReps | Other reps involved in the order |

---

## Project Structure

```
commission-calculator/
├── commission_calculator.py   # Main script
├── .env                       # Your credentials (never commit)
├── .env.example               # Template for new setups
├── .gitignore                 # Excludes .env, CSVs, venv
└── README.md                  # This file
```

---

## Security

- Credentials are stored in `.env` only — never hardcoded
- A dedicated read-only scraper account is used (not your main admin login)
- `.env` is excluded from Git via `.gitignore`
- The scraper only reads data — it makes no changes to orders

---

## Known Limitations

- **Month mode** requires Playwright (JS calendar) — not yet implemented
- **Year-end edge case**: event dates on new orders don't include the year (e.g. "Mar 14"), so the script assumes the current year. Orders booked in December for the following January may need manual verification
- **Surface fee row ID** (`ers_line_item_option_surface_fee`) has not been confirmed from a real order — update if surface fees are not being captured
- The script processes orders sequentially — large batches may take a few minutes

---

## Future Development

### Phase 1 — Polish (near term)
- [ ] Month mode via Playwright for automatic order discovery
- [ ] Email integration — send report directly from the app
- [ ] Streamlit web UI — browser-based interface, no terminal needed
- [ ] Auto-run on the 1st of each month for the prior month
- [ ] Audit log — record every run with timestamp and order count

### Phase 2 — Scale (medium term)
- [ ] Multi-user support — each rep runs their own report
- [ ] Manager dashboard — see all reps' commissions in one view
- [ ] Month-over-month comparison
- [ ] YTD running total
- [ ] Dispute flagging tab — mark orders for follow-up

### Phase 3 — Product (longer term)
- [ ] Package as a SaaS product for other ERS-platform party rental operators
- [ ] Per-seat subscription pricing ($19-29/month per rep)
- [ ] Onboarding flow — enter your ERS URL, credentials, and go
- [ ] Bundle with Employee Time Tracker (separate project) as a party rental back-office suite

---

## Related Projects

**Employee Time Tracker** — A companion tool in development for tracking employee clock-in/out shifts at the warehouse, with admin dashboard and CSV export for payroll. See `timetracker_spec.docx` for full spec.

---

## Built By

Jeff Boerger — General Manager, Freedom Fun Houston South  
April 2026

> *"Built by a party rental GM, for party rental operators."*
