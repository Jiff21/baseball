"""
Environment configuration for behave BDD tests
"""

def before_all(context):
    """Setup before all tests"""
    context.config.setup_logging()

def before_scenario(context, scenario):
    """Setup before each scenario"""
    # Reset any context variables
    context.extracted_wins = None
    context.extracted_losses = None
    context.standings_data = None
    context.stats_extractor = None

def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    pass

def after_all(context):
    """Cleanup after all tests"""
    pass
