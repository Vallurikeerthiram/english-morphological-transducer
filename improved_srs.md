# Improved Software Requirements Specification

## AgriCapital Connect

**Team Members:** Valluri Keerthi Ram, Abhay Gokavarapu, Ajay Nageswara Rao, Venkata Sai Vivekanand Tammana  
**Submission Date:** 23rd March 2026

## Table of Contents

[TOC would be here]

## Chapter 1: Product Planning (Team)

### 1.1 Product Initial Wish List

### 1.2 Sprint List

### 1.3 Tasks per Sprint

## Chapter 2: Daily Scrum (Individual Updates)

### 2.1 Sprint 1 - Daily Update

#### Day 1
**Roles:**  
Product Owner – Valluri Keerthi Ram  
Scrum Master – Ajay Nageswara Rao  
Developers – Abhay Gokavarapu, Tammana Venkata Sai Vivekanand  

**Today's Work:**  
Understand project vision and product scope.  
Define initial architecture approach.  
Plan repository structure.  

**Blockers:** None  

**Discussion:**  
The Product Owner explained the main goal: creating a transparent digital infrastructure for lease-based agriculture.  

**Problem:** Early in the project, there was confusion about whether to include land sales alongside leasing, as the initial vision focused only on leasing but market research suggested sales could be valuable.  

**Options Considered:**  
1. Stick to pure leasing platform to maintain focus and simplicity.  
2. Expand to include land sales to attract more landowners and investors.  
3. Create modular design allowing future addition of sales without initial complexity.  

**Debate:**  
Keerthi emphasized keeping the MVP simple to avoid scope creep, while Abhay argued that including sales from the start would provide more immediate value and attract diverse users. Ajay raised concerns about timeline impact.  

**Decision:** Include both leasing and sales features in the initial design.  

**Reason:** Market analysis showed that landowners often want to sell rather than lease, and a comprehensive platform would have better adoption. The modular architecture would allow phased implementation.  

The team discussed major modules such as lease lifecycle management, expense tracking, and marketplace functionality. The Scrum Master emphasized following Agile workflow.

#### Day 2
**Roles:**  
Product Owner – Ajay Nageswara Rao  
Scrum Master – Vivekanand Tammana  
Developers – Keerthi Ram Valluri, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Project scope and vision discussion completed.  

**Today's Work:**  
Identify MVP features.  
Define sprint plan.  
Prepare backlog.  

**Blockers:** None  

**Discussion:**  
The team reviewed the product goals and broke them into high-level features such as authentication, lease management, land listing, expense tracking, and ROI analytics.  

**Problem:** Prioritizing features for MVP was challenging due to competing stakeholder needs.  

**Options Considered:**  
1. Farmer-focused MVP with basic leasing.  
2. Balanced MVP covering all user types.  
3. Landowner-focused MVP to secure supply side first.  

**Debate:**  
Vivekanand pushed for farmer-first approach as they are the end-users, while Abhay wanted to prioritize landowners to ensure land availability. Keerthi suggested starting with authentication as the foundation.  

**Decision:** Start with authentication and core data structure.  

**Reason:** Authentication is prerequisite for all features, and getting user management right early prevents future refactoring.  

It was decided that authentication and core data structure would be prioritized first.

#### Day 3
**Roles:**  
Product Owner – Abhay Gokavarapu  
Scrum Master – Keerthi Ram Valluri  
Developers – Ajay Nageswara Rao, Vivekanand  

**Yesterday Completed Work:**  
Sprint planning completed.  

**Today's Work:**  
Define project folder structure.  
Setup Git repository.  
Configure development environment.  

**Blockers:** None  

**Discussion:**  
The team finalized the repository structure and agreed on organizing modules into authentication, land management, marketplace, and finance components.  

**Problem:** Choosing between monolithic vs microservices architecture given the team's size and timeline.  

**Options Considered:**  
1. Monolithic architecture for simplicity and faster initial development.  
2. Microservices for scalability and team parallelization.  
3. Modular monolith as a middle ground.  

**Debate:**  
Ajay argued for microservices to leverage team members' parallel work, while Vivekanand cautioned about complexity for a small team. Keerthi suggested starting monolithic and refactoring later if needed.  

**Decision:** Go with modular monolithic architecture.  

**Reason:** With 4 developers and tight timeline, monolithic allows faster initial delivery while maintaining clean separation of concerns through modules.

#### Day 4
**Roles:**  
Product Owner – Keerthi Ram Valluri  
Scrum Master – Abhay Gokavarapu  
Developers – Ajay Nageswara Rao, Vivekanand  

**Yesterday Completed Work:**  
Repository setup started.  

