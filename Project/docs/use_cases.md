# GooseMarket Use Cases

## Student Use Cases

Use Case: Sign Up

Actor: Student
Goal: Create account using @uwaterloo.ca email
Preconditions: User not already registered

Main Flow:
Student opens Sign-Up page
System prompts for @uwaterloo.ca email
Student submits registration form
System validates email domain
System sends verification link

Postconditions: Account created, pending verification
Exceptions: Invalid email domain → registration denied

Use Case: Verify Email

Actor: Student
Goal: Confirm account ownership
Preconditions: Verification email sent

Main Flow:
Student opens verification email
Student clicks verification link
System validates token
System activates GooseMarket account

Postconditions: Account verified and active
Exceptions: Expired or invalid link → resend verification

Use Case: Secure Login

Actor: Student
Goal: Access GooseMarket account securely
Preconditions: Account verified

Main Flow:
Student enters credentials
System authenticates credentials
System logs user into dashboard

Postconditions: Student session active
Exceptions: Wrong credentials → show error

Use Case: Receive Login Bonus

Actor: Student
Goal: Earn Goose Dollars for logging in
Preconditions: Successful login

Main Flow:
System checks last login date
System awards Goose Dollars if eligible
System updates student balance

Postconditions: Student balance increased
Exceptions: Already rewarded today → no bonus

Use Case: Earn Participation Rewards

Actor: Student
Goal: Gain Goose Dollars from ongoing engagement
Preconditions: Account active

Main Flow:
Student completes platform interactions
System tracks participation metrics
System grants reward when threshold met

Postconditions: Additional Goose Dollars added
Exceptions: Suspicious activity → reward withheld

Use Case: Browse Events

Actor: Student
Goal: Explore open prediction events
Preconditions: Logged in

Main Flow:
Student opens Events page
System displays list of open events
System updates list dynamically

Postconditions: Events visible to student
Exceptions: No events available → show placeholder

Use Case: Filter Events

Actor: Student
Goal: Find events by category or group
Preconditions: Events available

Main Flow:
Student selects filter options
System refines event list
Student views filtered results

Postconditions: Relevant events displayed
Exceptions: No matches found → show “no results”

Use Case: View Event Details

Actor: Student
Goal: Review event information before predicting
Preconditions: Event selected

Main Flow:
System loads event page
System displays description, odds, activity
Student reviews event information

Postconditions: Student informed about event
Exceptions: Event unavailable → show error

Use Case: Create Prediction Event

Actor: Student
Goal: Propose a new community prediction
Preconditions: Logged in

Main Flow:
Student opens “Create Event” form
Student enters title, options, and description
System validates input
System submits event for admin approval

Postconditions: Event pending moderator review
Exceptions: Invalid or incomplete data → show error

Use Case: Buy/Sell Shares

Actor: Student
Goal: Participate in prediction market
Preconditions: Event open, sufficient balance

Main Flow:
Student selects event option
Student enters Goose Dollar amount
System processes trade
System updates holdings and balance

Postconditions: Student position updated
Exceptions: Insufficient balance → trade denied

Use Case: View Positions

Actor: Student
Goal: Track current event investments
Preconditions: Active trades exist

Main Flow:
Student opens portfolio
System displays list of active positions
System shows performance metrics

Postconditions: Student sees up-to-date holdings
Exceptions: No active positions → show empty state

Use Case: Quick Access to Event from Position

Actor: Student
Goal: Manage predictions directly from portfolio
Preconditions: Active positions exist

Main Flow:
Student clicks a position
System navigates to corresponding event page

Postconditions: Event details loaded
Exceptions: Event resolved or removed → show notice

Use Case: View Profile

Actor: Student
Goal: See stats and trade history
Preconditions: Logged in

Main Flow:
Student opens profile
System loads statistics, balance, and trade log

Postconditions: Profile data displayed
Exceptions: Profile data load error → retry

Use Case: View Leaderboard

Actor: Student
Goal: Compare performance with others
Preconditions: Sufficient player data

Main Flow:
Student selects Leaderboard
System ranks users by Goose Dollars
System displays top performers

Postconditions: Leaderboard visible
Exceptions: No rankings yet → show placeholder

Use Case: Join Groups

Actor: Student
Goal: Participate within faculty or community group
Preconditions: Logged in

Main Flow:
Student opens Groups section
System lists available groups
Student selects group to join
System updates membership

Postconditions: Student joined group
Exceptions: Already a member → show notice

Use Case: Subscribe to Event Tags

Actor: Student
Goal: Get updates on topics of interest
Preconditions: Logged in

Main Flow:
Student browses event tags
Student subscribes to chosen tags
System records subscriptions

Postconditions: Notifications enabled for tags
Exceptions: Subscription error → retry

Use Case: Access Help / Tutorial

Actor: Student
Goal: Learn how GooseMarket works
Preconditions: None

Main Flow:
Student opens Help section
System displays tutorial or guide

Postconditions: Student better understands platform
Exceptions: Help page not loaded → show error

Use Case: View Tooltips / UI Guidance

Actor: Student
Goal: Understand features through inline hints
Preconditions: Logged in

Main Flow:
System shows contextual tooltips
Student interacts with UI
System highlights new or complex actions

