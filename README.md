
Hotel Revenue and Guest Insights Dashboard

___________________________________________________________________________________

Authors

Mohammed Abudagga
202210006



Supervised by
Dr. Wasef Matar.


Course: 307498 – Graduation Project
First Semester, 2025/2027

2026

___________________________________________________________________________________




Abstract	3

Acknowledgment	3

Business Intelligence Project description and objectives	4

Data Research and Acquiring Effort	4

Links to raw data	4

Data Description and understandings	5

Data Primary Cleaning and Transformation	8

Data Visualization and Insights	8

Advanced Analytics and AI Modeling	14

Tools Research and Selection Effort	15

Project Deployment Effort – Use Case	15

Results	16

References	17



___________________________________________________________________________________














Abstract

Independent hotels with roughly ten to one hundred rooms generate booking and guest data through reservation systems and online travel agencies, but many small properties still lack an affordable and understandable way to turn that data into pricing, occupancy, and channel decisions. The Hotel Revenue and Guest Insights Dashboard addresses this gap through a web-based prototype designed specifically for independent hotel managers.

The project uses the supplied Hotel Booking Demand dataset for development and exploratory analysis. The prototype workflow accepts a booking CSV, validates the required fields, applies the intended cleaning and standardization steps, and presents hotel-specific dashboard modules for revenue and occupancy, booking channels, guest behavior, room status, competitor pricing, short-term forecasts, alerts, exports, upload history, and subscription management. The analytics approach is deliberately explainable: alerts are rule-based and the forecast is based on simple moving averages rather than a black-box machine-learning model.

The result is a working front-end demonstration that shows how a hotel manager can move from booking data to a clear operational view in a small number of steps. The prototype demonstrates the intended user experience and business logic, while the current documented limitations remain: no persistent backend/database, illustrative occupancy values on the main dashboard, manual competitor-rate entry, and moving-average forecasting intended for a short 7-14 day window.

___________________________________________________________________________________

Acknowledgment

I would like to thank my supervisor, Dr. Wasef Matar, for his guidance and honest feedback throughout the development of this project. His questions about who would actually pay for this and why pushed me to rethink parts of the business model I had originally taken for granted, and the project is stronger for it.

I am also grateful to the Faculty of Administrative and Financial Sciences at the University of Petra for the resources and support that made this project possible, and to the independent hotel managers and industry contacts who took the time to discuss how they currently handle pricing and booking data. Their input shaped how I approached this problem.

___________________________________________________________________________________

Business Intelligence Project description and objectives

HotelBI is a web-based business intelligence prototype for independent hotel owners and managers, especially properties with roughly 10-100 rooms and no dedicated analytics team. The business problem is not a lack of booking data; it is the lack of an affordable and simple way to interpret that data. The project so focuses on turning a booking CSV export into hotel-specific insights that can be understood without a technical background.


The project objectives documented and implemented in the prototype are:
• Provide a CSV upload workflow for hotel booking data and clearly identify required and optional fields.

• Apply an ETL preparation process that validates files, removes duplicate rows, standardizes date formats, and standardizes booking-channel values.

• Present core hotel performance views including occupancy, Average Daily Rate (ADR), Revenue per Available Room (RevPAR), and booking-channel mix.

• Show guest behavior measures including repeat guest rate, booking lead time, and cancellation rate.

• Provide room-status, competitor-pricing, forecasting, alerts/recommendations, export, upload-history, and profile/subscription screens.

• Keep alerts explainable through configurable thresholds instead of relying on a black-box prediction model.

• Support a 7-14 day short-term forecasting use case using a simple moving-average approach in the current prototype.

___________________________________________________________________________________

Data Research and Acquiring Effort

The project required a hotel-booking dataset containing fields that could support the same business questions represented in HotelBI: booking status, arrival dates, stay duration, rate, distribution channel, guest country, repeat-guest status, room type, lead time, and cancellation behavior. The supplied development dataset is the Hotel Booking Demand dataset by Jesse Mostipak on Kaggle. It contains 119,390 rows and 32 source columns and was used for development, testing, and exploratory analysis.
The dataset was selected because its fields map directly to the prototype's intended booking-data workflow. Where the prototype expects a single CheckInDate and CheckOutDate, the Kaggle source provides arrival date components and length-of-stay fields, so these can be transformed into the prototype structure. The project documentation also makes clear that real hotel data would ultimately be supplied by the hotel through a reservation-system or OTA CSV export.

