import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import MoodFlowScreen from './components/MoodFlowScreen';
import './styles/MoodFlowScreen.css';

const App = () => {
  return (
    <Router>
      <div className="app">
        <Routes>
          {/* Professional mood flow */}
          <Route path="/mood-flow" element={<MoodFlowScreen />} />
          
          {/* Landing page */}
          <Route path="/" element={<LandingPage />} />
        </Routes>
      </div>
    </Router>
  );
};

const LandingPage = () => (
  <div className="landing-page">
    <div className="landing-container">
      <header className="landing-header">
        <h1>🌱 Happy Path - Professional Mood Tracking</h1>
        <p>A healing-focused approach to mental wellness monitoring</p>
      </header>

      <div className="demo-links">
        <div className="link-card featured">
          <h3>� Healing-Focused Mood Flow</h3>
          <p>Experience our professional, production-ready mood tracking system with healing themes</p>
          <Link to="/mood-flow" className="demo-link primary">
            Experience Mood Flow
          </Link>
        </div>
      </div>

      <div className="feature-highlights">
        <h2>✨ Healing-Centered Features</h2>
        <div className="highlights-grid">
          <div className="highlight-item">
            <div className="highlight-icon">�</div>
            <h4>Healing Acknowledgment</h4>
            <p>Every mood entry is met with compassion and validation</p>
          </div>
          <div className="highlight-item">
            <div className="highlight-icon">🧘‍♀️</div>
            <h4>Evidence-Based Interventions</h4>
            <p>Personalized breathing exercises and mindfulness practices</p>
          </div>
          <div className="highlight-item">
            <div className="highlight-icon">📈</div>
            <h4>Growth-Oriented Analytics</h4>
            <p>Insights that highlight healing patterns and progress</p>
          </div>
          <div className="highlight-item">
            <div className="highlight-icon">🛡️</div>
            <h4>Safety-First Design</h4>
            <p>Comprehensive crisis prevention and professional integration</p>
          </div>
          <div className="highlight-item">
            <div className="highlight-icon">💝</div>
            <h4>Reflective Practices</h4>
            <p>Guided questions and gratitude exercises for deeper healing</p>
          </div>
          <div className="highlight-item">
            <div className="highlight-icon">🎯</div>
            <h4>Personalized Goals</h4>
            <p>Healing-focused goals that support emotional regulation</p>
          </div>
        </div>
      </div>

      <div className="technical-overview">
        <h2>🔧 Professional Features</h2>
        <div className="tech-list">
          <div className="tech-item">
            <span className="tech-icon">🌿</span>
            <span>Healing-themed UI with calming color psychology</span>
          </div>
          <div className="tech-item">
            <span className="tech-icon">🔬</span>
            <span>Evidence-based intervention recommendations</span>
          </div>
          <div className="tech-item">
            <span className="tech-icon">🔒</span>
            <span>HIPAA-compliant data structures and privacy controls</span>
          </div>
          <div className="tech-item">
            <span className="tech-icon">📊</span>
            <span>Comprehensive mood analytics and pattern recognition</span>
          </div>
          <div className="tech-item">
            <span className="tech-icon">🚨</span>
            <span>Crisis detection and safety planning integration</span>
          </div>
          <div className="tech-item">
            <span className="tech-icon">👩‍⚕️</span>
            <span>Professional therapy integration and referral system</span>
          </div>
        </div>
      </div>

      <footer className="landing-footer">
        <p>Professional Mental Wellness Platform</p>
        <p>Combining clinical best practices with healing-centered design</p>
      </footer>
    </div>
  </div>
);

// Landing page styles
const landingStyles = `
.landing-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.landing-container {
  max-width: 1000px;
  margin: 0 auto;
  color: white;
}

.landing-header {
  text-align: center;
  margin-bottom: 48px;
}

.landing-header h1 {
  margin: 0 0 16px 0;
  font-size: 36px;
  font-weight: 700;
}

.landing-header p {
  margin: 0;
  font-size: 18px;
  opacity: 0.9;
}

.demo-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 48px;
}

.link-card {
  background: rgba(255,255,255,0.1);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(10px);
  text-align: center;
}

.link-card h3 {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 600;
}

.link-card p {
  margin: 0 0 20px 0;
  font-size: 14px;
  opacity: 0.9;
  line-height: 1.5;
}

.demo-link {
  display: inline-block;
  padding: 12px 24px;
  border-radius: 24px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.2s ease;
}

.demo-link.primary {
  background: white;
  color: #667eea;
}

.demo-link.secondary {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1px solid rgba(255,255,255,0.3);
}

.demo-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
}

.feature-highlights {
  margin-bottom: 48px;
}

.feature-highlights h2 {
  text-align: center;
  margin: 0 0 32px 0;
  font-size: 28px;
  font-weight: 600;
}

.highlights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
}

.highlight-item {
  background: rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  backdrop-filter: blur(5px);
}

.highlight-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.highlight-item h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
}

.highlight-item p {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
  line-height: 1.4;
}

.technical-overview {
  margin-bottom: 48px;
}

.technical-overview h2 {
  text-align: center;
  margin: 0 0 32px 0;
  font-size: 28px;
  font-weight: 600;
}

.tech-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 16px;
}

.tech-item {
  background: rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
  backdrop-filter: blur(5px);
}

.tech-icon {
  font-size: 20px;
  flex-shrink: 0;
}

.landing-footer {
  text-align: center;
  opacity: 0.8;
  margin-top: 48px;
}

.landing-footer p {
  margin: 8px 0;
  font-size: 14px;
}

@media (max-width: 768px) {
  .landing-header h1 {
    font-size: 28px;
  }
  
  .landing-header p {
    font-size: 16px;
  }
  
  .demo-links {
    grid-template-columns: 1fr;
  }
  
  .highlights-grid {
    grid-template-columns: 1fr;
  }
  
  .tech-list {
    grid-template-columns: 1fr;
  }
}
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.type = 'text/css';
styleSheet.innerText = landingStyles;
document.head.appendChild(styleSheet);

export default App;
