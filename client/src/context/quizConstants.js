// Quiz sections in order of progression
export const QUIZ_SECTIONS = [
  'menu',
  'username',
  'personality',
  'personality-tiebreaker',
  'subject',
  'subject-tiebreaker',
  'results',
  'network-board'
];

// Initial state for the quiz context
export const INITIAL_STATE = {
  section: 'menu',
  username: '',
  traitPercentages: null,
  needsPersonalityTieBreaker: false,
  personalityTies: [],
  preferredTrait: null,
  subjectPercentages: null,
  needsSubjectTieBreaker: false,
  subjectTies: [],
  preferredSubject: null,
  // The following fields are implemented after the quiz is submitted
  bestSubject: '',
  subjectScore: 0,
  bestPersonalityTrait: '',
  personalityScore: 0,
  preferredEnvironment: '',
  dateOfSubmission: ''
};

// Tolerance for considering scores as tied (percentage points)
// for example, if the score is 50.001, it will be considered 50
export const SCORE_TOLERANCE = 5; 