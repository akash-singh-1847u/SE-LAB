# Lab 3: Component Modelling and Architectural Pattern Selection

**SRN:** PES2UG24CS042
**Problem Statement:** #38 - Dropshipping Inventory & Order Orchestrator
**Domain:** Retail, E-Commerce & Finance
**Course:** Software Engineering, Dept. of CSE, PES University

---

## Architecture selected

Microservices. Six components sit inside the DIOO boundary, each deployed on its own and reached only through a published interface. The full argument is in the justification document.

Short version: NFR-001 wants the storefront webhook answered in under 200 ms, and NFR-002 wants a failed supplier call retried three times with 30 seconds between attempts. Those two live on very different clocks, so the webhook edge and the supplier retry loop are separate services.

## Components

| Component | Responsibility | Lab 1 requirements |
|---|---|---|
| Storefront Gateway | Webhook intake, HMAC check, HTTP 200 reply, tracking write back | FR-001, FR-004, NFR-001 |
| Order Manager | Order state machine, splits an order into sub-orders | FR-001, FR-002, NFR-002 |
| Supplier Integration | Stock calls, purchase orders, 3 retries at 30 s, tracking intake | FR-001, FR-004, NFR-002 |
| Inventory and SKU Map | Supplier SKU map, stock counts, sub-order records | FR-002, UC-08 |
| Payment Service | Supplier settlement and customer refunds | FR-003 hold path |
| Owner Dashboard and Alerts | Order view, on hold alert within one minute | FR-003, FR-005 |

Order Manager and Payment Service are the two components fixed by the lab handout. The customer pays on the storefront before the webhook arrives, so in DIOO the Payment Service covers supplier settlement and the refund the owner issues when a sub-order cannot be filled.

## Interfaces

| Interface | Provided by | Required by | Transport |
|---|---|---|---|
| IWebhookIntake | Storefront Gateway | Storefront Platform (public port) | HTTPS, HMAC verified |
| IOwnerConsole | Owner Dashboard and Alerts | E-Store Owner (public port) | HTTPS, browser |
| IOrderIntake | Order Manager | Storefront Gateway | Queued, internal |
| IStockCheck | Supplier Integration | Order Manager | REST over HTTPS |
| IPurchaseOrder | Supplier Integration | Order Manager | REST over HTTPS |
| ITrackingWriteBack | Storefront Gateway | Supplier Integration | Internal REST |
| ISkuLookup | Inventory and SKU Map | Order Manager | Read, cached |
| ISkuMapAdmin | Inventory and SKU Map | Owner Dashboard and Alerts | Read and write |
| IOrderStatus | Order Manager | Owner Dashboard and Alerts | Read, plus hold events |
| IPaymentOps | Payment Service | Order Manager | Settle, refund |

## External systems

The four Lab 1 actors sit outside the boundary and are reached through `<<use>>` dependencies: Storefront Platform (posts the order webhook, receives the tracking write back), Supplier Partner Systems (stock, purchase orders, tracking), Courier Service (shipment status), and the Payment Gateway used for settlement and refunds. The E-Store Owner works through IOwnerConsole.

## Files in this repo

| File | Deliverable |
|---|---|
| `DIOO_Lab3_Submission_PES2UG24CS042.pdf` | Both deliverables in one PDF. Page 1 diagram, page 2 justification |
| `DIOO_Lab3_ComponentDiagram_PES2UG24CS042.png` | Component diagram, PNG at 150 dpi |
| `DIOO_Lab3_ComponentDiagram_PES2UG24CS042.pdf` | Same diagram as vector PDF |
| `DIOO_Lab3_ComponentDiagram_PES2UG24CS042.drawio` | Editable source. Open with File > Open From > Device in draw.io |
| `DIOO_Lab3_Justification_PES2UG24CS042.docx` | Written justification, editable |
| `DIOO_Lab3_Justification_PES2UG24CS042.pdf` | Written justification, one page, for submission |

## Notation used

Ball for a provided interface, socket for a required interface, a ball sitting inside a socket for an assembly connector between two components, small squares for ports on the component boundary, and dashed arrows with `<<use>>` for calls to systems outside DIOO. A ball on the boundary with no socket is a public port, used from outside the system.