**Today's Work:**  
Complete repository structure (Task T1).  
Begin database schema design.  

**Blockers:** None  

**Discussion:**  
The team discussed required entities: Users, Land, Lease, Expense, Yield, Settlement.  
Developers started defining database relationships.  

**Problem:** Database design decisions around normalization and relationships.  

**Options Considered:**  
1. Fully normalized schema for data integrity.  
2. Denormalized for performance.  
3. Hybrid approach.  

**Debate:**  
Abhay wanted full normalization, while Ajay suggested some denormalization for read-heavy operations like marketplace listings.  

**Decision:** Balanced normalized schema with strategic denormalization for performance-critical queries.  

**Reason:** Agriculture data has complex relationships that require integrity, but marketplace performance is crucial for user experience.

#### Day 5
**Roles:**  
Product Owner – Vivekanand  
Scrum Master – Ajay Nageswara Rao  
Developers – Keerthi Ram Valluri, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Repository structure finalized.  

**Today's Work:**  
Design database schema (Task T2).  
Identify entity relationships.  

**Blockers:** None  

**Discussion:**  
Developers discussed separating authentication credentials from profile data.  
The team also identified relations between land → lease → expenses → yield → settlement.  

**Problem:** Handling user roles and permissions in the database schema.  

**Options Considered:**  
1. Single users table with role column.  
2. Separate tables for each role type.  
3. Role-based permissions table.  

**Debate:**  
Keerthi preferred single table for simplicity, while Abhay wanted separate tables for better data organization. Vivekanand suggested role-based approach for flexibility.  

**Decision:** Single users table with role enumeration and permissions matrix.  

**Reason:** Simpler queries and easier role management, with permissions handled at application level.

#### Day 6
**Roles:**  
Product Owner – Abhay Gokavarapu  
Scrum Master – Vivekanand  
Developers – Keerthi Ram Valluri, Ajay Nageswara Rao  

**Yesterday Completed Work:**  
Database schema drafting completed.  

**Today's Work:**  
Start implementing user registration module (Task T3).  

**Blockers:** Minor discussion on validation rules.  

**Discussion:**  
Developers discussed mandatory fields such as name, phone number, role, and password.  
Validation rules were defined to ensure unique phone numbers.  

**Problem:** Phone number validation and uniqueness constraints.  

**Options Considered:**  
1. Simple format validation.  
2. Full international phone number support.  
3. OTP verification for uniqueness.  

**Debate:**  
Ajay wanted international support, while Keerthi argued for Indian market focus. Abhay suggested OTP for security.  

**Decision:** Indian phone format with uniqueness check.  

**Reason:** Target market is Indian agriculture, keeping it simple while ensuring no duplicate accounts.

#### Day 7
**Roles:**  
Product Owner – Keerthi Ram Valluri  
Scrum Master – Ajay Nageswara Rao  
Developers – Abhay Gokavarapu, Vivekanand  

**Yesterday Completed Work:**  
User registration module started.  

**Today's Work:**  
Complete registration backend logic.  
Begin login system implementation (Task T4).  

**Blockers:** Password hashing approach discussion.  

**Discussion:**  
The team agreed to implement secure password hashing and ensure authentication tokens are generated properly.  

**Problem:** Choosing authentication mechanism.  

**Options Considered:**  
1. JWT tokens for stateless auth.  
2. Session-based authentication.  
3. OAuth integration.  

**Debate:**  
Vivekanand preferred JWT for scalability, while Abhay worried about token security. Keerthi suggested sessions for simplicity.  

**Decision:** JWT with refresh tokens.  

**Reason:** Better for mobile app compatibility and API design, with proper security measures.

#### Day 8
**Roles:**  
Product Owner – Ajay Nageswara Rao  
Scrum Master – Vivekanand  
Developers – Keerthi Ram Valluri, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Login module development started.  

**Today's Work:**  
Complete login authentication logic.  
Begin role-based access control implementation (Task T5).  

**Blockers:** none  

**Discussion:**  
Developers discussed role restrictions for Farmer, Landowner, and Buyer.  

**Problem:** Granularity of role-based permissions.  

**Options Considered:**  
1. Simple role-based (admin/user).  
2. Attribute-based access control.  
3. Object-level permissions.  

**Debate:**  
Abhay wanted fine-grained permissions, while Keerthi argued for simplicity. Ajay suggested starting simple and expanding.  

**Decision:** Role-based with basic permissions, extensible design.  

**Reason:** Meets current needs while allowing future enhancement without major rework.

#### Day 9
**Roles:**  
Product Owner – Abhay Gokavarapu  
Scrum Master – Keerthi Ram Valluri  
Developers – Ajay Nageswara Rao, Vivekanand  

