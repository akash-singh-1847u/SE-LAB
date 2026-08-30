# Lab 1: Requirements Engineering and UML Use-Case Modelling

**SRN:** PES2UG24CS042
**Problem Statement:** #38 - Dropshipping Inventory & Order Orchestrator
**Domain:** Retail, E-Commerce & Finance
**Course:** Software Engineering, Dept. of CSE, PES University

---

## Scenario

An e-commerce backend for a dropshipping store. It reads order webhooks from the storefront, checks stock with the supplier API in real time, splits an order that has items from more than one supplier, sends a purchase order to each supplier, and keeps the tracking numbers up to date.

## Actors

| Actor | Role |
|---|---|
| E-Store Owner | Owns the store, watches orders, and fixes items that are on hold. |
| Supplier Partner | Gives stock counts, accepts purchase orders, returns tracking numbers. |
| Storefront Platform | Shopify or WooCommerce. Sends the order webhook to the system. |
| Courier Service | Gives the shipment status for a tracking number. |

## Files in this repo

| File | Deliverable |
|---|---|
| `01_Requirements_Table.docx` / `.pdf` | 5 FRs, 2 NFRs, plus the actor and use case list |
| `02_Use_Case_Diagram.pdf` | UML use-case diagram, exported as PDF |
| `02_Use_Case_Diagram.drawio` | Editable source. Open with File > Open From > Device in draw.io |
| `03_Use_Case_Flow.docx` / `.pdf` | One-page flow for UC-01 with preconditions, postconditions, main success scenario, and one alternate flow |

## Requirements at a glance

| ID | Type | Short description | Priority |
|---|---|---|---|
| FR-001 | Functional | Read order webhook, check supplier stock, send purchase order | High |
| FR-002 | Functional | Split a multi-supplier order into one sub-order per supplier | High |
| FR-003 | Functional | Hold the sub-order and alert the owner when stock is zero | High |
| FR-004 | Functional | Save the tracking number and write it back to the storefront | Medium |
| FR-005 | Functional | Show the owner a dashboard of orders, statuses, and tracking | Medium |
| NFR-001 | Performance & Security | Reply HTTP 200 within 200 ms, only after HMAC check | High |
| NFR-002 | Reliability | Retry a failed supplier API call 3 times, never drop an order | High |

## Use cases

| ID | Use case | Actor |
|---|---|---|
| UC-01 | Process Storefront Order | Storefront Platform |
| UC-02 | Check Supplier Stock | Supplier Partner |
| UC-03 | Split Multi-Vendor Order | E-Store Owner |
| UC-04 | Send Supplier Purchase Order | Supplier Partner |
| UC-05 | Update Tracking Number | Supplier Partner, Courier Service |
| UC-06 | View Order Dashboard | E-Store Owner |
| UC-07 | Flag Out of Stock Item | System, seen by E-Store Owner |
| UC-08 | Manage Supplier SKU Map | E-Store Owner |

## Include and extend relationships

- UC-01 «include» UC-02 - every order run always checks supplier stock.
- UC-01 «include» UC-04 - every order run always sends a purchase order.
- UC-03 «extend» UC-01 - splitting runs only when the order has more than one supplier.
- UC-07 «extend» UC-02 - flagging runs only when the stock count comes back as zero.

Include is used for behaviour that always runs. Extend is used for behaviour that runs only under a condition.
