# Enterprise ERP Data Analytics & Automation
# Logistics ERP Analytics — End-to-End Project Report

## 1. Executive Summary

This project is an end-to-end **Enterprise Logistics ERP Analytics Implementation** developed for a USA-based logistics and supply-chain organization.

The organization migrated data from multiple legacy ERP systems into a centralized Logistics ERP. After migration, management identified inconsistencies between operational, finance, inventory, procurement, warehouse, and shipment reports.

The objective of this project was to create a **reliable, governed, scalable, and analytics-ready enterprise data platform** that could support operational reporting, executive decision-making, predictive analytics, and process automation.

The project covers 10 major phases:

1. Enterprise Data Audit & Governance
2. Enterprise ETL & Data Engineering
3. Enterprise Data Warehouse Design
4. Advanced SQL Engineering
5. Advanced DAX & KPI Development
6. Executive Power BI Solution
7. Predictive & Prescriptive Analytics
8. Business Problem Solving
9. Automation & DevOps
10. Executive Documentation

The source dataset contains **3,500 records and 65 columns**, covering customers, products, suppliers, inventory, procurement, orders, warehouse operations, shipments, couriers, and delivery information.

---

# 2. Business Problem

The company was facing several challenges after consolidating data from different legacy ERP systems.

### Major business problems

* Different departments were using inconsistent reports.
* Customer, product, supplier, and SKU information required standardization.
* Duplicate and potentially duplicated transaction identifiers existed.
* Shipment and delivery information contained data-quality exceptions.
* Inventory reports required reconciliation.
* Finance and operational reports had inconsistent calculations.
* Management lacked a centralized KPI framework.
* Manual reporting created dependency on analysts.
* There was no unified executive dashboard.
* Historical and future-oriented analytics were limited.
* Data-quality issues were not systematically monitored.
* ETL processes required better logging and error handling.

The project therefore focused on creating a **single source of analytical truth**.

---

# 3. Project Objectives

The main objectives were:

* Audit ERP data quality.
* Identify duplicates, missing values, inconsistencies, and anomalies.
* Establish data governance standards.
* Standardize master data.
* Build a scalable ETL pipeline.
* Design an enterprise data warehouse.
* Develop reusable SQL queries.
* Build enterprise DAX measures.
* Create executive Power BI dashboards.
* Implement advanced analytics.
* Develop forecasting and optimization use cases.
* Provide evidence-based solutions to business problems.
* Automate refresh and monitoring processes.
* Implement logging and auditability.
* Establish version-control practices.
* Prepare complete technical and business documentation.

---

# 4. Dataset Overview

The actual ERP dataset inspected contains:

* **Rows:** 3,500
* **Columns:** 65
* **Distinct Product IDs:** 3,500
* **Distinct SKUs:** 3,500
* **Distinct Customer IDs:** 10
* **Distinct Suppliers:** 12
* **Multiple warehouses**
* **Multiple couriers**
* **Multiple product categories**
* **Multiple shipment statuses**

### Major data domains

### Customer Data

* Customer ID
* Customer Code
* Company Name
* Contact Person
* Email
* Phone
* City
* State
* Country

### Product Data

* Product ID
* SKU
* Product Name
* Product Category
* Unit of Measure
* Unit Price
* Weight
* Dimensions
* CBM

### Inventory Data

* Stock ID
* Warehouse
* Opening Date
* Opening Quantity
* Opening Value
* GRN Number
* Supplier
* Received Quantity
* Unit Cost
* Batch Number
* Expiry Date

### Order Data

* Order ID
* Order Date
* PO Number
* Order Quantity
* Order Value
* Pick List Number
* Picked Quantity
* Packed Quantity
* Packed By
* Packed Date

### Shipment Data

* Shipment ID
* Tracking Number
* Courier
* Vehicle Number
* Dispatch Date
* Expected Delivery
* Delivered Date
* Shipment Status

### Inventory Movement

* Issued Quantity
* Adjustment Quantity
* Closing Quantity

---

# 5. Overall Solution Architecture

The proposed solution follows a layered enterprise analytics architecture.

**Source ERP / Excel**

↓

**Power Query Extraction**

↓

**Data Cleaning & Transformation**

↓

**Data Validation**

↓

**MySQL Staging**

↓