**Yesterday Completed Work:**  
Login system implemented  

**Today's Work:**  
Implement role-based access control.  
Define permission rules.  

**Blockers:** none  

**Discussion:**  
It was decided that each user can only access data related to their role and ownership.  

**Problem:** Handling data ownership and privacy.  

**Options Considered:**  
1. Database-level row security.  
2. Application-level filtering.  
3. Hybrid approach.  

**Debate:**  
Vivekanand preferred database security, while Ajay argued for application control for flexibility.  

**Decision:** Application-level filtering with database constraints.  

**Reason:** Better performance and easier debugging, with database as safety net.

#### Day 10
**Roles:**  
Product Owner – Vivekanand  
Scrum Master – Ajay Nageswara Rao  
Developers – Keerthi Ram Valluri, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Role access module implemented.  

**Today's Work:**  
Create role-based dashboard templates (Task T6).  

**Blockers:** UI layout decision pending.  

**Discussion:**  
The team discussed designing simple dashboards for each user role.  

**Problem:** UI framework choice.  

**Options Considered:**  
1. React for modern SPA.  
2. Vue.js for simplicity.  
3. Vanilla JS with Bootstrap.  

**Debate:**  
Keerthi wanted React for future scalability, while Abhay preferred Vue for learning curve. Vivekanand suggested vanilla for faster initial development.  

**Decision:** React with Material-UI.  

**Reason:** Team has React experience, Material-UI provides good components for rapid development.

#### Day 11
**Roles:**  
Product Owner – Keerthi Ram Valluri  
Scrum Master – Abhay Gokavarapu  
Developers – Ajay Nageswara Rao, Vivekanand  

**Yesterday Completed Work:**  
Dashboard templates created.  

**Today's Work:**  
Perform authentication testing (Task T7).  

**Blockers:** Minor validation bugs identified.  

**Discussion:**  
Developers tested registration, login, and role-based access workflows.  

**Problem:** Testing approach for authentication.  

**Options Considered:**  
1. Manual testing only.  
2. Unit tests for backend.  
3. Integration tests.  

**Debate:**  
Ajay wanted comprehensive testing, while Keerthi argued for time constraints. Abhay suggested automated unit tests.  

**Decision:** Unit tests for critical auth functions, manual testing for flows.  

**Reason:** Balances quality assurance with development speed.

#### Day 12
**Roles:**  
Product Owner – Ajay Nageswara Rao  
Scrum Master – Vivekanand  
Developers – Keerthi Ram Valluri, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Authentication testing completed.  

**Today's Work:**  
Fix authentication bugs.  
Close Sprint-1.  

**Blockers:** None  

**Discussion:**  
Sprint-1 goals were successfully achieved:  
- Repository setup  
- Database schema design  
- User registration  
- Login system  
- Role-based access  
- Dashboard templates  
- Authentication testing  

**Retrospective:**  
**What went well:** Good collaboration, clear requirements.  
**Problems:** Initial scope debates caused some delays.  
**Improvements:** Better upfront planning for future sprints.  

The team prepared to begin Sprint-2 (Land Management Module).

### 2.2 Sprint 2 - Daily Scrum

#### Day 1
**Roles:**  
Product Owner – Ajay Nageswara Rao  
Scrum Master – Abhay Gokavarapu  
Developers – Keerthi Ram Valluri, Vivekanand  

**Yesterday Completed Work:**  
Sprint-1 successfully completed with authentication and dashboards.  

**Today's Work:**  
Begin Sprint-2 implementation.  
Start creating land database tables (Task T8).  

**Blockers:** None  

**Discussion:**  
The Product Owner explained that Sprint-2 focuses on the land management module.  
The team reviewed the database entities needed for land records including land ID, owner ID, location, size, and status.  

**Problem:** Location data storage format.  

**Options Considered:**  
1. Text address fields.  
2. Geographic coordinates.  
3. Both address and coordinates.  

**Debate:**  
Vivekanand wanted coordinates for mapping, while Keerthi argued text addresses are more user-friendly. Abhay suggested both.  

**Decision:** Store both address and latitude/longitude.  

**Reason:** Supports both user experience and advanced features like distance sorting.

#### Day 2
**Roles:**  
Product Owner – Vivekanand  
Scrum Master – Keerthi Ram Valluri  
Developers – Ajay Nageswara Rao, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Initial land database structure defined.  

**Today's Work:**  
Complete land database schema.  
Define relationships with user and lease tables.  

**Blockers:** Minor discussion about land ownership constraints.  

**Discussion:**  
The team discussed enforcing referential integrity so each land record belongs to a valid landowner.  

**Problem:** Handling multiple owners for same land.  

