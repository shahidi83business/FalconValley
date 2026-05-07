<?xml version="1.0" ?>
<map version="1.0.1">
  <node TEXT="Game Frontend Architecture">
    <node TEXT="App Shell">
      <node TEXT="Router"/>
      <node TEXT="Global Layout"/>
      <node TEXT="Theme / UI System"/>
      <node TEXT="Notification System"/>
    </node>
    <node TEXT="Game Screens">
      <node TEXT="Lobby / Start Screen"/>
      <node TEXT="Scenario View"/>
      <node TEXT="Decision Panel"/>
      <node TEXT="Round Outcome Screen"/>
      <node TEXT="Session Summary"/>
    </node>
    <node TEXT="Scenario Rendering">
      <node TEXT="Narrative Text Renderer"/>
      <node TEXT="Dynamic Choice Generator"/>
      <node TEXT="Scenario Metadata Viewer"/>
    </node>
    <node TEXT="State Management">
      <node TEXT="Game Session State"/>
      <node TEXT="Round State"/>
      <node TEXT="Player History"/>
      <node TEXT="Trust / Reputation Indicators"/>
    </node>
    <node TEXT="API Layer">
      <node TEXT="Scenario Fetch API"/>
      <node TEXT="Decision Submit API"/>
      <node TEXT="Game State Sync"/>
      <node TEXT="Session Save"/>
    </node>
    <node TEXT="Core Components">
      <node TEXT="Choice Buttons"/>
      <node TEXT="Score Panel"/>
      <node TEXT="Opponent Indicator"/>
      <node TEXT="Timeline / History"/>
    </node>
    <node TEXT="Event Flow">
      <node TEXT="Scenario Loaded"/>
      <node TEXT="Player Decision"/>
      <node TEXT="Opponent Decision"/>
      <node TEXT="Economy Result"/>
      <node TEXT="State Update"/>
    </node>
    <node TEXT="Persistence">
      <node TEXT="Local Cache"/>
      <node TEXT="Session Restore"/>
      <node TEXT="Analytics Events"/>
    </node>
  </node>
</map>
