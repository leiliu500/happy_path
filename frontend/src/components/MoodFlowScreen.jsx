import React, { useState, useEffect } from 'react';
import { productionMoodFlowData } from '../mockData/moodFlowMockData';

const MoodFlowScreen = () => {
  const [currentPhase, setCurrentPhase] = useState('acknowledgment');
  const [fadeIn, setFadeIn] = useState(false);
  
  const { 
    moodEntry, 
    healingInsights, 
    healingGoals, 
    healingFlow, 
    safetyAssessment 
  } = productionMoodFlowData;

  useEffect(() => {
    setFadeIn(true);
  }, []);

  const getMoodEmoji = (mood) => {
    if (mood >= 8) return "😊";
    if (mood >= 6) return "🙂";
    if (mood >= 4) return "😐";
    if (mood >= 2) return "😔";
    return "😢";
  };

  const getAnxietyColor = (level) => {
    if (level <= 1) return "#4CAF50";
    if (level <= 2) return "#8BC34A";
    if (level <= 3) return "#FFC107";
    if (level <= 4) return "#FF9800";
    return "#F44336";
  };

  const renderAcknowledgment = () => (
    <div className={`healing-acknowledgment ${fadeIn ? 'fade-in' : ''}`}>
      <div className="healing-header">
        <div className="healing-icon">🌱</div>
        <h1>{healingFlow.immediate.acknowledgment.title}</h1>
        <p className="healing-message">
          {healingFlow.immediate.acknowledgment.message}
        </p>
      </div>

      <div className="mood-summary-card">
        <div className="mood-display">
          <div className="mood-emoji-large">
            {getMoodEmoji(moodEntry.mood.overall)}
          </div>
          <div className="mood-details">
            <h3>Today's Check-in</h3>
            <div className="mood-value">
              <span className="mood-number">{moodEntry.mood.overall}</span>
              <span className="mood-scale">/10</span>
            </div>
            <p className="mood-validation">
              {healingFlow.immediate.acknowledgment.moodValidation}
            </p>
          </div>
        </div>

        <div className="emotional-landscape">
          <h4>Your Emotional Landscape</h4>
          <div className="emotion-grid">
            <div className="emotion-item">
              <span className="emotion-label">Anxiety</span>
              <div className="emotion-indicator">
                <div 
                  className="emotion-level" 
                  style={{
                    width: `${(moodEntry.mood.anxiety / 5) * 100}%`,
                    backgroundColor: getAnxietyColor(moodEntry.mood.anxiety)
                  }}
                ></div>
              </div>
              <span className="emotion-value">{moodEntry.mood.anxiety}/5</span>
            </div>
            <div className="emotion-item">
              <span className="emotion-label">Energy</span>
              <div className="emotion-indicator">
                <div 
                  className="emotion-level" 
                  style={{
                    width: `${(moodEntry.mood.energy / 5) * 100}%`,
                    backgroundColor: "#4CAF50"
                  }}
                ></div>
              </div>
              <span className="emotion-value">{moodEntry.mood.energy}/5</span>
            </div>
            <div className="emotion-item">
              <span className="emotion-label">Stress</span>
              <div className="emotion-indicator">
                <div 
                  className="emotion-level" 
                  style={{
                    width: `${(moodEntry.mood.stress / 5) * 100}%`,
                    backgroundColor: "#FF9800"
                  }}
                ></div>
              </div>
              <span className="emotion-value">{moodEntry.mood.stress}/5</span>
            </div>
          </div>
        </div>
      </div>

      <div className="primary-healing-suggestion">
        <div className="suggestion-icon">🌿</div>
        <div className="suggestion-content">
          <h3>{healingFlow.immediate.healingSuggestion.primary.title}</h3>
          <p>{healingFlow.immediate.healingSuggestion.primary.description}</p>
          <div className="suggestion-meta">
            <span className="duration">{healingFlow.immediate.healingSuggestion.primary.duration}</span>
            <span className="healing-intent">For {healingFlow.immediate.healingSuggestion.primary.healingIntent.replace('_', ' ')}</span>
          </div>
        </div>
        <button 
          className="primary-healing-btn"
          onClick={() => setCurrentPhase('breathing_exercise')}
        >
          Begin Breathing
        </button>
      </div>

      <div className="secondary-suggestions">
        {healingFlow.immediate.healingSuggestion.secondary.map((suggestion, index) => (
          <button 
            key={index}
            className="secondary-healing-btn"
            onClick={() => setCurrentPhase(suggestion.action)}
          >
            <span className="suggestion-title">{suggestion.title}</span>
            <span className="suggestion-duration">{suggestion.duration}</span>
          </button>
        ))}
      </div>

      <div className="continue-journey">
        <button 
          className="continue-btn"
          onClick={() => setCurrentPhase('healing_practices')}
        >
          Continue Healing Journey
        </button>
      </div>
    </div>
  );

  const renderBreathingExercise = () => (
    <div className="breathing-healing-space">
      <div className="breathing-header">
        <button 
          className="back-healing-btn" 
          onClick={() => setCurrentPhase('acknowledgment')}
        >
          ← Return to Check-in
        </button>
        <h2>Anxiety-Soothing Breath Work</h2>
        <p>Let's calm your nervous system together</p>
      </div>

      <div className="breathing-guide-container">
        <div className="breathing-circle-healing">
          <div className="inner-healing-circle">
            <span className="breath-instruction">Breathe slowly</span>
            <span className="breath-count">4-7-8</span>
          </div>
        </div>

        <div className="breathing-instructions-healing">
          <h3>4-7-8 Technique</h3>
          <div className="instruction-steps">
            <div className="step">
              <span className="step-number">1</span>
              <span className="step-text">Inhale through nose for 4 counts</span>
            </div>
            <div className="step">
              <span className="step-number">2</span>
              <span className="step-text">Hold breath for 7 counts</span>
            </div>
            <div className="step">
              <span className="step-number">3</span>
              <span className="step-text">Exhale through mouth for 8 counts</span>
            </div>
          </div>
          
          <div className="healing-benefits">
            <h4>Healing Benefits</h4>
            <ul>
              <li>Activates your parasympathetic nervous system</li>
              <li>Reduces cortisol (stress hormone) levels</li>
              <li>Increases confidence and inner calm</li>
              <li>Prepares your body and mind for success</li>
            </ul>
          </div>
        </div>

        <div className="breathing-controls-healing">
          <button className="start-breathing-btn">
            🌿 Start Guided Breathing
          </button>
          <button 
            className="skip-to-insights-btn"
            onClick={() => setCurrentPhase('healing_practices')}
          >
            Continue to Healing Practices
          </button>
        </div>
      </div>
    </div>
  );

  const renderHealingPractices = () => (
    <div className="healing-practices-container">
      <div className="practices-header">
        <button 
          className="back-healing-btn" 
          onClick={() => setCurrentPhase('acknowledgment')}
        >
          ← Back to Check-in
        </button>
        <h2>Your Personalized Healing Practices</h2>
        <p>Evidence-based practices tailored to your current emotional state</p>
      </div>

      <div className="practices-grid">
        {healingFlow.nextSteps.healingPractices.map((practice, index) => (
          <div key={index} className="practice-card">
            <div className="practice-header">
              <h3>{practice.title}</h3>
              <span className="practice-type">{practice.type.replace('_', ' ')}</span>
            </div>
            
            <p className="practice-description">{practice.description}</p>
            
            <div className="practice-benefits">
              <h4>Healing Benefits</h4>
              <ul>
                {practice.benefits.map((benefit, i) => (
                  <li key={i}>{benefit}</li>
                ))}
              </ul>
            </div>
            
            <div className="practice-meta">
              <span className="practice-duration">{practice.duration}</span>
              <span className="practice-difficulty">{practice.difficulty}</span>
            </div>
            
            <button className="practice-start-btn">
              Begin Practice
            </button>
          </div>
        ))}
      </div>

      <div className="reflective-questions-section">
        <h3>Gentle Self-Reflection</h3>
        <p>Take a moment to explore these healing questions:</p>
        <div className="questions-list">
          {healingFlow.nextSteps.reflectiveQuestions.map((question, index) => (
            <div key={index} className="question-card">
              <span className="question-icon">💭</span>
              <p>{question}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="healing-insights-section">
        <h3>Your Healing Insights</h3>
        <div className="insights-wellness-score">
          <div className="score-display-healing">
            <span className="score-label">Wellness Growth</span>
            <div className="score-value">
              <span className="score-number">{healingInsights.wellnessAssessment.wellnessScore}</span>
              <span className="score-change positive">+{healingInsights.wellnessAssessment.scoreChange}%</span>
            </div>
            <span className="score-description">Your healing journey is creating positive change</span>
          </div>
        </div>

        <div className="personal-patterns">
          <h4>Your Personal Healing Patterns</h4>
          <div className="patterns-grid">
            {healingInsights.healingPatterns.insights.map((insight, index) => (
              <div key={index} className="pattern-insight">
                <span className="insight-icon">✨</span>
                <p>{insight}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="healing-reminders-section">
        <h3>Healing Reminders for Today</h3>
        <div className="reminders-list">
          {healingFlow.nextSteps.healingReminders.map((reminder, index) => (
            <div key={index} className="reminder-card">
              <div className="reminder-time">{reminder.time}</div>
              <div className="reminder-content">
                <p>{reminder.message}</p>
                <button className="reminder-action-btn">
                  {reminder.action.replace('_', ' ')}
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderCurrentPhase = () => {
    switch(currentPhase) {
      case 'acknowledgment':
        return renderAcknowledgment();
      case 'breathing_exercise':
      case 'guided_breathing':
        return renderBreathingExercise();
      case 'healing_practices':
      case 'strength_reflection':
      case 'intention_setting':
        return renderHealingPractices();
      default:
        return renderAcknowledgment();
    }
  };

  return (
    <div className="mood-flow-healing-container">
      {renderCurrentPhase()}
    </div>
  );
};

export default MoodFlowScreen;
