from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import date

class GoalMetric(BaseModel):
    goal: str
    kpi: str
    target: str

class UserPersonaScenario(BaseModel):
    persona: str
    scenario: str

class UserStoryAcceptanceCriteria(BaseModel):
    given: str
    when: str
    then: str

class UserStory(BaseModel):
    epic: str
    story_id: str
    as_a: str
    i_want: str
    so_that: str
    acceptance_criteria: List[UserStoryAcceptanceCriteria]

class FunctionalRequirements(BaseModel):
    epics: List[str]
    user_stories: List[UserStory]

class NonFunctionalRequirement(BaseModel):
    category: str
    requirement: str

class ReleaseMilestone(BaseModel):
    version: str
    target_date: Optional[date]
    description: str

class OutOfScopeItem(BaseModel):
    version: str
    items: List[str]

class FutureWorkItem(BaseModel):
    description: str

class AppendixItem(BaseModel):
    type: str  # 'Open Question', 'Dependency', etc.
    content: str

class ProductRequirementsDocument(BaseModel):
    # Metadata
    product_name: str
    status: str
    author: str
    version: str
    last_updated: date

    # 1. Executive Summary & Vision
    executive_summary_vision: str

    # 2. The Problem
    problem_statement: str
    user_personas_scenarios: List[UserPersonaScenario]

    # 3. Goals & Success Metrics
    goals_and_metrics: List[GoalMetric]

    # 4. Functional Requirements & User Stories
    functional_requirements: FunctionalRequirements

    # 5. Non-Functional Requirements
    non_functional_requirements: List[NonFunctionalRequirement]

    # 6. Release Plan & Milestones
    release_plan_milestones: List[ReleaseMilestone]

    # 7. Out of Scope & Future Considerations
    out_of_scope: List[str]
    future_work: List[str]

    # 8. Appendix & Open Questions
    appendix: List[AppendixItem]