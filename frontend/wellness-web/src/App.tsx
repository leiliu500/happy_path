import React from 'react';
import './globals.css';

function App() {
  const [currentMood, setCurrentMood] = React.useState(7);

  const wellnessFocusAreas = [
    { 
      title: 'Stress & Anxiety', 
      description: 'Find calm in moments of overwhelm',
      icon: '🧘‍♀️',
      color: 'var(--color-calm)'
    },
    { 
      title: 'Depression Support', 
      description: 'Gentle guidance through difficult times',
      icon: '💚',
      color: 'var(--color-growth)'
    },
    { 
      title: 'Sleep & Rest', 
      description: 'Restore your body and mind',
      icon: '🌙',
      color: 'var(--color-peace)'
    },
    { 
      title: 'Personal Growth', 
      description: 'Discover your inner strength',
      icon: '🌱',
      color: 'var(--color-wisdom)'
    },
  ];

  const activities = [
    { title: '3-Minute Breathing', duration: '3 min', icon: '🫁' },
    { title: 'Guided Meditation', duration: '10 min', icon: '🧘' },
    { title: 'Gratitude Journal', duration: '5 min', icon: '📝' },
    { title: 'Calming Music', duration: '15 min', icon: '🎵' },
  ];

  return (
    <div className="app-container">
      {/* Header */}
      <header style={{
        background: 'var(--color-primary-gradient)',
        color: 'white',
        padding: 'var(--spacing-xl)',
        textAlign: 'center',
        position: 'relative',
        overflow: 'hidden'
      }}>
        <div style={{ position: 'relative', zIndex: 2 }}>
          <div className="wellness-icon breathing-element" style={{
            width: '80px',
            height: '80px',
            fontSize: '40px',
            margin: '0 auto var(--spacing-lg)',
            background: 'rgba(255, 255, 255, 0.2)',
            backdropFilter: 'blur(10px)'
          }}>
            🌸
          </div>
          <h1 className="font-display text-4xl" style={{ marginBottom: 'var(--spacing-sm)' }}>
            Welcome to HappyPath
          </h1>
          <p className="text-lg" style={{ opacity: 0.9 }}>
            Your professional mental wellness journey begins here
          </p>
        </div>
        
        {/* Floating elements */}
        <div style={{
          position: 'absolute',
          top: '20%',
          left: '10%',
          fontSize: '24px',
          opacity: 0.3,
          animation: 'breathe 3s ease-in-out infinite'
        }}>✨</div>
        <div style={{
          position: 'absolute',
          top: '60%',
          right: '15%',
          fontSize: '20px',
          opacity: 0.3,
          animation: 'breathe 4s ease-in-out infinite'
        }}>🦋</div>
      </header>

      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: 'var(--spacing-xl)' }}>
        
        {/* Quick Mood Check */}
        <section className="healing-card" style={{ marginBottom: 'var(--spacing-2xl)' }}>
          <h2 className="font-display text-2xl text-healing-primary" style={{ marginBottom: 'var(--spacing-lg)' }}>
            How are you feeling right now?
          </h2>
          
          <div style={{ textAlign: 'center', marginBottom: 'var(--spacing-lg)' }}>
            <div style={{ 
              fontSize: '48px', 
              marginBottom: 'var(--spacing-sm)',
              filter: 'drop-shadow(0 4px 8px rgba(0,0,0,0.1))'
            }}>
              {currentMood <= 3 ? '😢' : currentMood <= 5 ? '😐' : currentMood <= 7 ? '🙂' : '😊'}
            </div>
            <div className="text-lg text-healing-primary" style={{ fontWeight: '600' }}>
              {currentMood <= 3 ? 'Struggling' : currentMood <= 5 ? 'Okay' : currentMood <= 7 ? 'Good' : 'Great'}
            </div>
          </div>

          <div style={{ position: 'relative', margin: 'var(--spacing-lg) 0' }}>
            <input 
              type="range" 
              min="1" 
              max="10" 
              value={currentMood}
              onChange={(e) => setCurrentMood(parseInt(e.target.value))}
              style={{
                width: '100%',
                height: '8px',
                borderRadius: '4px',
                background: `linear-gradient(to right, 
                  var(--color-danger) 0%, 
                  var(--color-warning) 50%, 
                  var(--color-success) 100%)`,
                outline: 'none',
                cursor: 'pointer'
              }}
            />
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginTop: 'var(--spacing-sm)',
              fontSize: 'var(--font-size-sm)',
              color: 'var(--color-text-secondary)'
            }}>
              <span>Low</span>
              <span>High</span>
            </div>
          </div>

          <button className="wellness-button wellness-button-primary" style={{ width: '100%' }}>
            Save My Mood
          </button>
        </section>

        {/* Wellness Focus Areas */}
        <section style={{ marginBottom: 'var(--spacing-2xl)' }}>
          <h2 className="font-display text-2xl text-healing-primary" style={{ 
            marginBottom: 'var(--spacing-lg)',
            textAlign: 'center'
          }}>
            Choose Your Wellness Focus
          </h2>
          
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: 'var(--spacing-lg)'
          }}>
            {wellnessFocusAreas.map((area, index) => (
              <div key={index} className="healing-card" style={{
                textAlign: 'center',
                padding: 'var(--spacing-xl)',
                cursor: 'pointer',
                transition: 'all var(--transition-base)',
                background: `linear-gradient(135deg, ${area.color}08 0%, ${area.color}15 100%)`
              }}>
                <div style={{ 
                  fontSize: '48px', 
                  marginBottom: 'var(--spacing-md)',
                  filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))'
                }}>
                  {area.icon}
                </div>
                <h3 className="text-xl" style={{ 
                  marginBottom: 'var(--spacing-sm)',
                  color: 'var(--color-text-primary)',
                  fontWeight: '600'
                }}>
                  {area.title}
                </h3>
                <p style={{ 
                  color: 'var(--color-text-secondary)',
                  lineHeight: '1.5'
                }}>
                  {area.description}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Quick Activities */}
        <section style={{ marginBottom: 'var(--spacing-2xl)' }}>
          <h2 className="font-display text-2xl text-healing-primary" style={{ 
            marginBottom: 'var(--spacing-lg)',
            textAlign: 'center'
          }}>
            Start Your Healing Journey Now
          </h2>
          
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
            gap: 'var(--spacing-md)'
          }}>
            {activities.map((activity, index) => (
              <div key={index} className="healing-card" style={{
                display: 'flex',
                alignItems: 'center',
                padding: 'var(--spacing-lg)',
                cursor: 'pointer',
                background: 'var(--color-background)',
                border: '2px solid var(--color-border)',
                transition: 'all var(--transition-base)'
              }}>
                <div style={{ 
                  fontSize: '32px', 
                  marginRight: 'var(--spacing-md)',
                  filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))'
                }}>
                  {activity.icon}
                </div>
                <div style={{ flex: 1 }}>
                  <h4 style={{ 
                    fontWeight: '600',
                    marginBottom: 'var(--spacing-xs)',
                    color: 'var(--color-text-primary)'
                  }}>
                    {activity.title}
                  </h4>
                  <p style={{ 
                    fontSize: 'var(--font-size-sm)',
                    color: 'var(--color-text-secondary)'
                  }}>
                    {activity.duration}
                  </p>
                </div>
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: 'var(--color-primary)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontSize: '16px'
                }}>
                  ▶
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Call to Action */}
        <section className="healing-card" style={{
          textAlign: 'center',
          padding: 'var(--spacing-2xl)',
          background: 'var(--color-primary-gradient)',
          color: 'white',
          position: 'relative',
          overflow: 'hidden'
        }}>
          <div style={{ position: 'relative', zIndex: 2 }}>
            <h2 className="font-display text-3xl" style={{ marginBottom: 'var(--spacing-lg)' }}>
              Ready to Transform Your Wellbeing?
            </h2>
            <p className="text-lg" style={{ 
              marginBottom: 'var(--spacing-xl)',
              opacity: 0.9,
              maxWidth: '600px',
              margin: '0 auto var(--spacing-xl)'
            }}>
              Join thousands who have found peace, growth, and healing through our evidence-based wellness platform.
            </p>
            
            <div style={{
              display: 'flex',
              gap: 'var(--spacing-md)',
              justifyContent: 'center',
              flexWrap: 'wrap'
            }}>
              <button className="wellness-button" style={{
                background: 'rgba(255, 255, 255, 0.2)',
                color: 'white',
                border: '2px solid rgba(255, 255, 255, 0.3)',
                backdropFilter: 'blur(10px)'
              }}>
                Start Free Journey
              </button>
              <button className="wellness-button" style={{
                background: 'rgba(255, 255, 255, 0.1)',
                color: 'white',
                border: '2px solid rgba(255, 255, 255, 0.3)'
              }}>
                Learn More
              </button>
            </div>
          </div>

          {/* Background decoration */}
          <div style={{
            position: 'absolute',
            top: '-50px',
            right: '-50px',
            width: '200px',
            height: '200px',
            borderRadius: '50%',
            background: 'rgba(255, 255, 255, 0.1)',
            animation: 'breathe 6s ease-in-out infinite'
          }}></div>
        </section>
      </div>

      {/* Footer */}
      <footer style={{
        background: 'var(--color-surface)',
        padding: 'var(--spacing-xl)',
        textAlign: 'center',
        marginTop: 'var(--spacing-3xl)',
        borderTop: '1px solid var(--color-border)'
      }}>
        <p style={{ color: 'var(--color-text-secondary)' }}>
          © 2025 HappyPath. Professional mental wellness platform designed for healing and growth.
        </p>
      </footer>
    </div>
  );
}

export default App;
