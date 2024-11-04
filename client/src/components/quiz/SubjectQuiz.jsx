// SubjectQuiz.jsx
import React, { useState, useEffect, useRef } from 'react';
import { useQuiz } from '../../context/QuizContext';
import ProgressBar from '../shared/ProgressBar';
import RadioGroup from '../shared/RadioGroup';
import QuizNavigation from '../shared/QuizNavigation';
import LoadingSpinner from '../shared/LoadingSpinner';
import Alert from '../shared/Alert';
import { subjects, getRandomQuestions } from '../../data/subjectQuestions';

const SubjectQuiz = () => {
  const { updateState, moveToNextSection, subjectAnswers: existingSubjectAnswers } = useQuiz();
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [currentAnswer, setCurrentAnswer] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState(new Array(50).fill(null));
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [subjectScores, setSubjectScores] = useState({
    Science: 0,
    Technology: 0,
    English: 0,
    Art: 0,
    Math: 0,
  });
  const [quizCompleted, setQuizCompleted] = useState(false);
  const stateUpdated = useRef(false);

  const totalQuestions = 50;

  useEffect(() => {
    try {
      const allQuestions = [];
      
      Object.keys(subjects).forEach(subject => {
        const subjectQuestions = getRandomQuestions(subject, 10);        
        allQuestions.push(...subjectQuestions);
      });

      setQuestions(allQuestions);
      setSubjectScores({
        Science: 0,
        Technology: 0,
        English: 0,
        Art: 0,
        Math: 0
      });
      setIsLoading(false);
    } catch (error) {
      console.error('Error loading questions:', error);
      setError('Failed to load quiz questions. Please try again.');
      setIsLoading(false);
    }
  }, []);

  const handleQuizCompletion = () => {
    if (!stateUpdated.current) {
      const finalSubjectResults = {
        subjectAnswers: answers
      };

      console.log('Completing subject quiz. Current state PASSED (DO NOT DELETE):', {
        newSubjectAnswers: answers.length,
        subjectScoresSummary: Object.entries(subjectScores)
          .map(([subject, score]) => `${subject}: ${score}/10`)
          .join(', ')
      });
      
      console.log('Sending to updateState:', finalSubjectResults);

      updateState(finalSubjectResults, () => {
        if (answers.length !== 50) {
          console.error('Invalid number of subject answers:', answers.length);
          setError('Failed to save subject quiz results. Please try again.');
          return;
        }
        
        stateUpdated.current = true;
        moveToNextSection();
      });
    }
  };

  useEffect(() => {
    if (quizCompleted) {
      handleQuizCompletion();
    }
  }, [quizCompleted]);

  const getCurrentSubject = () => {
    if (currentQuestion < 10) return 'Science';
    if (currentQuestion < 20) return 'Technology';
    if (currentQuestion < 30) return 'English';
    if (currentQuestion < 40) return 'Art';
    return 'Math';
  };

  const handleAnswer = (value) => {
    setCurrentAnswer(value);
  };

  const handleNext = () => {
    if (currentAnswer !== null) {
      const currentQuestionData = getCurrentQuestionData();
      const answerResult = checkAnswer(currentQuestionData, currentAnswer);
      const subject = getCurrentSubject();

      // Create new answers array
      const newAnswers = [...answers];
      newAnswers[currentQuestion] = answerResult;
      setAnswers(newAnswers);

      setSubjectScores(prev => {
        const newScores = { ...prev };
        const currentScore = Number(prev[subject] || 0);
        const newScore = currentScore + (answerResult ? 1 : 0);
        newScores[subject] = newScore;

        // If this is the last question
        if (currentQuestion === totalQuestions - 1) {
          // Create a structured scores object
          const scoreOutput = {
            answers: newAnswers.map((answer, index) => {
              const subject = Math.floor(index / 10);
              return {
                subject: ['Science', 'Technology', 'English', 'Art', 'Math'][subject],
                value: answer
              };
            }),
            scores: [
              { subject: 'Science', value: newScores.Science },
              { subject: 'Technology', value: newScores.Technology },
              { subject: 'English', value: newScores.English },
              { subject: 'Art', value: newScores.Art },
              { subject: 'Math', value: newScores.Math }
            ]
          };

          // console.log('Final question completed for SubjectQuiz:', 
          //   JSON.stringify(scoreOutput, null, 2)
          // );

          setQuizCompleted(true);
        }

        return newScores;
      });

      if (currentQuestion < totalQuestions - 1) {
        setCurrentQuestion(currentQuestion + 1);
        setCurrentAnswer(null);
      }
    }
  };

  const checkAnswer = (question, selectedAnswer) => {
    const options = getAnswerOptions();
    const selectedOption = options.find(opt => opt.value === selectedAnswer);
    const isCorrect = selectedOption?.label === question.correct_answer;
  
    // console.log(`Q${currentQuestion % 10 + 1} checkAnswer:  ${selectedOption?.label} - ${isCorrect ? 'True' : 'False'}`);

    return isCorrect
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
      const previousAnswer = answers[currentQuestion - 1];
      setCurrentAnswer(previousAnswer ? previousAnswer.selectedAnswer : null);
      updateState({
        progress: ((currentQuestion - 1) / totalQuestions * 100)
      });
    }
  };

  const getCurrentQuestionData = () => {
    if (!questions.length) return null;
    return questions[currentQuestion];
  };

  const getAnswerOptions = () => {
    const question = getCurrentQuestionData();
    if (!question) return [];

    const allAnswers = [
      question.correct_answer,
      ...question.incorrect_answers
    ];
    
    // Deterministic shuffle based on question text
    const shuffledAnswers = allAnswers
      .map((answer, index) => ({
        answer,
        sort: question.question.charCodeAt(index % question.question.length)
      }))
      .sort((a, b) => a.sort - b.sort)
      .map((item, index) => ({
        value: index + 1,
        label: item.answer
      }));

    return shuffledAnswers;
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-[200px]">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return <Alert type="error">{error}</Alert>;
  }

  const currentSubject = getCurrentSubject();
  const questionNumber = (currentQuestion % 10) + 1;
  const question = getCurrentQuestionData();

  if (!question) {
    return <Alert type="error">Failed to load quiz questions. Please try again.</Alert>;
  }

  const subjectProgress = ((questionNumber / 10) * 100).toFixed(0);
  const overallProgress = ((currentQuestion + 1) / totalQuestions * 100).toFixed(0);

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <ProgressBar progress={parseFloat(overallProgress)} total={100} />
        <div className="flex justify-between text-sm text-gray-600">
          <span>Overall Progress: {overallProgress}%</span>
          <span>{currentSubject} Progress: {subjectProgress}%</span>
        </div>
      </div>

      <div className="bg-white dark:bg-slate-800 rounded-lg p-6 shadow-sm">
        <h2 className="text-xl font-semibold mb-4">
          STEAM Subject Quiz
        </h2>
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <p className="text-gray-600 dark:text-gray-300">
              {currentSubject} - Question {questionNumber} of 10
            </p>
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
              {subjects[currentSubject].icon}
            </span>
          </div>

          <div className="p-4 bg-gray-50 dark:bg-slate-700 rounded-lg">
            <p className="text-lg font-medium mb-2">
              {question.question}
            </p>
            <p className="text-gray-600 dark:text-gray-300 text-sm">
              {subjects[currentSubject].description}
            </p>
          </div>

          <RadioGroup
            options={getAnswerOptions()}
            value={currentAnswer}
            onChange={handleAnswer}
            name="subject-answer"
          />

          <QuizNavigation
            onNext={handleNext}
            onPrev={handlePrevious}
            canProgress={currentAnswer !== null}
            showPrev={currentQuestion > 0}
          />
        </div>
      </div>
    </div>
  );
};

export default SubjectQuiz;