___________________________________________________________________________________

Links to raw data

Raw development dataset: Kaggle - Hotel Booking Demand
Live HotelBI prototype: https://hotelbii.netlify.app/
The CSV supplied with this submission is the project's local working copy of the Hotel Booking Demand dataset. The Netlify link is the deployed front-end prototype documented in the project report.

___________________________________________________________________________________


Data Description and understandings

The HotelBI upload screen defines four required columns and five optional columns. The table below maps those fields to the supplied Hotel Booking Demand dataset and explains why each field matters to the project. GuestName is optional in HotelBI but does not exist in the Kaggle dataset, so no guest-name analysis is claimed.
HotelBI field	Source / transformation	Requirement	Why it matters
CheckInDate	arrival_date_year + arrival_date_month + arrival_date_day_of_month	Required	Defines arrival timing and supports time-based trends.
CheckOutDate	CheckInDate + stays_in_weekend_nights + stays_in_week_nights	Required	Defines stay end date and length of stay.
RateAmount	adr	Required	Supports ADR and revenue-oriented analysis.
BookingStatus	is_canceled / reservation_status	Required	Separates confirmed and cancelled bookings and supports cancellation analysis.
RoomType	assigned_room_type	Optional	Supports room-category views in the prototype.
Channel	distribution_channel	Optional	Supports the bookings-by-channel view and channel comparison.
GuestName	Not available in supplied Kaggle dataset	Optional	Supported by the prototype upload structure, but not used in this dataset analysis.
GuestCountry	country	Optional	Provides guest-origin context.
RepeatGuest	is_repeated_guest	Optional	Supports the repeat-guest metric in Guest Insights.
Initial EDA used the supplied CSV before and after the intended duplicate-removal step. The raw file contains 119,390 records and 32 columns. Exact duplicate-row checking identified 31,994 duplicate rows. Missing values occur mainly in company (112,593), agent (16,340), country (488), and children (4). Company and agent are not required by the HotelBI prototype, while missing country and children values can be handled during preparation.
___________________________________________________________________________________
 
Figure: Booking status distribution after duplicate removal. Cancellation rate in the prepared data is 27.5%.
 
Figure: Booking volume by distribution channel. The data supports the channel-mix view that appears in the HotelBI dashboard.
 
Figure: Lead-time distribution. The prepared data has an average lead time of 79.9 days and a median of 49 days, supporting the lead-time metric in Guest Insights.
 
Figure: ADR distribution for confirmed bookings within the displayed 0-500 range. The mean ADR for confirmed non-negative-rate records is about 102.00.

The EDA patterns directly relate to HotelBI rather than introducing additional analytics. Cancellation status supports the alerts and Guest Insights modules; distribution channel supports the channel breakdown; lead time supports Guest Insights; and ADR supports the revenue and occupancy dashboard. Repeat guests account for about 3.9% of the prepared records, which is why repeat-guest tracking is shown as a dedicated metric in the prototype.

___________________________________________________________________________________


Data Primary Cleaning and Transformation

The preparation sequence is aligned with the HotelBI upload and ETL behavior described in the project documentation and with the fields shown on the prototype upload screen:

• Validate the incoming CSV structure. HotelBI requires CheckInDate, CheckOutDate, RateAmount, and BookingStatus; RoomType, Channel, GuestName, GuestCountry, and RepeatGuest are optional.

• Remove exact duplicate rows. In the supplied source file, 31,994 exact duplicate rows are detected, leaving 87,396 rows after this step.

• Create CheckInDate from the Kaggle arrival year, month, and day fields and convert it to a true date value.

• Create total stay nights by adding weekend and week-night stays, then derive CheckOutDate from CheckInDate plus total stay nights.

• Map adr to RateAmount and map cancellation information to a clear BookingStatus value (Confirmed or Cancelled).

• Map assigned_room_type to RoomType, distribution_channel to Channel, country to GuestCountry, and is_repeated_guest to RepeatGuest.

• Fill missing country values with an explicit Unknown label for analysis. The four missing children values are set to zero for preparation, although children is not a HotelBI upload field.

• Do not invent GuestName because that field is not available in the supplied dataset. It remains an optional prototype field only.

