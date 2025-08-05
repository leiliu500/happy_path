import React, { useState, useEffect } from 'react';
import MoodSavedScreen from '../components/MoodSavedScreen';
import '../styles/MoodSavedScreen.css';

const MoodFlowDemo = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Simulate the mood saving process
    setTimeout(() => setIsVisible(true), 500);
  }, []);

  if (!isVisible) {
    return (
      <div className="demo-loading">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <h3>Saving your mood...</h3>
          <p>Processing your wellness data</p>
        </div>
      </div>
    );
  }

  return (
    <div className="mood-flow-demo">
      <div className="demo-header">
        <h1>Mood Tracking Flow Demo</h1>
        <p>Experience the complete user journey after saving mood data</p>
      </div>
      
      <MoodSavedScreen />
      
      <div className="demo-footer">
        <div className="flow-explanation">
          <h3>🔄 Complete Mood Tracking Flow</h3>
          <div className="flow-steps">
            <div className="flow-step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h4>Immediate Feedback</h4>
                <p>User receives instant confirmation and wellness score update</p>
              </div>
            </div>
            <div className="flow-step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h4>AI Analysis & Insights</h4>
                <p>Background processing generates personalized recommendations</p>
              </div>
            </div>
            <div className="flow-step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h4>Goal Progress Update</h4>
                <p>Automatic tracking of wellness goals and streak maintenance</p>
              </div>
            </div>
            <div className="flow-step">
              <div className="step-number">4</div>
              <div className="step-content">
                <h4>Recommended Actions</h4>
                <p>Personalized next steps based on current mood and patterns</p>
              </div>
            </div>
            <div className="flow-step">
              <div className="step-number">5</div>
              <div className="step-content">
                <h4>Community Integration</h4>
                <p>Optional sharing and connection with support network</p>
              </div>
            </div>
          </div>
        </div>

        <div className="technical-features">
          <h3>🔧 Technical Implementation Features</h3>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🧠</div>
              <h4>AI-Powered Insights</h4>
              <p>Real-time mood analysis with pattern recognition and correlation detection</p>
              <ul>
                <li>Crisis detection algorithms</li>
                <li>Mood-sleep correlation analysis</li>
                <li>Personalized recommendations</li>
                <li>Trend pattern recognition</li>
              </ul>
            </div>

            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h4>Data Analytics</h4>
              <p>Comprehensive wellness tracking with intelligent insights</p>
              <ul>
                <li>Real-time score calculations</li>
                <li>Multi-factor correlation analysis</li>
                <li>Goal progress tracking</li>
                <li>Achievement system</li>
              </ul>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🎯</div>
              <h4>Progressive Engagement</h4>
              <p>Adaptive user experience based on engagement patterns</p>
              <ul>
                <li>Personalized onboarding</li>
                <li>Feature unlocking system</li>
                <li>Habit formation support</li>
                <li>Community integration</li>
              </ul>
            </div>

            <div className="feature-card">
              <div className="feature-icon">🔐</div>
              <h4>Privacy & Security</h4>
              <p>Privacy-first design with user data control</p>
              <ul>
                <li>End-to-end encryption</li>
                <li>Anonymous community features</li>
                <li>User-controlled data sharing</li>
                <li>GDPR/HIPAA compliance</li>
              </ul>
            </div>
          </div>
        </div>

        <div className="user-flow-summary">
          <h3>📱 User Flow Summary</h3>
          <div className="flow-diagram">
            <div className="flow-item">
              <div className="flow-icon">💾</div>
              <span>Save Mood</span>
            </div>
            <div className="flow-arrow">→</div>
            <div className="flow-item">
              <div className="flow-icon">✅</div>
              <span>Immediate Feedback</span>
            </div>
            <div className="flow-arrow">→</div>
            <div className="flow-item">
              <div className="flow-icon">🧠</div>
              <span>AI Analysis</span>
            </div>
            <div className="flow-arrow">→</div>
            <div className="flow-item">
              <div className="flow-icon">🎯</div>
              <span>Goal Updates</span>
            </div>
            <div className="flow-arrow">→</div>
            <div className="flow-item">
              <div className="flow-icon">💡</div>
              <span>Recommendations</span>
            </div>
            <div className="flow-arrow">→</div>
            <div className="flow-item">
              <div className="flow-icon">🚀</div>
              <span>Next Actions</span>
            </div>
          </div>
        </div>

        <div className="data-structure-info">
          <h3>📄 Mock Data Structure</h3>
          <div className="data-tabs">
            <div className="data-tab">
              <h4>Mood Entry</h4>
              <pre className="code-block">
{`{
  entryId: "mood_67890",
  userId: "user_12345", 
  overallMood: 7,
  anxietyLevel: "mild",
  stressLevel: "moderate",
  emotions: ["hopeful", "focused"],
  triggers: ["work_presentation"],
  copingStrategies: ["deep_breathing"],
  notes: "Feeling confident...",
  wellnessScore: 73
}`}
              </pre>
            </div>

            <div className="data-tab">
              <h4>AI Insights</h4>
              <pre className="code-block">
{`{
  wellnessScore: 73,
  scoreChange: +15,
  riskLevel: "low",
  correlations: {
    sleepMoodCorrelation: 0.82,
    exerciseMoodCorrelation: 0.67
  },
  recommendations: [
    {
      type: "breathing_exercise",
      priority: "high",
      title: "2-min breathing"
    }
  ]
}`}
              </pre>
            </div>

            <div className="data-tab">
              <h4>Goal Progress</h4>
              <pre className="code-block">
{`{
  activeGoals: [
    {
      name: "Daily Mood Check-ins",
      currentStreak: 5,
      successRate: 100,
      progress: {
        thisWeek: 5,
        target: 7
      }
    }
  ]
}`}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MoodFlowDemo;