**Options Considered:**  
1. Single owner only.  
2. Multiple owners with joint ownership.  
3. Primary owner with co-owners.  

**Debate:**  
Abhay wanted multiple owners for family lands, while Ajay preferred single owner simplicity. Keerthi suggested starting with single owner.  

**Decision:** Single landowner per land record.  

**Reason:** Simpler initial implementation, can extend later if needed.

#### Day 3
**Roles:**  
Product Owner – Abhay Gokavarapu  
Scrum Master – Ajay Nageswara Rao  
Developers – Keerthi Ram Valluri, Vivekanand  

**Yesterday Completed Work:**  
Land database schema finalized.  

**Today's Work:**  
Begin implementing add-land module for landowners (Task T9).  

**Blockers:** None  

**Discussion:**  
The developers discussed required fields such as land location, area size, irrigation type, and ownership details.  

**Problem:** Land area units standardization.  

**Options Considered:**  
1. Acres only.  
2. Support multiple units (acres, hectares, sq meters).  
3. User preference setting.  

**Debate:**  
Vivekanand wanted multiple units for international users, while Keerthi argued for acres as standard in Indian agriculture.  

**Decision:** Store in acres, display conversions.  

**Reason:** Simplifies calculations while supporting user preferences.

#### Day 4
**Roles:**  
Product Owner – Keerthi Ram Valluri  
Scrum Master – Vivekanand  
Developers – Ajay Nageswara Rao, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Add-land backend implementation started.  

**Today's Work:**  
Complete backend for land registration.  
Begin frontend form development.  

**Blockers:** None  

**Discussion:**  
The team ensured that land registration forms validate mandatory inputs before submission.  

**Problem:** Document verification process.  

**Options Considered:**  
1. Manual verification by admins.  
2. Automated checks.  
3. Third-party verification service.  

**Debate:**  
Abhay wanted automated verification, while Ajay cautioned about false positives. Keerthi suggested manual for accuracy.  

**Decision:** Manual verification with automated pre-checks.  

**Reason:** Balances security with operational feasibility.

#### Day 5
**Roles:**  
Product Owner – Ajay Nageswara Rao  
Scrum Master – Abhay Gokavarapu  
Developers – Keerthi Ram Valluri, Vivekanand  

**Yesterday Completed Work:**  
Add-land module created.  

**Today's Work:**  
Implement document upload functionality for land verification (Task T10).  

**Blockers:** File storage structure discussion.  

**Discussion:**  
Developers decided to allow document uploads in PDF format.  

**Problem:** File storage architecture.  

**Options Considered:**  
1. Local file system.  
2. Cloud storage (AWS S3).  
3. Database BLOBs.  

**Debate:**  
Vivekanand preferred cloud for scalability, while Keerthi worried about costs. Abhay suggested local for development simplicity.  

**Decision:** Local storage with cloud migration path.  

**Reason:** Faster development, easy to change later.

#### Day 6
**Roles:**  
Product Owner – Vivekanand  
Scrum Master – Keerthi Ram Valluri  
Developers – Ajay Nageswara Rao, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Document upload module partially implemented.  

**Today's Work:**  
Complete land document upload feature.  

**Blockers:** None  

**Discussion:**  
The team discussed linking uploaded documents with land records for verification.  

**Problem:** Document security and access control.  

**Options Considered:**  
1. Public access with tokens.  
2. Authenticated access only.  
3. Owner-only access.  

**Debate:**  
Ajay wanted authenticated access, while Abhay argued for owner-only to protect sensitive documents.  

**Decision:** Owner and admin access only.  

**Reason:** Protects landowner privacy while allowing necessary verifications.

#### Day 7
**Roles:**  
Product Owner – Abhay Gokavarapu  
Scrum Master – Ajay Nageswara Rao  
Developers – Keerthi Ram Valluri, Vivekanand  

**Yesterday Completed Work:**  
Document upload feature completed.  

**Today's Work:**  
Implement landowner view for listing owned lands (Task T11).  

**Blockers:** None  

**Discussion:**  
The team discussed displaying all lands owned by the user in a structured dashboard view.  

**Problem:** Dashboard information density.  

**Options Considered:**  
1. Table view.  
2. Card layout.  
3. Map view.  

**Debate:**  
Keerthi preferred table for data density, while Vivekanand wanted cards for visual appeal. Abhay suggested map integration.  

**Decision:** Card layout with map toggle.  

**Reason:** Better user experience while showing key information.

#### Day 8
**Roles:**  
Product Owner – Keerthi Ram Valluri  
Scrum Master – Vivekanand  
Developers – Ajay Nageswara Rao, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Landowner dashboard listing started.  

