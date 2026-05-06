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
    print("Generating context narrative...")
    print("Updating player internal state...")
    print("Updating opponent perception...")
    print("Setting economic frame...")
    print("Presenting decision moment...")

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
    print("Updating reputation...")
    print("Updating trust...")
    print("Updating risk preference...")
    print("Storing round decisions...")
    print("Persisting to database...")

def feedback_player(feedback):
    print("Showing outcome narrative...")
    print("Displaying payoff...")
    print("Displaying reputation change...")

def check_session(session):
    print("Checking if max rounds reached, player exit, or scenario completed...")
    return True  # Placeholder for continuation logic

def next_round(round):
    print("Looping back to round start...")

def end_session(session):
    print("Calculating total profit...")
    print("Updating player progression...")
    print("Storing session summary...")

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
