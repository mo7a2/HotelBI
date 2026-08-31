# Hotel Revenue and Guest Insights Dashboard

---

## Authors

**Mohammed Abudagga**  
202210006  

**Supervised by:** Dr. Wasef Matar  
**Course:** 307498 – Graduation Project  
**Semester:** First Semester, 2025/2027  
**Year:** 2026  

---

## Table of Contents

*   [Abstract](#abstract)
*   [Acknowledgment](#acknowledgment)
*   [Business Intelligence Project Description and Objectives](#business-intelligence-project-description-and-objectives)
*   [Data Research and Acquiring Effort](#data-research-and-acquiring-effort)
*   [Links to Raw Data](#links-to-raw-data)
*   [Data Description and Understandings](#data-description-and-understandings)
*   [Data Primary Cleaning and Transformation](#data-primary-cleaning-and-transformation)
*   [Python Libraries and Backend Implementation](#python-libraries-and-backend-implementation)
*   [Data Visualization and Insights](#data-visualization-and-insights)
*   [Advanced Analytics and AI Modeling](#advanced-analytics-and-ai-modeling)
*   [Data Analytics and Business Intelligence Functions](#data-analytics-and-business-intelligence-functions)
*   [Tools Research and Selection Effort](#tools-research-and-selection-effort)
*   [HTML and Frontend Implementation](#html-and-frontend-implementation)
*   [Project Deployment Effort – Use Case](#project-deployment-effort--use-case)
*   [Results](#results)
*   [References](#references)

---

## <a id="abstract"></a>Abstract

Independent hotels with roughly ten to one hundred rooms generate booking and guest data through reservation systems and online travel agencies, but many small properties still lack an affordable and understandable way to turn that data into pricing, occupancy, and channel decisions. The **Hotel Revenue and Guest Insights Dashboard** addresses this gap through a web-based prototype designed specifically for independent hotel managers.

The project uses the supplied Hotel Booking Demand dataset for development and exploratory analysis. The prototype workflow accepts a booking CSV, validates the required fields, applies the intended cleaning and standardization steps, and presents hotel-specific dashboard modules for revenue and occupancy, booking channels, guest behavior, room status, competitor pricing, short-term forecasts, alerts, exports, upload history, and subscription management. The analytics approach is deliberately explainable: alerts are rule-based and the forecast is based on simple moving averages rather than a black-box machine-learning model.

The result is a working front-end demonstration that shows how a hotel manager can move from booking data to a clear operational view in a small number of steps. The prototype demonstrates the intended user experience and business logic, while the current documented limitations remain: no persistent backend/database, illustrative occupancy values on the main dashboard, manual competitor-rate entry, and moving-average forecasting intended for a short 7-14 day window.

---

## <a id="acknowledgment"></a>Acknowledgment

I would like to thank my supervisor, **Dr. Wasef Matar**, for his guidance and honest feedback throughout the development of this project. His questions about who would actually pay for this and why pushed me to rethink parts of the business model I had originally taken for granted, and the project is stronger for it.

I am also grateful to the **Faculty of Administrative and Financial Sciences at the University of Petra** for the resources and support that made this project possible, and to the independent hotel managers and industry contacts who took the time to discuss how they currently handle pricing and booking data. Their input shaped how I approached this problem.

---

## <a id="business-intelligence-project-description-and-objectives"></a>Business Intelligence Project Description and Objectives

**HotelBI** is a web-based business intelligence prototype for independent hotel owners and managers, especially properties with roughly 10-100 rooms and no dedicated analytics team. The business problem is not a lack of booking data; it is the lack of an affordable and simple way to interpret that data. The project so focuses on turning a booking CSV export into hotel-specific insights that can be understood without a technical background.

The project objectives documented and implemented in the prototype are:

*   Provide a CSV upload workflow for hotel booking data and clearly identify required and optional fields.
*   Apply an ETL preparation process that validates files, removes duplicate rows, standardizes date formats, and standardizes booking-channel values.
*   Present core hotel performance views including occupancy, Average Daily Rate (ADR), Revenue per Available Room (RevPAR), and booking-channel mix.
*   Show guest behavior measures including repeat guest rate, booking lead time, and cancellation rate.
*   Provide room-status, competitor-pricing, forecasting, alerts/recommendations, export, upload-history, and profile/subscription screens.
*   Keep alerts explainable through configurable thresholds instead of relying on a black-box prediction model.
*   Support a 7-14 day short-term forecasting use case using a simple moving-average approach in the current prototype.

---

## <a id="data-research-and-acquiring-effort"></a>Data Research and Acquiring Effort

The project required a hotel-booking dataset containing fields that could support the same business questions represented in HotelBI: booking status, arrival dates, stay duration, rate, distribution channel, guest country, repeat-guest status, room type, lead time, and cancellation behavior. The supplied development dataset is the **Hotel Booking Demand dataset by Jesse Mostipak on Kaggle**. It contains 119,390 rows and 32 source columns and was used for development, testing, and exploratory analysis.

The dataset was selected because its fields map directly to the prototype's intended booking-data workflow. Where the prototype expects a single `CheckInDate` and `CheckOutDate`, the Kaggle source provides arrival date components and length-of-stay fields, so these can be transformed into the prototype structure. The project documentation also makes clear that real hotel data would ultimately be supplied by the hotel through a reservation-system or OTA CSV export.

---

## <a id="links-to-raw-data"></a>Links to Raw Data

*   **Raw development dataset:** [Kaggle - Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand)
*   **Live HotelBI prototype:** [HotelBI Netlify App](https://hotelbii.netlify.app/)

The CSV supplied with this submission is the project's local working copy of the Hotel Booking Demand dataset. The Netlify link is the deployed front-end prototype documented in the project report.

---

## <a id="data-description-and-understandings"></a>Data Description and Understandings

The HotelBI upload screen defines four required columns and five optional columns. The table below maps those fields to the supplied Hotel Booking Demand dataset and explains why each field matters to the project. `GuestName` is optional in HotelBI but does not exist in the Kaggle dataset, so no guest-name analysis is claimed.

| HotelBI Field | Source / Transformation | Requirement | Why It Matters |
| :--- | :--- | :--- | :--- |
| **CheckInDate** | arrival_date_year + arrival_date_month + arrival_date_day_of_month | Required | Defines arrival timing and supports time-based trends. |
| **CheckOutDate** | CheckInDate + stays_in_weekend_nights + stays_in_week_nights | Required | Defines stay end date and length of stay. |
| **RateAmount** | adr | Required | Supports ADR and revenue-oriented analysis. |
| **BookingStatus** | is_canceled / reservation_status | Required | Separates confirmed and cancelled bookings and supports cancellation analysis. |
| **RoomType** | assigned_room_type | Optional | Supports room-category views in the prototype. |
| **Channel** | distribution_channel | Optional | Supports the bookings-by-channel view and channel comparison. |
| **GuestName** | Not available in supplied Kaggle dataset | Optional | Supported by the prototype upload structure, but not used in this dataset analysis. |
| **GuestCountry** | country | Optional | Provides guest-origin context. |
| **RepeatGuest** | is_repeated_guest | Optional | Supports the repeat-guest metric in Guest Insights. |


<img width="425" height="248" alt="image" src="https://github.com/user-attachments/assets/bbb7dda0-3ac5-4840-bfe3-eee6b246ec5e" />

*   **Figure:** Booking status distribution after duplicate removal. Cancellation rate in the prepared data is 27.5%.

<img width="425" height="248" alt="image" src="https://github.com/user-attachments/assets/9c1dfa0f-fde3-4ff7-baa8-461aafce60ad" />

*   **Figure:** Booking volume by distribution channel. The data supports the channel-mix view that appears in the HotelBI dashboard.

  <img width="425" height="248" alt="image" src="https://github.com/user-attachments/assets/cc6a17f0-4173-49c9-b0e2-20f37a3286d0" />

*   **Figure:** Lead-time distribution. The prepared data has an average lead time of 79.9 days and a median of 49 days, supporting the lead-time metric in Guest Insights.
  
<img width="425" height="248" alt="image" src="https://github.com/user-attachments/assets/bf3615bf-8932-4d68-abb7-87a3cdd03fae" />

*   **Figure:** ADR distribution for confirmed bookings within the displayed 0-500 range. The mean ADR for confirmed non-negative-rate records is about 102.00.

The EDA patterns directly relate to HotelBI rather than introducing additional analytics. Cancellation status supports the alerts and Guest Insights modules; distribution channel supports the channel breakdown; lead time supports Guest Insights; and ADR supports the revenue and occupancy dashboard. Repeat guests account for about 3.9% of the prepared records, which is why repeat-guest tracking is shown as a dedicated metric in the prototype.

---

## <a id="data-primary-cleaning-and-transformation"></a>Data Primary Cleaning and Transformation

The preparation sequence is aligned with the HotelBI upload and ETL behavior described in the project documentation and with the fields shown on the prototype upload screen:

*   Validate the incoming CSV structure. HotelBI requires `CheckInDate`, `CheckOutDate`, `RateAmount`, and `BookingStatus`; `RoomType`, `Channel`, `GuestName`, `GuestCountry`, and `RepeatGuest` are optional.
*   Remove exact duplicate rows. In the supplied source file, 31,994 exact duplicate rows are detected, leaving 87,396 rows after this step.
*   Create `CheckInDate` from the Kaggle arrival year, month, and day fields and convert it to a true date value.
*   Create total stay nights by adding weekend and week-night stays, then derive `CheckOutDate` from `CheckInDate` plus total stay nights.
*   Map `adr` to `RateAmount` and map cancellation information to a clear `BookingStatus` value (Confirmed or Cancelled).
*   Map `assigned_room_type` to `RoomType`, `distribution_channel` to `Channel`, `country` to `GuestCountry`, and `is_repeated_guest` to `RepeatGuest`.
*   Fill missing country values with an explicit `Unknown` label for analysis. The four missing children values are set to zero for preparation, although children is not a HotelBI upload field.
*   Do not invent `GuestName` because that field is not available in the supplied dataset. It remains an optional prototype field only.
*   Preserve the project limitation around occupancy: true occupancy requires room-inventory availability as well as bookings, and the supplied dataset does not provide a complete room inventory calendar. So, this report does not present the prototype's sample occupancy percentage as a value calculated from the Kaggle CSV.

---

## <a id="python-libraries-and-backend-implementation"></a>Python Libraries and Backend Implementation

The Python backend was developed using several libraries to support data processing, web API development, database management, and analytical operations.

*   **Flask:** Used to build the backend application and create REST API endpoints that connect the dashboard with the data-processing layer.
*   **Pandas:** Used as the main data analysis and manipulation library. It is responsible for reading CSV files, cleaning records, removing duplicates, converting data types, filtering invalid records, grouping data, and calculating analytical metrics.
*   **NumPy:** Used for numerical calculations and statistical operations, particularly when calculating averages, sums, and forecasting values.
*   **SQLite3:** Used to create and manage the local database. It stores upload history, user profiles, and system settings.
*   **JSON:** Used to serialize and exchange structured data between the backend and frontend.
*   **io:** Used to read uploaded CSV files directly from memory before processing them with Pandas.
*   **datetime:** Used to handle dates and timestamps, including upload times and hotel booking dates.
*   **Flask-CORS:** Used to enable communication between the frontend application and the Flask backend.

The backend is organized into reusable functions. The `process_dataframe()` function performs the main data-validation and transformation process. It checks the required columns, removes duplicate records, converts dates and numerical fields, validates room availability and revenue values, and calculates occupancy, ADR, and RevPAR.

The `daily_metrics()` function transforms booking-level information into daily hotel performance metrics. It calculates the number of occupied rooms, revenue, occupancy percentage, ADR, and RevPAR for each day.

The `guest_insights()` function analyzes guest-related information and produces indicators such as repeat-guest rate, cancellation rate, average stay duration, booking channels, guest countries, and room types.

This structure separates data processing from the presentation layer and allows the analytical results to be returned to the dashboard through API responses.

---

## <a id="data-visualization-and-insights"></a>Data Visualization and Insights

The final visualization layer is the HotelBI web dashboard. The screenshots below are taken from the supplied project documentation and represent the same functions documented for the deployed prototype. The report does not add dashboard modules beyond those already present in HotelBI.

### Exploratory Data Analysis (EDA)
The EDA figures in the previous section were used to verify that the supplied dataset can support the same dimensions represented in the prototype: booking status, channel, lead time, ADR, and repeat-guest behavior. These checks establish the availability and distribution of the data before it is mapped into the HotelBI upload structure.

### Dashboard Design & Insights

*   **Business Question 1 - How is the hotel performing across occupancy, ADR, RevPAR, and channel mix?**
<img width="399" height="281" alt="image" src="https://github.com/user-attachments/assets/f944d891-710d-4400-8aa4-ab0a7b73156c" />

    *HotelBI Revenue and Occupancy dashboard - 14-day view.*  
    The main dashboard answers this with three KPI cards, an Occupancy and ADR trend chart, a RevPAR chart, and a bookings-by-channel donut chart. In the prototype screenshot the selected 14-day view displays 79.8% occupancy, $149 ADR, and $120 RevPAR. These figures are part of the prototype demonstration; the project documentation states that the occupancy trend is illustrative rather than calculated live from the supplied Kaggle dataset.

*   **Business Question 2 - What do the bookings reveal about guest behavior?**  
    *HotelBI Guest Behavior screen.*  
    The Guest Insights screen presents repeat guest rate, average booking lead time, and cancellation rate from the manager's most recent upload. These are the same dimensions verified in the EDA from `is_repeated_guest`, `lead_time`, and booking/cancellation status.

*   **Business Question 3 - What is the current room-status picture?**  
    *HotelBI Room Status screen.*  
    The Room Status module shows rooms grouped by room type and labels them as occupied, available, or out of service. In the current prototype this is a demonstration view; the project documentation notes that a full room inventory calendar is not yet modeled in the backend.

*   **Business Question 4 - How do the hotel's rates compare with competitors?**  
    *HotelBI Competitor Pricing screen.*  
    The Premium-tier competitor view compares the hotel's own rate with manually entered competitor rates for the same period and room type. The current system does not collect competitor rates automatically.

*   **Business Question 5 - What does the short-term outlook look like?**  
    *HotelBI Occupancy Forecast screen.*  
    The forecast screen shows the next 10 days and is intended for the project's short 7-14 day planning window. The current prototype uses simple moving averages rather than a machine-learning forecast.

*   **Business Question 6 - What requires management attention and why?**  
    *HotelBI Alerts and Recommendations screen / Administrator Alert Thresholds screen.*  
    The alert system is intentionally explainable. The administrator screen exposes the default thresholds used by the prototype: a 65% low-occupancy threshold, a $20 competitor-rate gap, and a 10% cancellation-spike threshold. Alerts show a severity, generation date, and a plain-language reason so the manager can understand why each alert fired.

---

## <a id="advanced-analytics-and-ai-modeling"></a>Advanced Analytics and AI Modeling

The project does not implement a machine-learning or generative-AI model. This is intentional and is consistent with both the documented design and the prototype. The advanced analytics component combines rule-based decision logic with short-term statistical forecasting so the output remains transparent to hotel managers.

*   **Rule-based analytics:** The alert engine compares current or projected values with configurable thresholds. The prototype administrator view shows default rules for low occupancy (65%), competitor rate gap ($20), and cancellation spike (10%). The purpose is not to produce a hidden score; it is to generate an alert whose reason can be shown directly to the manager.
*   **Forecasting:** The current prototype uses simple moving averages to produce a short 7-14 day occupancy/revenue outlook. The documentation explicitly treats longer-window or more sophisticated forecasting as future work. Because the project does not use a trained predictive model, measures such as model accuracy, feature weights, precision, recall, or confusion matrices are not applicable to the current implementation and are so not reported.

---

## <a id="data-analytics-and-business-intelligence-functions"></a>Data Analytics and Business Intelligence Functions

The second Python component focuses on transforming cleaned hotel booking data into meaningful Business Intelligence indicators and decision-support information.

The data-cleaning process uses functions such as `_norm_name()`, `_rename_columns()`, `parse_csv_bytes()`, and `clean_bookings()`. These functions standardize column names, identify required fields, remove duplicate records, validate dates and rates, handle missing optional fields, standardize booking statuses and booking channels, and create additional analytical fields such as `Nights` and `StayRevenue`.

Several Key Performance Indicators (KPIs) are calculated from the processed data:
*   **Occupancy Rate:** Calculated as rooms sold divided by available rooms, multiplied by 100.
*   **Average Daily Rate (ADR):** Calculated as room revenue divided by the number of rooms sold.
*   **Revenue per Available Room (RevPAR):** Calculated as room revenue divided by the total number of available rooms.
*   **Repeat Guest Rate:** Calculated from the percentage of bookings identified as repeat guests.
*   **Cancellation Rate:** Calculated from the percentage of bookings classified as cancelled or no-show.
*   **Average Stay:** Calculated from the average number of nights per booking.

The `dashboard_summary()` function aggregates the daily analytical results and provides average occupancy, average ADR, average RevPAR, and total revenue.

For predictive analytics, the `forecast_from_daily()` function uses historical occupancy values and NumPy numerical functions to estimate future occupancy. A linear trend is fitted to the available daily data using `numpy.polyfit()`, and the predicted values are limited to a realistic range between 0% and 100%. The function also calculates lower and upper prediction boundaries using the standard deviation of the historical residuals.

The `build_alerts()` function implements rule-based Business Intelligence alerts. It compares calculated KPIs against configurable thresholds and generates alerts when performance requires management attention. This provides an explainable decision-support mechanism instead of relying on a black-box machine-learning model.

Overall, these functions demonstrate the transformation of raw hotel data into cleaned information, analytical KPIs, trends, forecasts, and actionable business insights.

---

## <a id="tools-research-and-selection-effort"></a>Tools Research and Selection Effort

The tools selected in the project are those documented in the implementation and reference list. The prototype is a web application, and the main choices support CSV handling, interface development, charting, icons, and deployment:

*   **React:** Used to build the interactive front-end interface and role-based screens.
*   **Papa Parse:** Used for CSV parsing in the front-end prototype.
*   **Recharts:** Used for the dashboard charts and visualizations.
*   **Lucide:** Used for interface icons.
*   **Netlify:** Used to deploy the front-end prototype at `hotelbii.netlify.app`.
*   **Kaggle Hotel Booking Demand dataset:** Used as the development and testing data source.
*   **Power BI and Tableau:** Reviewed as established BI competitors; they were not used to build HotelBI because the project is a custom hotel-specific web prototype.

---

## <a id="html-and-frontend-implementation"></a>HTML and Frontend Implementation

The HTML component provides the basic structure and entry point of the HotelBI web application. The document defines the page structure, metadata, viewport configuration, title, and the root element in which the React application is rendered.

The frontend is responsible for presenting the analytical results in an interactive dashboard. It provides the user interface for uploading data, viewing KPIs, exploring guest insights, monitoring room status, reviewing competitor pricing, viewing forecasts, and managing alerts. The frontend communicates with the Python backend through API endpoints. For example, uploaded CSV files are sent to the backend for validation and processing, while the resulting JSON data is returned to the frontend and displayed through the dashboard.

The interface therefore acts as the visualization layer of the Business Intelligence system, while Python performs the main data preparation and analytical processing. This separation follows a clear data flow:

> Raw Data $\rightarrow$ Data Cleaning $\rightarrow$ Data Transformation $\rightarrow$ KPI Calculation $\rightarrow$ Analytics/Forecasting $\rightarrow$ API $\rightarrow$ Dashboard Visualization

This architecture allows the project to convert raw hotel booking data into information that can support operational and managerial decision-making.

---

## <a id="project-deployment-effort---use-case"></a>Project Deployment Effort – Use Case

The business consumes HotelBI as an interactive web application. The deployed prototype is available through Netlify and is designed around two roles: Hotel Manager and Administrator.

*   **Deployment URL:** [https://hotelbii.netlify.app/](https://hotelbii.netlify.app/)

### Hotel Manager Use Case Sequence
*   Open the web application and select Hotel Manager on the login screen.
*   Log in using the manager account.
*   Open Upload Data and submit a CSV containing the required booking fields; the screen also provides sample and error-file demonstrations.
*   Use Dashboard to review the selected 7-day or 14-day revenue and occupancy view.
*   Open Guest Insights, Room Status, Competitor Pricing, Forecasts, and Alerts for the corresponding analysis modules.
*   Use Export Reports to export current information and Upload History to review or reprocess previous submissions.
*   Use Profile to review hotel details and Standard/Premium subscription information.

### Administrator Use Case Sequence
*   Log in as Administrator.
*   Use Platform Overview to review aggregate hotel accounts, premium accounts, uploads, and open alerts.
*   Use Hotel Onboarding to confirm new-hotel setup.
*   Use Alert Thresholds to adjust the default rules.
*   Use Subscription Tiers to review the Standard and Premium feature sets.

*   *HotelBI Administrator - Platform Overview.*  
**Current deployment scope:** The deployed version is a front-end demonstration. The supplied documentation states that there is no real persistent server/database behind it yet, uploaded data and account changes do not persist after refresh, and login uses fixed demo credentials. These limitations are retained here rather than describing deployment capabilities that are not part of the current project.

---

## <a id="results"></a>Results

The project produced a complete front-end HotelBI prototype that connects the major business questions of an independent hotel to a single interface. The manager side covers upload, revenue and occupancy, channel mix, guest behavior, room status, competitor pricing, short-term forecasting, alerts, exports, upload history, and profile/subscription management. The administrator side adds platform overview, onboarding, alert thresholds, and subscription-tier controls. This confirms that the planned information architecture and user flow can be represented coherently in one hotel-specific BI product.

The supplied dataset also supports the key analytical dimensions used by the prototype. After the documented duplicate-removal preparation step, 87,396 records remain. The prepared data shows a cancellation rate of 27.5%, a repeat-guest rate of 3.9%, an average lead time of 79.9 days, and a median lead time of 49 days. These findings validate the availability of booking-status, repeat-guest, and lead-time signals that HotelBI exposes in its Guest Insights and alert-oriented views. Channel and ADR fields likewise support the channel mix and rate-oriented dashboard components.

The most important project result is not a single predictive score; it is the explainable workflow demonstrated by the dashboard and alert system. A manager can see the KPI or threshold that led to a recommendation rather than being asked to trust a black-box model. At the same time, the evaluation must remain within the current implementation: true occupancy still requires a full room inventory model, competitor rates are entered manually, the forecast uses moving averages, and the deployed prototype has no persistent backend or real authentication. These are documented limitations and future-development areas rather than functions claimed as completed.

---

## <a id="references"></a>References

*   Cloudbeds. (n.d.). *Cloudbeds hospitality platform*. [https://www.cloudbeds.com](https://www.cloudbeds.com)
*   Little Hotelier. (n.d.). *Little Hotelier property management system*. [https://www.littlehotelier.com](https://www.littlehotelier.com)
*   Lucide. (n.d.). *Lucide icon library*. [https://lucide.dev](https://lucide.dev)
*   Mews. (n.d.). *Mews hospitality cloud*. [https://www.mews.com](https://www.mews.com)
*   Microsoft. (n.d.). *Power BI*. [https://powerbi.microsoft.com](https://powerbi.microsoft.com)
*   Mostipak, J. (2020). *Hotel booking demand dataset*. Kaggle. [https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand)
*   Papa Parse. (n.d.). *Papa Parse, a powerful CSV parser for JavaScript*. [https://www.papaparse.com](https://www.papaparse.com)
*   React. (n.d.). *React, the library for web and native user interfaces*. [https://react.dev](https://react.dev)
*   Recharts. (n.d.). *Recharts, a composable charting library built on React components*. [https://recharts.org](https://recharts.org)
*   Tableau. (n.d.). *Tableau Software*. [https://www.tableau.com](https://www.tableau.com)
*   HotelBI prototype. (2026). *Hotel Revenue and Guest Insights Dashboard*. [https://hotelbii.netlify.app/](https://hotelbii.netlify.app/)
