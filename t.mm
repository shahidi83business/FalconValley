<map version=“1.0.1”>

<node TEXT=“Game Loop (MVP)”>

<node TEXT=“Game Session Start”>

<node TEXT=“Load Player Profile”/>

<node TEXT=“Load Reputation”/>

<node TEXT=“Load Risk Preference”/>

<node TEXT=“Initialize Session State”/>

</node>

<node TEXT=“Scenario Initialization”>

<node TEXT=“Select Category”/>

<node TEXT=“Load Scenario Template”/>

<node TEXT=“Load Economy Function Pipeline”/>

<node TEXT=“Initialize Opponent Strategy”/>

</node>

<node TEXT=“Round Start”>

<node TEXT=“Increment Round Counter”/>

<node TEXT=“Load Previous History”/>

<node TEXT=“Build Current Game State”/>

</node>

<node TEXT=“Scenario Generation”>

<node TEXT=“Context Narrative”/>

<node TEXT=“Player Internal State”/>

<node TEXT=“Opponent Perception”/>

<node TEXT=“Economic Frame”/>

<node TEXT=“Decision Moment”/>

</node>

<node TEXT=“Player Decision”>

<node TEXT=“Option: Cooperate”/>

<node TEXT=“Option: Defect”/>

<node TEXT=“Record Player Choice”/>

</node>

<node TEXT=“Opponent Decision”>

<node TEXT=“Strategy Evaluation”/>

<node TEXT=“Use History”/>

<node TEXT=“Generate Action”/>

</node>

<node TEXT=“Economy Engine”>

<node TEXT=“Execute Function Pipeline”>

<node TEXT=“Base Payoff”>

<node TEXT=“PrisonerPayoff”/>

</node>

<node TEXT=“Risk Layer”>

<node TEXT=“RiskUtility”/>

<node TEXT=“ProspectTheory”/>

<node TEXT=“UncertaintyNoise”/>

</node>

<node TEXT=“Reputation Layer”>

<node TEXT=“ReputationUpdate”/>

<node TEXT=“TrustUpdate”/>

</node>

<node TEXT=“Future Impact”>

<node TEXT=“DiscountUpdate”/>

<node TEXT=“FuturePayoffModifier”/>

</node>

</node>

</node>

<node TEXT=“Outcome Calculation”>

<node TEXT=“Compute Player Payoff”/>

<node TEXT=“Compute Opponent Payoff”/>

<node TEXT=“Update Profit”/>

</node>

<node TEXT=“State Update”>

<node TEXT=“Update Reputation”/>

<node TEXT=“Update Trust”/>

<node TEXT=“Update Risk Preference”/>

<node TEXT=“Store Round Decisions”/>

<node TEXT=“Persist to Database”/>

</node>

<node TEXT=“Feedback to Player”>

<node TEXT=“Show Outcome Narrative”/>

<node TEXT=“Display Payoff”/>

<node TEXT=“Display Reputation Change”/>

</node>

<node TEXT=“Check Continuation”>

<node TEXT=“Max Rounds Reached?”/>

<node TEXT=“Player Exit?”/>

<node TEXT=“Scenario Completed?”/>

</node>

<node TEXT=“Next Round”>

<node TEXT=“Loop Back to Round Start”/>

</node>

<node TEXT=“Session End”>

<node TEXT=“Calculate Total Profit”/>

<node TEXT=“Update Player Progression”/>

<node TEXT=“Store Session Summary”/>

</node>

</node>

</map>