**Today's Work:**  
Complete landowner land-listing module.  

**Blockers:** None  

**Discussion:**  
Developers ensured land details such as size, location, and status appear correctly in the dashboard.  

**Problem:** Status indicators and workflow.  

**Options Considered:**  
1. Simple status badges.  
2. Status with action buttons.  
3. Workflow progress bars.  

**Debate:**  
Abhay wanted progress bars, while Ajay preferred simple badges. Keerthi suggested action-oriented design.  

**Decision:** Status badges with contextual actions.  

**Reason:** Clear status communication with actionable next steps.

#### Day 9
**Roles:**  
Product Owner – Ajay Nageswara Rao  
Scrum Master – Abhay Gokavarapu  
Developers – Keerthi Ram Valluri, Vivekanand  

**Yesterday Completed Work:**  
Landowner listing module completed.  

**Today's Work:**  
Implement feature to list land for lease (Task T12).  

**Blockers:** None  

**Discussion:**  
The team discussed adding lease price and availability fields to land records.  

**Problem:** Pricing model complexity.  

**Options Considered:**  
1. Fixed price per acre.  
2. Flexible pricing.  
3. Auction-style.  

**Debate:**  
Vivekanand wanted flexible pricing, while Keerthi argued for simplicity. Abhay suggested starting with fixed price.  

**Decision:** Fixed price per acre per season.  

**Reason:** Matches traditional agricultural leasing practices.

#### Day 10
**Roles:**  
Product Owner – Vivekanand  
Scrum Master – Keerthi Ram Valluri  
Developers – Ajay Nageswara Rao, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Lease listing module started.  

**Today's Work:**  
Complete lease listing implementation.  

**Blockers:** None  

**Discussion:**  
Developers ensured lease listings appear in the marketplace feed.  

**Problem:** Marketplace visibility rules.  

**Options Considered:**  
1. All listings visible.  
2. Filtered by user type.  
3. Location-based visibility.  

**Debate:**  
Abhay wanted location filtering, while Ajay preferred open marketplace. Keerthi suggested user-type filtering.  

**Decision:** All authenticated users can see all listings.  

**Reason:** Maximizes opportunities for landowners and farmers.

#### Day 11
**Roles:**  
Product Owner – Abhay Gokavarapu  
Scrum Master – Ajay Nageswara Rao  
Developers – Keerthi Ram Valluri, Vivekanand  

**Yesterday Completed Work:**  
Lease listing functionality implemented.  

**Today's Work:**  
Implement land sale listing module (Task T13).  

**Blockers:** None  

**Discussion:**  
The team decided to reuse marketplace infrastructure for sale listings.  

**Problem:** Sale vs lease differentiation.  

**Options Considered:**  
1. Separate sections.  
2. Unified feed with filters.  
3. Different marketplaces.  

**Debate:**  
Keerthi wanted separate sections, while Vivekanand preferred unified feed. Abhay suggested filters.  

**Decision:** Unified marketplace with type filters.  

**Reason:** Simpler UI and better discoverability.

#### Day 12
**Roles:**  
Product Owner – Keerthi Ram Valluri  
Scrum Master – Vivekanand  
Developers – Ajay Nageswara Rao, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Land sale listing module implemented.  

**Today's Work:**  
Improve UI for land management pages (Task T14).  

**Blockers:** None  

**Discussion:**  
Developers improved layout, form validation, and responsiveness.  

**Problem:** Mobile responsiveness priority.  

**Options Considered:**  
1. Desktop-first.  
2. Mobile-first.  
3. Responsive design.  

**Debate:**  
Ajay wanted mobile-first for farmers, while Abhay argued desktop for landowners. Keerthi suggested responsive.  

**Decision:** Fully responsive design.  

**Reason:** Users access from various devices in agricultural settings.

#### Day 13
**Roles:**  
Product Owner – Ajay Nageswara Rao  
Scrum Master – Abhay Gokavarapu  
Developers – Keerthi Ram Valluri, Vivekanand  

**Yesterday Completed Work:**  
UI improvements completed.  

**Today's Work:**  
Review Sprint-2 progress.  
Close Sprint-2.  

**Blockers:** None  

**Discussion:**  
Sprint-2 goals achieved:  
- Land database tables  
- Land registration  
- Document upload  
- Landowner land listing  
- Lease listing  
- Sale listing  
- UI improvements  

**Retrospective:**  
**What went well:** Good progress on land management features.  
**Problems:** Some UI design debates slowed progress.  
**Improvements:** Establish design system earlier to reduce discussions.

The team prepared to begin Sprint-3 marketplace browsing features.

### 2.3 Sprint 3 - Daily Scrum

