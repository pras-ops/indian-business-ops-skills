# Tally data exchange — formats and a voucher skeleton

> Snapshot written October 2026. Tally's XML tags differ between **Tally Prime** and **Tally.ERP 9**
> and across releases. Validate against the target version, and import into a **test company**
> first. This is a structural guide, not a guaranteed-for-your-release schema.

## Export formats you'll receive

- **Day Book / Ledger / Trial Balance / GST reports** export to **Excel/CSV** (for reading) or
  **XML** (for machine processing). When reading Excel, map by the **header row**, not fixed column
  positions — layouts vary with the options chosen at export.
- Tally can also export masters (ledgers, stock items) to XML, which is the easiest way to learn the
  exact tag names your release uses: export one, read it, mirror it when importing.

## Import format: the XML envelope

Tally imports an `ENVELOPE` containing one or more `TALLYMESSAGE` blocks. Masters and vouchers use
different element types. **Import masters before vouchers.**

### A sales voucher skeleton (illustrative — verify tags for your release)

```xml
<ENVELOPE>
  <HEADER>
    <TALLYREQUEST>Import Data</TALLYREQUEST>
  </HEADER>
  <BODY>
    <IMPORTDATA>
      <REQUESTDESC>
        <REPORTNAME>Vouchers</REPORTNAME>
        <STATICVARIABLES>
          <SVCURRENTCOMPANY>Your Test Company</SVCURRENTCOMPANY>
        </STATICVARIABLES>
      </REQUESTDESC>
      <REQUESTDATA>
        <TALLYMESSAGE xmlns:UDF="TallyUDF">
          <VOUCHER VCHTYPE="Sales" ACTION="Create" OBJVIEW="Invoice Voucher View">
            <DATE>20260401</DATE>
            <VOUCHERTYPENAME>Sales</VOUCHERTYPENAME>
            <VOUCHERNUMBER>INV/0001</VOUCHERNUMBER>
            <PARTYLEDGERNAME>ABC Traders</PARTYLEDGERNAME>
            <PERSISTEDVIEW>Invoice Voucher View</PERSISTEDVIEW>

            <!-- Party: debit the receivable -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>ABC Traders</LEDGERNAME>
              <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
              <AMOUNT>-1180.00</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- Sales income -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Sales - Local</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>1000.00</AMOUNT>
            </ALLLEDGERENTRIES.LIST>

            <!-- GST: CGST + SGST for an intra-state sale (rate per gst-compliance) -->
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Output CGST</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>90.00</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
            <ALLLEDGERENTRIES.LIST>
              <LEDGERNAME>Output SGST</LEDGERNAME>
              <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
              <AMOUNT>90.00</AMOUNT>
            </ALLLEDGERENTRIES.LIST>
          </VOUCHER>
        </TALLYMESSAGE>
      </REQUESTDATA>
    </IMPORTDATA>
  </BODY>
</ENVELOPE>
```

Notes on the skeleton:

- **Dates** are `YYYYMMDD` with no separators.
- Debits and credits are signed amounts; in a sales voucher the party ledger is deemed positive
  (debit) and carries a negative `AMOUNT`, while income/tax ledgers are credits with positive
  amounts. The entries must **net to zero**.
- Every `LEDGERNAME` and `VOUCHERTYPENAME` must already exist in the company with that **exact**
  name, or the import creates duplicates / fails.
- For inter-state, replace CGST+SGST with a single **Output IGST** ledger.
- For an item-level invoice, add `ALLINVENTORYENTRIES.LIST` blocks (stock item, quantity, rate,
  amount) alongside the ledger entries.

## A safe import procedure

1. Export an existing voucher/master of the same type from the target company → read its exact tags.
2. Generate **one** voucher in that shape.
3. Import into a **test company**; open it in Tally and confirm the ledgers, amounts and GST are
   right.
4. Fix the mapping, then generate and import the full batch.
5. Reconcile imported totals against the source before trusting it.

## Mapping Tally → GST return (sales)

| GSTR-1 section | From Tally |
|---|---|
| B2B (invoice-wise) | Sales vouchers with a party GSTIN |
| B2C (summary) | Sales vouchers without a GSTIN, summarised by rate/place |
| HSN summary | Stock-item / ledger HSN totals by rate |
| Credit/Debit notes | Credit note / debit note vouchers |

Flag any sales row missing a GSTIN (for B2B) or an HSN/SAC before building the return.

## Official source

- Tally Solutions documentation: https://help.tallysolutions.com