**Clean Data Layer**

↓

**Dimensional Data Warehouse**

↓

**Power BI Semantic Model**

↓

**DAX KPI Layer**

↓

**Executive Dashboards**

↓

**Predictive & Prescriptive Analytics**

↓

**Automation, Monitoring & Alerts**

---

# 6. Phase 1 — Enterprise Data Audit & Governance

The first phase focused on understanding the quality, structure, ownership, and reliability of the ERP data.

## 6.1 Data Quality Assessment

The following observations were identified from the actual dataset.

### Missing Delivered Dates

Approximately **1,531 records** do not have a Delivered Date.

This represents approximately **43.7% of the dataset**.

However, missing Delivered Dates should not automatically be classified as data errors because many of these records correspond to shipments that are still:

* In Transit
* Out for Delivery
* Pending Dispatch

Therefore, the correct approach is to validate the Delivered Date against Shipment Status.

---

## 6.2 Duplicate Analysis

The following repeated identifiers were identified:

* **7 repeated Order IDs**
* **2 repeated PO Numbers**
* **2 repeated Shipment IDs**

These should not immediately be deleted.

The first step should be to determine the intended grain:

* Order header
* Order line
* Shipment event
* Purchase order line
* Transaction

If multiple rows represent legitimate transaction lines, repetition may be expected.

---

## 6.3 Customer Master Analysis

Only **10 distinct Customer IDs** exist across 3,500 transaction records.

This is not necessarily a data-quality problem.

Customer IDs naturally repeat across multiple:

* Orders
* Shipments
* Transactions
* Inventory activities

Therefore, uniqueness should be enforced inside the **Customer Dimension**, rather than in the raw transaction table.

---

## 6.4 Delivery-Date Validation

Approximately **296 records** contain:

> Delivered Date < Dispatch Date

This represents a temporal data-quality issue.

Possible causes include:

* Incorrect source-system entry
* Date-format conversion
* Time-zone differences
* Historical migration issues
* Incorrect mapping between shipment events

These records should be flagged for reconciliation.

---

## 6.5 Financial Data Validation

One of the most important findings was:

**Order Value ≈ Unit Cost × Order Quantity**

This causes calculated:

**Profit ≈ 0**

Therefore, the financial model requires validation.

Possible explanations include:

* Unit Cost actually represents selling price.
* Order Value was generated using cost rather than revenue.
* Freight/tax/discount information is missing.
* The source dataset is synthetic.
* Financial definitions were not correctly mapped.

This should be resolved before using calculated Profit or Margin as a production financial KPI.

---

# 7. Data Governance Framework

A governance framework was designed around:

### Data Ownership

* Customer → Sales
* Product → Inventory
* Supplier → Procurement
* Warehouse → Operations

### Data Classification

Sensitive/internal information includes:

* Customer information
* Revenue
* SKU
* Warehouse information

### Data Retention

Examples include:

* Orders → 7 years
* Inventory → 5 years
* Payments → 7 years

### Access Roles

* CEO
* Manager
* Analyst
* Administrator

---

# 8. Master Data Standardization

Standardization rules include:

* Trim unnecessary spaces.
* Standardize customer names.
* Standardize supplier names.
* Convert SKU values to uppercase.
* Remove unnecessary SKU formatting.
* Standardize date formats.
* Validate emails.
* Validate phone numbers.
* Validate shipment statuses.
* Validate reference data.
* Enforce master-data uniqueness.

---

# 9. Validation Rule Repository

The project includes a validation framework containing approximately 30 business rules.

Examples:

### Customer

Customer ID cannot be NULL.

### Product

SKU must be unique.

### Financial

Revenue must be greater than zero.

### Date

Shipment Date must not be earlier than Order Date.

### Inventory

Closing Quantity should not be negative.

### Supplier

Supplier must exist in Supplier Master.

### Shipment

Shipment Status must belong to an approved status list.

### Referential Integrity

Foreign keys must exist in their corresponding dimensions.

---

# 10. Phase 2 — Enterprise ETL & Data Engineering

The ETL framework was designed using **Power Query, MySQL, Power BI, and validation logic**.

## ETL Process

### Step 1 — Source Extraction

Extract ERP data from Excel/source systems.

### Step 2 — Parameterization