#### Day 1
**Roles:**  
Product Owner – Keerthi Ram Valluri  
Scrum Master – Ajay Nageswara Rao  
Developers – Abhay Gokavarapu, Vivekanand  

**Yesterday Completed Work:**  
Sprint-2 completed with land management module.  

**Today's Work:**  
Start Sprint-3.  
Begin developing marketplace module for showing lands available for lease (Task T15).  

**Blockers:** None  

**Discussion:**  
The team discussed how marketplace listings will display land details including location, area, price, and lease availability.  
Developers decided to reuse the existing land database structure for generating listing feeds.  

**Problem:** Marketplace performance with large datasets.  

**Options Considered:**  
1. Simple pagination.  
2. Infinite scroll.  
3. Search and filter first.  

**Debate:**  
Vivekanand wanted infinite scroll, while Keerthi preferred pagination. Abhay suggested prioritizing search.  

**Decision:** Pagination with advanced filters.  

**Reason:** Better performance and user control.

#### Day 2
**Roles:**  
Product Owner – Vivekanand  
Scrum Master – Abhay Gokavarapu  
Developers – Keerthi Ram Valluri, Ajay Nageswara Rao  

**Yesterday Completed Work:**  
Lease marketplace module started.  

**Today's Work:**  
Complete backend API for lease marketplace listings.  

**Blockers:** None  

**Discussion:**  
The team verified that lease listings are fetched correctly from the database and displayed to farmers in the marketplace dashboard.  

**Problem:** API response format standardization.  

**Options Considered:**  
1. Custom JSON format.  
2. RESTful conventions.  
3. GraphQL.  

**Debate:**  
Ajay wanted GraphQL for flexibility, while Keerthi argued REST is sufficient. Abhay suggested standard REST.  

**Decision:** RESTful API with consistent JSON format.  

**Reason:** Team familiarity and simpler implementation.

#### Day 3
**Roles:**  
Product Owner – Abhay Gokavarapu  
Scrum Master – Keerthi Ram Valluri  
Developers – Ajay Nageswara Rao, Vivekanand  

**Yesterday Completed Work:**  
Lease listing module completed.  

**Today's Work:**  
Implement marketplace module to display lands available for sale (Task T16).  

**Blockers:** None  

**Discussion:**  
The developers discussed reusing the same marketplace interface but filtering listings by sale availability.  

**Problem:** Sale price display format.  

**Options Considered:**  
1. Per acre pricing.  
2. Total price.  
3. Both.  

**Debate:**  
Vivekanand wanted both, while Abhay preferred per acre. Keerthi suggested total price for clarity.  

**Decision:** Show both per acre and total price.  

**Reason:** Gives users flexibility in understanding value.

#### Day 4
**Roles:**  
Product Owner – Ajay Nageswara Rao  
Scrum Master – Vivekanand  
Developers – Keerthi Ram Valluri, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Sale listing module implemented.  

**Today's Work:**  
Integrate lease listings and sale listings into the same marketplace feed (Task T17).  

**Blockers:** None  

**Discussion:**  
The team ensured that the system clearly differentiates between lease listings and sale listings using separate indicators.  

**Problem:** Visual differentiation strategy.  

**Options Considered:**  
1. Color coding.  
2. Icons.  
3. Badges.  

**Debate:**  
Keerthi wanted color coding, while Ajay preferred icons. Abhay suggested badges.  

**Decision:** Color-coded badges with icons.  

**Reason:** Clear visual hierarchy and accessibility.

#### Day 5
**Roles:**  
Product Owner – Keerthi Ram Valluri  
Scrum Master – Abhay Gokavarapu  
Developers – Ajay Nageswara Rao, Vivekanand  

**Yesterday Completed Work:**  
Marketplace integration completed.  

**Today's Work:**  
Implement distance-based sorting of listings (Task T18).  

**Blockers:** Location coordinate handling needed clarification.  

**Discussion:**  
The team discussed calculating geographic distance using stored coordinates to allow farmers to view lands closer to their location first.  

**Problem:** Distance calculation method.  

**Options Considered:**  
1. Simple Euclidean distance.  
2. Haversine formula.  
3. Geospatial database functions.  

**Debate:**  
Vivekanand wanted Haversine for accuracy, while Keerthi argued Euclidean is sufficient for local areas. Abhay suggested database functions.  

**Decision:** Haversine formula for accuracy.  

**Reason:** Indian agriculture spans large areas, accuracy matters.

#### Day 6
**Roles:**  
Product Owner – Vivekanand  
Scrum Master – Ajay Nageswara Rao  
Developers – Keerthi Ram Valluri, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Distance sorting partially implemented.  