• Preserve the project limitation around occupancy: true occupancy requires room-inventory availability as well as bookings, and the supplied dataset does not provide a complete room inventory calendar. so, this report does not present the prototype's sample occupancy percentage as a value calculated from the Kaggle CSV.

___________________________________________________________________________________


Data Visualization and Insights:

The final visualization layer is the HotelBI web dashboard. The screenshots below are taken from the supplied project documentation and represent the same functions documented for the deployed prototype. The report does not add dashboard modules beyond those already present in HotelBI.


Exploratory Data Analysis (EDA)

The EDA figures in the previous section were used to verify that the supplied dataset can support the same dimensions represented in the prototype: booking status, channel, lead time, ADR, and repeat-guest behavior. These checks establish the availability and distribution of the data before it is mapped into the HotelBI upload structure.


Dashboard Design & Insights

Business Question 1 - How is the hotel performing across occupancy, ADR, RevPAR, and channel mix?

___________________________________________________________________________________

 
HotelBI Revenue and Occupancy dashboard - 14-day view.

The main dashboard answers this with three KPI cards, an Occupancy and ADR trend chart, a RevPAR chart, and a bookings-by-channel donut chart. In the prototype screenshot the selected 14-day view displays 79.8% occupancy, $149 ADR, and $120 RevPAR. These figures are part of the prototype demonstration; the project documentation states that the occupancy trend is illustrative rather than calculated live from the supplied Kaggle dataset.


Business Question 2 - What do the bookings reveal about guest behavior?
 
HotelBI Guest Behavior screen.
The Guest Insights screen presents repeat guest rate, average booking lead time, and cancellation rate from the manager's most recent upload. These are the same dimensions verified in the EDA from is_repeated_guest, lead_time, and booking/cancellation status.


Business Question 3 - What is the current room-status picture?
 
HotelBI Room Status screen.
The Room Status module shows rooms grouped by room type and labels them as occupied, available, or out of service. In the current prototype this is a demonstration view; the project documentation notes that a full room inventory calendar is not yet modeled in the backend.


Business Question 4 - How do the hotel's rates compare with competitors?
 
HotelBI Competitor Pricing screen.
The Premium-tier competitor view compares the hotel's own rate with manually entered competitor rates for the same period and room type. The current system does not collect competitor rates automatically.


Business Question 5 - What does the short-term outlook look like?
 
HotelBI Occupancy Forecast screen.
The forecast screen shows the next 10 days and is intended for the project's short 7-14 day planning window. The current prototype uses simple moving averages rather than a machine-learning forecast.


Business Question 6 - What requires management attention and why?
 
HotelBI Alerts and Recommendations screen.
Administrator Alert Thresholds screen.
The alert system is intentionally explainable. The administrator screen exposes the default thresholds used by the prototype: a 65% low-occupancy threshold, a $20 competitor-rate gap, and a 10% cancellation-spike threshold. Alerts show a severity, generation date, and a plain-language reason so the manager can understand why each alert fired.

___________________________________________________________________________________


Advanced Analytics and AI Modeling

The project does not implement a machine-learning or generative-AI model. This is intentional and is consistent with both the documented design and the prototype. The advanced analytics component combines rule-based decision logic with short-term statistical forecasting so the output remains transparent to hotel managers.
Rule-based analytics: the alert engine compares current or projected values with configurable thresholds. The prototype administrator view shows default rules for low occupancy (65%), competitor rate gap ($20), and cancellation spike (10%). The purpose is not to produce a hidden score; it is to generate an alert whose reason can be shown directly to the manager.

Forecasting: the current prototype uses simple moving averages to produce a short 7-14 day occupancy/revenue outlook. The documentation explicitly treats longer-window or more sophisticated forecasting as future work. Because the project does not use a trained predictive model, measures such as model accuracy, feature weights, precision, recall, or confusion matrices are not applicable to the current implementation and are so not reported.

___________________________________________________________________________________


Tools Research and Selection Effort

The tools selected in the project are those documented in the implementation and reference list. The prototype is a web application, and the main choices support CSV handling, interface development, charting, icons, and deployment:

• React - used to build the interactive front-end interface and role-based screens.
• Papa Parse - used for CSV parsing in the front-end prototype.
• Recharts - used for the dashboard charts and visualizations.
• Lucide - used for interface icons.
• Netlify - used to deploy the front-end prototype at hotelbii.netlify.app.
• Kaggle Hotel Booking Demand dataset - used as the development and testing data source.
• Power BI and Tableau - reviewed as established BI competitors; they were not used to build HotelBI because the project is a custom hotel-specific web prototype.

___________________________________________________________________________________


Project Deployment Effort – Use Case

The business consumes HotelBI as an interactive web application. The deployed prototype is available through Netlify and is designed around two roles: Hotel Manager and Administrator.

Deployment URL: https://hotelbii.netlify.app/

Hotel Manager use case sequence:
• Open the web application and select Hotel Manager on the login screen.
• Log in using the manager account.
• Open Upload Data and submit a CSV containing the required booking fields; the screen also provides sample and error-file demonstrations.
• Use Dashboard to review the selected 7-day or 14-day revenue and occupancy view.
• Open Guest Insights, Room Status, Competitor Pricing, Forecasts, and Alerts for the corresponding analysis modules.
• Use Export Reports to export current information and Upload History to review or reprocess previous submissions.
• Use Profile to review hotel details and Standard/Premium subscription information.

Administrator use case sequence:
• Log in as Administrator.
• Use Platform Overview to review aggregate hotel accounts, premium accounts, uploads, and open alerts.
• Use Hotel Onboarding to confirm new-hotel setup.
• Use Alert Thresholds to adjust the default rules.
• Use Subscription Tiers to review the Standard and Premium feature sets.
 
HotelBI Administrator - Platform Overview.
Current deployment scope: the deployed version is a front-end demonstration. The supplied documentation states that there is no real persistent server/database behind it yet, uploaded data and account changes do not persist after refresh, and login uses fixed demo credentials. These limitations are retained here rather than describing deployment capabilities that are not part of the current project.

___________________________________________________________________________________


Results

The project produced a complete front-end HotelBI prototype that connects the major business questions of an independent hotel to a single interface. The manager side covers upload, revenue and occupancy, channel mix, guest behavior, room status, competitor pricing, short-term forecasting, alerts, exports, upload history, and profile/subscription management. The administrator side adds platform overview, onboarding, alert thresholds, and subscription-tier controls. This confirms that the planned information architecture and user flow can be represented coherently in one hotel-specific BI product.

The supplied dataset also supports the key analytical dimensions used by the prototype. After the documented duplicate-removal preparation step, 87,396 records remain. The prepared data shows a cancellation rate of 27.5%, a repeat-guest rate of 3.9%, an average lead time of 79.9 days, and a median lead time of 49 days. These findings validate the availability of booking-status, repeat-guest, and lead-time signals that HotelBI exposes in its Guest Insights and alert-oriented views. Channel and ADR fields likewise support the channel mix and rate-oriented dashboard components.

The most important project result is not a single predictive score; it is the explainable workflow demonstrated by the dashboard and alert system. A manager can see the KPI or threshold that led to a recommendation rather than being asked to trust a black-box model. At the same time, the evaluation must remain within the current implementation: true occupancy still requires a full room inventory model, competitor rates are entered manually, the forecast uses moving averages, and the deployed prototype has no persistent backend or real authentication. These are documented limitations and future-development areas rather than functions claimed as completed.

___________________________________________________________________________________


References

Cloudbeds. (n.d.). Cloudbeds hospitality platform. https://www.cloudbeds.com

Little Hotelier. (n.d.). Little Hotelier property management system. https://www.littlehotelier.com

Lucide. (n.d.). Lucide icon library. https://lucide.dev

Mews. (n.d.). Mews hospitality cloud. https://www.mews.com

Microsoft. (n.d.). Power BI. https://powerbi.microsoft.com

Mostipak, J. (2020). Hotel booking demand dataset. Kaggle. https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand

Papa Parse. (n.d.). Papa Parse, a powerful CSV parser for JavaScript. https://www.papaparse.com

React. (n.d.). React, the library for web and native user interfaces. https://react.dev

Recharts. (n.d.). Recharts, a composable charting library built on React components. https://recharts.org

Tableau. (n.d.). Tableau Software. https://www.tableau.com

HotelBI prototype. (2026). Hotel Revenue and Guest Insights Dashboard. https://hotelbii.netlify.app/