Use dynamic source parameters instead of hard-coded paths.

### Step 3 — Staging

Create staging queries such as:

* stg_customer
* stg_product
* stg_orders
* stg_shipments
* stg_inventory

### Step 4 — Transformation

Transform:

* Dates
* Text
* IDs
* Quantities
* Categories
* Statuses

### Step 5 — Validation

Apply:

* Null checks
* Duplicate checks
* Referential integrity
* Date checks
* Financial checks
* Inventory checks

### Step 6 — Clean Layer

Create validated datasets.

### Step 7 — Warehouse Loading

Load the clean data into dimensional tables.

### Step 8 — Power BI

Connect the semantic model to the warehouse.

---

# 11. ETL Logging

Two major logging mechanisms were designed.

## Error Log

Captures:

* Table
* Column
* Error Type
* Error Message
* Timestamp

## Audit Log

Captures:

* Process Name
* Start Time
* End Time
* Status
* Records Processed

This provides traceability and operational monitoring.

---

# 12. Incremental Refresh

Incremental refresh was designed using:

* RangeStart
* RangeEnd

Instead of refreshing the complete dataset every time, only recent data is refreshed while historical data remains stored.

Benefits:

* Faster refresh
* Lower resource consumption
* Better scalability
* Improved Power BI performance

---

# 13. Phase 3 — Enterprise Data Warehouse

The project follows a dimensional data warehouse approach.

## Fact Tables

Major fact tables include:

### Fact Sales Orders

Contains sales/order transactions.

### Fact Purchase Orders

Contains procurement transactions.

### Fact Shipments

Contains shipment events.

### Fact Inventory Movements

Contains inventory movement.

### Fact Returns

Contains return transactions.

### Fact Goods Receipt

Contains received goods.

### Fact Payments

Contains payment transactions.

### Fact Warehouse Operations

Contains warehouse activity.

---

# 14. Dimension Tables

Major dimensions include:

* Dim Customer
* Dim Product
* Dim Supplier
* Dim Employee
* Dim Warehouse
* Dim Courier
* Dim Geography
* Dim Calendar
* Dim Currency
* Dim Sales Territory

---

# 15. Star Schema

The Star Schema provides:

* Simple relationships
* Faster reporting
* Easier DAX
* Better Power BI usability
* Clear business grain

The model separates:

**Facts = measurable business events**

from

**Dimensions = descriptive business context**

---

# 16. Snowflake Schema

The project also documents Snowflake modeling for cases where dimensions need further normalization.

For example:

Product → Category → Product Group

or:

Customer → City → State → Country

The Snowflake approach reduces redundancy but may increase relationship complexity.

---

# 17. Slowly Changing Dimensions

The project documents **SCD Type 2**.

SCD Type 2 preserves historical changes.

Example:

If a customer moves from:

Delhi → Mumbai

the system retains the previous record and creates a new effective record.

Typical fields:

* Effective Start Date
* Effective End Date
* Current Flag

This allows historical reporting to use the correct customer attributes for each transaction period.

---

# 18. Phase 4 — Advanced SQL Engineering

The SQL phase contains advanced analytical and performance concepts.

## SQL Techniques

### JOINs

Used for:

* Customers
* Orders
* Products
* Suppliers
* Warehouses
* Shipments

### CTEs

Common Table Expressions were used for multi-step analytical queries.

### Window Functions

Used for:

* Ranking
* Running totals
* Customer analysis
* Product ranking
* Supplier comparisons

### Aggregations

Used for:

* Revenue
* Quantity
* Cost
* Inventory
* Delivery performance

### Dynamic SQL

Used for parameterized query generation.

---

# 19. SQL Performance Optimization

Optimization techniques include:

* Avoiding SELECT *
* Filtering early
* Reducing unnecessary joins
* Creating appropriate indexes
* Reviewing execution plans
* Maintaining statistics
* Using covering indexes
* Partitioning large tables
* Monitoring locks
* Preventing deadlocks

Execution plans were considered to identify:

* Table scans
* Index scans
* Expensive joins
* High-cost operators

---

# 20. Phase 5 — Advanced DAX & KPI Development

A centralized KPI library was developed.

## Financial KPIs

### Gross Revenue

**Gross Revenue = SUM(Order Value)**

### Net Revenue