Postconditions: Student learns feature usage
Exceptions: Tooltip disabled → none shown

Use Case: Report Suspicious Activity

Actor: Student
Goal: Notify moderators of abuse or cheating
Preconditions: Logged in

Main Flow:
Student opens report form
Student submits report
System logs case for moderator review

Postconditions: Report received by admin
Exceptions: Invalid or duplicate report → ignored

Use Case: Handle Disputes Fairly

Actor: Student
Goal: Submit or review event disputes
Preconditions: Event outcome contested

Main Flow:
Student submits dispute
System logs dispute for admin handling
Admin reviews evidence and responds

Postconditions: Dispute processed
Exceptions: Missing data → request clarification

Use Case: Login Streak Bonuses

Actor: Student
Goal: Earn rewards for consistent logins
Preconditions: Logged in

Main Flow:
System tracks consecutive login days
System calculates bonus
System updates balance

Postconditions: Student receives streak bonus
Exceptions: Streak broken → reset count

## Admin / Moderator Use-Case Models

Use Case: Moderator Login

Actor: Admin / Moderator
Goal: Access moderator tools securely
Preconditions: Moderator account exists

Main Flow:
Moderator enters credentials
System authenticates
System loads moderator dashboard

Postconditions: Moderator session active
Exceptions: Invalid credentials → access denied

Use Case: Approve or Reject Events

Actor: Moderator
Goal: Control which events go live
Preconditions: Event submitted for review

Main Flow:
Moderator opens pending event list
Moderator reviews event details
Moderator approves or rejects event
System updates event status

Postconditions: Event either published or rejected
Exceptions: Incomplete info → request edits

Use Case: Edit Events Before Approval

Actor: Moderator
Goal: Correct unclear or inappropriate event details
Preconditions: Event pending review

Main Flow:
Moderator edits title or description
System saves revisions
Moderator finalizes approval decision

Postconditions: Updated event ready for publication
Exceptions: Invalid edit → show error

Use Case: Resolve Event Outcomes

Actor: Moderator
Goal: Finalize result and trigger payouts
Preconditions: Event concluded

Main Flow:
Moderator reviews evidence
Moderator selects correct outcome
System processes payouts

Postconditions: Winners credited, event closed
Exceptions: Unclear result → defer resolution

Use Case: Reverse Payouts

Actor: Moderator
Goal: Fix incorrect distribution
Preconditions: Event already resolved

Main Flow:
Moderator selects event
Moderator triggers reversal
System restores balances
System re-applies corrected payout

Postconditions: Balances corrected
Exceptions: Unauthorized action → denied

Use Case: Review Suspicious Reports

Actor: Moderator
Goal: Investigate potential cheating or abuse
Preconditions: Reports submitted

Main Flow:
Moderator opens Reports dashboard
System displays flagged users/events
Moderator reviews logs and evidence

Postconditions: Case reviewed and acted upon
Exceptions: Insufficient data → mark as inconclusive

Use Case: Suspend Accounts

Actor: Moderator
Goal: Temporarily restrict abusive users
Preconditions: Verified rule violation

Main Flow:
Moderator selects user
Moderator applies restriction
System blocks access for set duration

Postconditions: User suspended
Exceptions: Admin override → suspension canceled

Use Case: View Alerts

Actor: Moderator
Goal: Detect abnormal or suspicious activity
Preconditions: Monitoring active

Main Flow:
System generates alerts
Moderator reviews flagged events
Moderator follows up if needed

Postconditions: Alerts reviewed or dismissed
Exceptions: False positive → mark safe

Use Case: Access Moderator Dashboard

Actor: Moderator
Goal: Manage users and events efficiently
Preconditions: Logged in

Main Flow:
Moderator opens dashboard
System shows overview of pending and active items
Moderator navigates between tools

Postconditions: Moderator controls platform state
Exceptions: Dashboard load error → retry

Use Case: Handle Disputes

Actor: Moderator
Goal: Ensure fairness in event outcomes
Preconditions: Dispute submitted

Main Flow:
Moderator reviews dispute
Moderator checks logs and communications
Moderator issues decision

Postconditions: Dispute resolved and logged
Exceptions: Ambiguous data → request clarification

Use Case: Monitor Reward Abuse

Actor: Moderator
Goal: Prevent exploitation of login or streak bonuses
Preconditions: Reward data logged

Main Flow:
System flags unusual reward patterns
Moderator reviews user history
Moderator adjusts balances if needed

Postconditions: Reward system integrity maintained
Exceptions: False alarm → no action taken

Use Case: Access System Logs

Actor: Moderator
Goal: Investigate major system actions
Preconditions: Admin privileges granted

Main Flow:
Moderator opens log viewer
System displays records of transactions and actions
Moderator filters and exports data

Postconditions: Logs reviewed for audit
Exceptions: Missing log entries → notify dev team

System-Level Use-Case Model
Use Case: Maintain Security and Fairness

Actor: GooseMarket Platform
Goal: Protect user data and ensure fair play
Preconditions: System operational

Main Flow:
System enforces secure authentication
System monitors suspicious activity
System prevents duplicate or automated actions
System ensures accurate payout logic

Postconditions: Platform integrity maintained
Exceptions: Detected breach → trigger security response