**Today's Work:**  
Optimize database queries for marketplace listing performance (Task T19).  

**Blockers:** None  

**Discussion:**  
The team optimized query filtering and indexing to improve loading speed when displaying large numbers of land listings.  

**Problem:** Database indexing strategy.  

**Options Considered:**  
1. Composite indexes.  
2. Separate indexes.  
3. Full-text search.  

**Debate:**  
Abhay wanted composite indexes, while Ajay suggested full-text for search. Keerthi argued for balanced approach.  

**Decision:** Strategic composite indexes with full-text search.  

**Reason:** Optimal query performance for various access patterns.

**Sprint-3 goal achieved:**  
- Lease marketplace listing  
- Sale marketplace listing  
- Integrated marketplace feed  
- Distance-based sorting  
- Query optimization  

### 2.4 Sprint 4 - Daily Scrum

#### Day 1
**Roles:**  
Product Owner – Keerthi Ram Valluri  
Scrum Master – Ajay Nageswara Rao  
Developers – Abhay Gokavarapu, Vivekanand  

**Yesterday Completed Work:**  
Development paused during mid-semester examinations.  

**Today's Work:**  
Start Sprint-4.  
Begin implementing land lease application system for farmers (Task T21).  

**Blockers:** None  

**Discussion:**  
The Product Owner explained that farmers should be able to apply for lease directly from the marketplace listing page.  
The team discussed the required database fields for lease requests including applicant ID, land ID, application status, and request date.  

**Problem:** Application workflow complexity.  

**Options Considered:**  
1. Direct application.  
2. Application with proposal.  
3. Auction system.  

**Debate:**  
Vivekanand wanted proposals for better matching, while Keerthi preferred simple applications. Abhay suggested starting simple.  

**Decision:** Direct application with optional message.  

**Reason:** Lowers barrier for farmers while allowing communication.

#### Day 2
**Roles:**  
Product Owner – Vivekanand  
Scrum Master – Abhay Gokavarapu  
Developers – Keerthi Ram Valluri, Ajay Nageswara Rao  

**Yesterday Completed Work:**  
Lease application module development started.  

**Today's Work:**  
Complete backend for lease applications.  
Connect lease application feature with land listings.  

**Blockers:** None  

**Discussion:**  
Developers ensured that farmers can submit lease applications and that these requests are stored in the database with proper ownership mapping.  

**Problem:** Application status tracking.  

**Options Considered:**  
1. Simple approved/rejected.  
2. Multi-stage workflow.  
3. Negotiation phase.  

**Debate:**  
Ajay wanted negotiation, while Keerthi argued for simplicity. Abhay suggested multi-stage.  

**Decision:** Approved/Pending/Rejected with negotiation option.  

**Reason:** Allows flexibility while keeping core simple.

#### Day 3
**Roles:**  
Product Owner – Abhay Gokavarapu  
Scrum Master – Keerthi Ram Valluri  
Developers – Ajay Nageswara Rao, Vivekanand  

**Yesterday Completed Work:**  
Lease application API implemented.  

**Today's Work:**  
Implement land purchase application system for investors and buyers (Task T22).  

**Blockers:** None  

**Discussion:**  
The team discussed differentiating between lease applications and purchase applications while maintaining a common request workflow.  

**Problem:** Purchase negotiation process.  

**Options Considered:**  
1. Fixed price purchase.  
2. Offer/counteroffer.  
3. Auction system.  

**Debate:**  
Vivekanand wanted offers, while Abhay preferred fixed prices. Keerthi suggested simple purchase requests.  

**Decision:** Purchase requests with landowner acceptance.  

**Reason:** Matches lease model, simpler implementation.

#### Day 4
**Roles:**  
Product Owner – Ajay Nageswara Rao  
Scrum Master – Vivekanand  
Developers – Keerthi Ram Valluri, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Purchase application module development started.  

**Today's Work:**  
Complete purchase application workflow.  
Connect purchase requests with landowner dashboard.  

**Blockers:** None  

**Discussion:**  
Developers ensured that landowners can view purchase requests and decide whether to accept or reject them.  

**Problem:** Notification system for applications.  

**Options Considered:**  
1. Email notifications.  
2. In-app notifications.  
3. SMS alerts.  

**Debate:**  
Keerthi wanted in-app, while Abhay suggested email. Vivekanand argued for SMS for rural users.  

**Decision:** In-app notifications with email backup.  

**Reason:** Immediate feedback with reliable delivery.

#### Day 5
**Roles:**  
Product Owner – Abhay Gokavarapu  
Scrum Master – Keerthi Ram Valluri  
Developers – Ajay Nageswara Rao, Vivekanand  