The submitted design uses a 10% assumed adjustment.

For production implementation, this should be replaced with actual:

* Discount
* Tax
* Freight
* Returns

data.

### Profit

**Profit = Revenue − Cost**

### Margin %

**Margin % = Profit / Revenue**

### Cost-to-Revenue Ratio

**Cost-to-Revenue = Cost / Revenue**

---

# 21. Customer KPIs

Important customer analytics include:

### Recency

Days since the customer's latest transaction.

### Frequency

Number of transactions/orders.

### Monetary Value

Total customer revenue.

### Churn Flag

Customers exceeding a defined inactivity period can be flagged.

---

# 22. Inventory KPIs

### Inventory Aging

Measures how long inventory has remained in stock.

### Inventory Velocity

Measures how quickly inventory is consumed.

Other important inventory KPIs include:

* Opening Stock
* Closing Stock
* Received Quantity
* Issued Quantity
* Stock Value
* Stock-out Rate
* Overstock Rate

---

# 23. Logistics KPIs

### On-Time Delivery %

Measures shipments delivered on or before the expected delivery date.

### Delivery Time

Measures:

**Delivered Date − Dispatch Date**

Other KPIs:

* Total Shipments
* Delayed Shipments
* Average Delivery Time
* Courier Performance
* SLA Compliance

---

# 24. Phase 6 — Executive Power BI Solution

Ten dashboards were designed.

## 1. CEO Dashboard

Focus:

* Revenue
* Profit
* Orders
* Growth
* Strategic KPIs
* Risk

## 2. CFO Dashboard

Focus:

* Revenue
* Cost
* Profit
* Margin
* Financial variance

## 3. COO Dashboard

Focus:

* Orders
* Fulfillment
* Delivery
* Operational efficiency

## 4. Warehouse Dashboard

Focus:

* Inventory
* Stock aging
* Warehouse utilization
* Low-stock items

## 5. Procurement Dashboard

Focus:

* Supplier performance
* Procurement cost
* Lead time
* Supplier risk

## 6. Sales Dashboard

Focus:

* Revenue
* Customers
* Categories
* Products
* Sales trends

## 7. Logistics Dashboard

Focus:

* Shipments
* Delivery performance
* Courier performance
* SLA

## 8. Inventory Dashboard

Focus:

* Stock
* Demand
* Inventory turnover
* Forecasting

## 9. Risk Dashboard

Focus:

* Supplier risk
* Delivery risk
* Stock-out risk
* Operational anomalies

## 10. Executive Summary

Combines the most important enterprise KPIs.

---

# 25. Advanced Power BI Features

The project includes documentation for:

* Drill-through
* Drill-down
* Bookmarks
* Dynamic tooltips
* Dynamic titles
* Field parameters
* Calculation groups
* Row-Level Security
* Incremental refresh
* Composite models
* Dynamic measure selection
* Dynamic currency conversion
* Scenario analysis

These capabilities make the solution more suitable for enterprise reporting rather than a static dashboard.

---

# 26. Phase 7 — Predictive Analytics

The predictive analytics phase extends reporting beyond historical analysis.

## Time-Series Forecasting

Used to estimate future trends in:

* Orders
* Revenue
* Shipments
* Demand

## Demand Forecasting

Predict future demand by:

* Product
* SKU
* Customer
* Category

## Inventory Forecasting

Predict future inventory requirements using:

* Historical demand
* Consumption
* Lead time
* Safety stock

---

# 27. Customer Segmentation

Customers can be segmented using:

* Revenue
* Frequency
* Recency
* Order volume

A typical analytical approach is RFM-based segmentation.

This helps identify:

* High-value customers
* Regular customers
* Inactive customers
* Low-value customers

---

# 28. Supplier Risk Prediction

Supplier risk can be evaluated using:

* Delivery delays
* Lead time
* Cost variation
* Defect/quality issues
* Order fulfillment performance

Suppliers can then be monitored through a risk score.

---

# 29. Stock-Out Prediction

Stock-out risk can be calculated using:

* Current stock
* Average consumption
* Demand forecast
* Supplier lead time

This helps determine which products may run out before replenishment arrives.

---

# 30. Overstock Prediction

Overstock analysis identifies:

* High stock
* Low demand
* Slow-moving products
* Excess inventory

