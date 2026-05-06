from core import ChainManager
from db_helper import EconomyFunction

def start_game_session(session):
    # Load player profile
    user = User.objects.first()
    if not user:
        print("No user found. Creating a new user...")
        user = User(username="default_user")
        user.save()

    # Load reputation
    profile = UserProfile.objects(user=user).first()
    if not profile:
        print("No profile found. Creating a new profile...")
        profile = UserProfile(user=user)
        profile.save()

    # Load risk preference
    print("Loading risk preference...")
    # Placeholder: Add logic to fetch or initialize risk preference

    # Initialize session state
    session = RoundSession(user=user, status=StatusEnum.in_progress)
    session.save()
    print("Session initialized with ID:", session.id)

def initialiaze_scenario(scenario):
    # Select category
    category = Category.objects.first()
    if not category:
        print("No category found. Creating a default category...")
        category = Category(name="Default Category", description="Default description")
        category.save()

    # Load scenario template
    scenario = Scenario.objects(category=category).first()
    if not scenario:
        print("No scenario found for the category. Creating a default scenario...")
        scenario = Scenario(text="Default Scenario", options=["Option 1", "Option 2"], category=category)
        scenario.save()

    # Load economy function pipeline
    economy_function = EconomyFunction.objects(category=category).first()
    if not economy_function:
        print("No economy function found for the category. Creating a default economy function...")
        economy_function = EconomyFunction(name="Default Economy Function", category=category, parameters={})
        economy_function.save()

    # Initialize opponent strategy
    opponent = Opponent.objects.first()
    if not opponent:
        print("No opponent found. Creating a default opponent...")
        opponent = Opponent(strategy_key="default_strategy", parameters={})
        opponent.save()

    print("Scenario initialized with category:", category.name)

def start_round(round):
    print("Incrementing round counter...")
    print("Loading previous history...")
    print("Building current game state...")

def generate_scenario(scenario):
    import openai
    from models import Scenario, UserProfile, Opponent

    # Fetch or create a scenario
    scenario = Scenario.objects.first()
    if not scenario:
        print("No scenario found. Creating a default scenario...")
        scenario = Scenario(text="Default Scenario", options=["Option 1", "Option 2"], correct_option=0)
        scenario.save()

    # Fetch player profile and opponent
    player_profile = UserProfile.objects.first()
    opponent = Opponent.objects.first()

    # Connect to GPT API for narrative generation
    openai.api_key = "your_openai_api_key_here"
    prompt = f"Generate a narrative scenario based on the following details:\nPlayer Profile: {player_profile}\nOpponent: {opponent}\nScenario: {scenario.text}"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )
        narrative = response.choices[0].text.strip()
        print("Generated Narrative:", narrative)

        # Update scenario with the generated narrative
        scenario.text = narrative
        scenario.save()

    except Exception as e:
        print("Error generating narrative:", e)

def make_decision(player, decision):
    print("Player is making a decision: Cooperate or Defect...")
    print("Recording player choice...")

def check_economy_engine(opponent):
    print("Evaluating opponent strategy...")
    print("Using history to generate action...")

def calculate_outcome(economy):
    # Fetch all economy functions from the database
    economy_functions = EconomyFunction.objects()

    # Convert database functions to method chain
    method_chain = [(func.path, func.name) for func in economy_functions]

    # Create a ChainManager instance
    chain_manager = ChainManager(method_chain)

    # Execute the chain with initial arguments
    result = chain_manager.execute(method="eco1")
    print("Economic engine result:", result)

def update_state(state):
    from models import UserProfile, Round, Decision

    # Fetch the current user profile
    profile = UserProfile.objects.first()
    if not profile:
        print("No user profile found. Cannot update state.")
        return

    # Update reputation (placeholder logic)
    print("Updating reputation for user:", profile.user.username)
    # Placeholder: Add logic to calculate and update reputation

    # Update trust (placeholder logic)
    print("Updating trust for user:", profile.user.username)
    # Placeholder: Add logic to calculate and update trust

    # Update risk preference (placeholder logic)
    print("Updating risk preference for user:", profile.user.username)
    # Placeholder: Add logic to calculate and update risk preference

    # Store round decisions
    current_round = Round.objects().order_by('-created_at').first()
    if current_round:
        print("Storing decisions for round ID:", current_round.id)
        # Placeholder: Add logic to store decisions

    # Persist changes to database
    print("Persisting updated state to database...")

def feedback_player(feedback):
    print("Showing outcome narrative...")
    print("Displaying payoff...")
    print("Displaying reputation change...")

def check_session(session):
    print("Checking if max rounds reached, player exit, or scenario completed...")
    return True  # Placeholder for continuation logic

def next_round(round):
    from models import Round, UserProfile

    # Fetch the current round
    current_round = Round.objects().order_by('-created_at').first()
    if not current_round:
        print("No current round found. Initializing a new round...")
        profile = UserProfile.objects.first()
        current_round = Round(profile=profile, created_at=now())
        current_round.save()

    # Increment round counter (placeholder logic)
    print("Starting next round with ID:", current_round.id)
    # Placeholder: Add logic to reset or prepare the state for the next round

def end_session(session):
    from models import RoundSession, UserProfile

    # Fetch the current session
    session = RoundSession.objects(status="in_progress").first()
    if not session:
        print("No active session found to end.")
        return

    # Calculate total profit (placeholder logic)
    total_profit = 100  # Replace with actual calculation logic
    print("Total profit calculated:", total_profit)

    # Update player progression
    profile = UserProfile.objects(user=session.user).first()
    if profile:
        print("Updating player progression for user:", session.user.username)
        # Placeholder: Add logic to update progression based on total_profit

    # Mark session as completed
    session.status = "completed"
    session.ended_at = now()
    session.save()
    print("Session ended and summary stored with ID:", session.id)

def game_loop():
    # Game Session Start
    start_game_session("session")

    while True:
        # Scenario Initialization
        initialiaze_scenario("scenario")

        # Round Start
        start_round("round")

        # Scenario Generation
        generate_scenario("scenario")

        # Player Decision
        make_decision("player", "decision")

        # Opponent Decision
        check_economy_engine("opponent")

        # Economy Engine
        calculate_outcome("economy")

        # Outcome Calculation
        update_state("state")

        # Feedback to Player
        feedback_player("feedback")

        # Check Continuation
        if not check_session("session"):
            break

        # Next Round
        next_round("round")

    # End Session
    end_session("session")