**Yesterday Completed Work:**  
Purchase application system implemented.  

**Today's Work:**  
Integrate Leaflet map for geolocation visualization of lands (Task T23).  

**Blockers:** None  

**Discussion:**  
The team discussed using latitude and longitude stored in the land database to render map locations.  

**Problem:** Map library choice.  

**Options Considered:**  
1. Google Maps.  
2. OpenStreetMap with Leaflet.  
3. Mapbox.  

**Debate:**  
Ajay wanted Google Maps, while Vivekanand preferred open-source Leaflet. Keerthi argued for cost considerations.  

**Decision:** Leaflet with OpenStreetMap.  

**Reason:** Free, open-source, and sufficient for agricultural use.

#### Day 6
**Roles:**  
Product Owner – Keerthi Ram Valluri  
Scrum Master – Vivekanand  
Developers – Ajay Nageswara Rao, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Leaflet map integration started.  

**Today's Work:**  
Display land markers on the map (Task T24).  

**Blockers:** None  

**Discussion:**  
Developers implemented dynamic map markers so each registered land appears visually on the map.  

**Problem:** Marker clustering for dense areas.  

**Options Considered:**  
1. No clustering.  
2. Basic clustering.  
3. Advanced clustering with zoom.  

**Debate:**  
Abhay wanted advanced clustering, while Keerthi argued it's overkill. Ajay suggested basic clustering.  

**Decision:** Basic marker clustering.  

**Reason:** Improves performance without complexity.

#### Day 7
**Roles:**  
Product Owner – Ajay Nageswara Rao  
Scrum Master – Abhay Gokavarapu  
Developers – Keerthi Ram Valluri, Vivekanand  

**Yesterday Completed Work:**  
Map marker display completed.  

**Today's Work:**  
Complete pending distance-based sorting improvements (Task T26).  

**Blockers:** None  

**Discussion:**  
Developers refined sorting logic to ensure listings display correctly according to geographic distance.  

**Problem:** Performance of distance calculations.  

**Options Considered:**  
1. Calculate on-the-fly.  
2. Pre-compute distances.  
3. Database spatial functions.  

**Debate:**  
Vivekanand wanted pre-compute, while Keerthi preferred on-the-fly. Abhay suggested database functions.  

**Decision:** Database spatial functions where possible.  

**Reason:** Better performance and accuracy.

#### Day 8
**Roles:**  
Product Owner – Vivekanand  
Scrum Master – Keerthi Ram Valluri  
Developers – Ajay Nageswara Rao, Abhay Gokavarapu  

**Yesterday Completed Work:**  
Distance sorting improvements implemented.  

**Today's Work:**  
Begin lease agreement generation module (Task T25).  

**Blockers:** Discussion on agreement format.  

**Discussion:**  
The team discussed generating structured lease agreement documents containing land details, lease duration, payment terms, and involved parties.  

**Problem:** Agreement document format.  

**Options Considered:**  
1. PDF generation.  
2. HTML templates.  
3. Docx templates.  

**Debate:**  
Abhay wanted PDF for official look, while Ajay preferred HTML. Keerthi suggested docx for editability.  

**Decision:** PDF generation with templates.  

**Reason:** Professional appearance and legal acceptance.

#### Day 9
**Roles:**  
Product Owner – Abhay Gokavarapu  
Scrum Master – Keerthi Ram Valluri  
Developers – Ajay Nageswara Rao, Vivekanand  

**Yesterday Completed Work:**  
Lease agreement module development started.  

**Today's Work:**  
Continue implementing agreement generation logic.  
Prepare system for next sprint tasks.  

**Blockers:** None  

**Discussion:**  
The team verified that lease application, purchase application, and map visualization modules are functioning properly.  
Initial lease agreement generation logic has been implemented but requires refinement in the next sprint.  

**Problem:** Agreement customization needs.  

**Options Considered:**  
1. Standard template.  
2. Customizable fields.  
3. Full negotiation interface.  

**Debate:**  
Vivekanand wanted customization, while Keerthi argued for standard. Ajay suggested basic customization.  

**Decision:** Standard template with key field customization.  

**Reason:** Balances legal requirements with user needs.

## Chapter 3: Design & Workflow (Team)

### 3.1 Level-1

### 3.2 Level-2: UML Diagrams

#### 3.2.1. Sequence Diagram

#### 3.2.2 Interaction Diagram

#### 3.2.3 Activity Diagram

#### 3.2.4 Class Diagram

### 3.3 Level-3: Wireframes

Figma Prototype: Full User Flow Overview

[Screen descriptions remain the same as original]

## Chapter 4: System Architecture & Requirements

### 4.1 System Architecture

### 4.2 System Requirements