Possible actions:

* Reduce future procurement
* Clearance
* Bundling
* Promotional sales
* Inventory redistribution

---

# 31. ABC-XYZ Analysis

ABC analysis classifies inventory according to value.

XYZ analysis classifies inventory according to demand variability.

Combining them creates:

* AX
* AY
* AZ
* BX
* BY
* BZ
* CX
* CY
* CZ

This provides a stronger inventory-management framework.

---

# 32. EOQ Optimization

Economic Order Quantity determines an optimal order quantity based on:

* Ordering cost
* Holding cost
* Demand

The objective is to balance inventory carrying cost with ordering cost.

---

# 33. Safety Stock Optimization

Safety stock protects against:

* Demand variability
* Supplier delays
* Lead-time uncertainty

The model can use demand standard deviation and supplier lead time to estimate required safety inventory.

---

# 34. Phase 8 — Business Problem Solving

The project converts analytical findings into business recommendations.

## Problem: Inventory increasing while sales remain flat

Potential analysis:

* Demand trend
* Procurement quantity
* Inventory aging
* Stock turnover

Possible actions:

* Reduce unnecessary procurement
* Improve demand forecasting
* Liquidate slow-moving inventory

---

## Problem: High-revenue but low-margin products

Analyze:

* Unit cost
* Selling price
* Freight
* Discounts
* Supplier cost

The company can then review pricing and sourcing strategies.

---

## Problem: Uneven warehouse utilization

Analyze:

* Inventory by warehouse
* Warehouse capacity
* Product movement
* Regional demand

Potential action:

Redistribute inventory based on demand.

---

## Problem: Supplier cost and reliability

Supplier evaluation should consider:

* Purchase price
* Lead time
* Delays
* Quality
* Logistics cost

This creates a Total Cost of Ownership approach.

---

## Problem: Delayed deliveries

Analyze:

* Courier
* Route
* Warehouse
* Dispatch timing
* Expected delivery
* Actual delivery

This allows SLA monitoring.

---

# 35. Phase 9 — Automation & DevOps

Automation capabilities include:

* Scheduled refresh
* Incremental refresh
* Data validation
* Error logging
* Audit logging
* Reconciliation
* Execution history
* Rollback procedures
* Version control

---

# 36. Git Version Control

The project includes Git-based version control.

The general workflow is:

**Modify → Test → Stage → Commit → Push**

Benefits:

* Change tracking
* Version history
* Collaboration
* Backup
* Rollback
* Controlled development

For production, the workflow can be extended to:

**Development → Testing/UAT → Production**

with controlled releases.

---

# 37. Phase 10 — Executive Documentation

The project contains a complete documentation framework.

Major documents include:

### BRD

Business Requirement Document.

### FSD

Functional Specification Document.

### TDD

Technical Design Document.

### Data Dictionary

Documents:

* Column names
* Definitions
* Data types
* Business meanings

### Data Governance Guide

Defines:

* Ownership
* Access
* Classification
* Retention
* Quality rules

### KPI Catalog

Defines:

* KPI
* Formula
* Business meaning
* Data source
* Frequency

### ETL Documentation

Explains the complete pipeline.

### SQL Documentation

Contains analytical queries and optimization guidance.

### Power BI User Guide

Explains dashboard usage and navigation.

---

# 38. Important Dataset Findings

The actual data inspection produced several important findings.

### Finding 1 — Dataset Size

**3,500 rows × 65 columns**

This is a relatively wide ERP transaction extract.

### Finding 2 — Delivery Data

**1,531 records have no Delivered Date.**

This requires status-based interpretation.

### Finding 3 — Delivery-Date Errors

**296 records have Delivered Date earlier than Dispatch Date.**

These should be investigated.

### Finding 4 — Repeated Order IDs

**7 repeated Order IDs**

These require grain analysis before being classified as duplicates.

### Finding 5 — Repeated PO Numbers

**2 repeated PO Numbers**

Requires validation against PO line/header structure.

### Finding 6 — Repeated Shipment IDs

**2 repeated Shipment IDs**

Requires shipment-grain investigation.

### Finding 7 — Financial Modeling Issue

Order Value is approximately equal to:

**Unit Cost × Order Quantity**

Therefore:

**Calculated Profit ≈ 0**

This is the most important financial-model validation issue.

---

# 39. Data Reconciliation Framework

The production solution should perform reconciliation at multiple levels.

## Source vs Target

Compare:

* Row count
* Revenue
* Quantity
* Cost
* Shipment count

## Inventory Reconciliation

Expected:

**Opening Stock + Received − Issued ± Adjustments = Closing Stock**

## Financial Reconciliation

Compare:

**Source Revenue vs Warehouse Revenue vs Power BI Revenue**

## Shipment Reconciliation

Compare:

**ERP Shipments vs Warehouse Shipments vs Power BI Shipments**

---

# 40. Recommended Production Improvements

The following improvements should be implemented before production deployment.

### 1. Clearly define fact-table grain

Every fact table should explicitly define whether one row represents:

* Order
* Order line
* Shipment
* Shipment event
* Inventory movement
* Purchase-order line

### 2. Separate master and transaction data

Create dedicated:

* Customer Master
* Product Master
* Supplier Master
* Warehouse Master
* Courier Master

### 3. Resolve delivery-date anomalies

Investigate the 296 records where:

**Delivered Date < Dispatch Date**

### 4. Investigate repeated identifiers

Review repeated:

* Order IDs
* PO Numbers
* Shipment IDs

### 5. Validate financial definitions

Confirm whether:

**Unit Cost × Quantity = Cost**

and whether:

**Order Value = Revenue**

### 6. Replace assumed financial adjustments

The 10% Net Revenue adjustment should be replaced with actual:

* Discounts
* Taxes
* Returns
* Freight

### 7. Strengthen automated data-quality monitoring

Create a daily data-quality scorecard.

### 8. Establish deployment environments

Use:

**Development → UAT → Production**

### 9. Implement automated testing

Validate:

* Schema
* Null rate
* Duplicate rate
* Referential integrity
* KPI reconciliation

### 10. Strengthen security

Use:

* Power BI RLS
* Least-privilege access
* Sensitive-field protection

---

# 41. Technology Stack

## Data & Programming

* Python
* SQL
* MySQL

## ETL

* Power Query
* Power BI
* MySQL

## Business Intelligence

* Power BI
* DAX

## Data Warehouse

* Star Schema
* Snowflake Schema
* SCD Type 2

## Advanced Analytics

* Forecasting
* Segmentation
* Optimization
* Risk analysis

## DevOps

* Git
* Version Control
* Logging
* Monitoring
* Refresh automation

---

# 42. Skills Demonstrated

This project demonstrates practical experience in:

* Data Analysis
* Data Cleaning
* Data Quality
* Data Governance
* SQL
* Advanced SQL
* MySQL
* Power Query
* ETL
* Data Warehousing
* Dimensional Modeling
* Star Schema
* Snowflake Schema
* SCD Type 2
* Power BI
* DAX
* KPI Development
* Dashboard Development
* Predictive Analytics
* Prescriptive Analytics
* Forecasting
* Inventory Analytics
* Logistics Analytics
* Procurement Analytics
* Customer Analytics
* Business Analysis
* DevOps
* Git
* Documentation

---

# 43. Final Project Conclusion

The Logistics ERP Analytics project represents a complete **enterprise data and analytics lifecycle**.

The project starts with raw ERP data and progresses through:

**Data Audit → Governance → ETL → Data Warehouse → SQL → DAX → Power BI → Predictive Analytics → Business Solutions → Automation → Documentation**

The implementation addresses both technical and business requirements.

From a technical perspective, it demonstrates the ability to build:

* Data-quality frameworks
* ETL pipelines
* Dimensional data warehouses
* SQL analytics
* DAX KPI libraries
* Power BI dashboards
* Predictive models
* Automation frameworks

From a business perspective, it provides analytics for:

* Finance
* Sales
* Procurement
* Warehouse
* Inventory
* Logistics
* Operations
* Executive management

The actual dataset analysis also identified important areas requiring validation before production use, particularly the **delivery-date anomalies, repeated transaction identifiers, master-vs-transaction grain, and financial calculation logic**.

Overall, the project demonstrates an end-to-end **Senior Data Analyst / Analytics Engineer capability**, connecting raw enterprise data with governed analytical models, executive reporting, predictive analytics, and business decision support.
