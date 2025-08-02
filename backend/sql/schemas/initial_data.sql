-- Initial Data / Seed Data for Happy Path Mental Health Application
-- Run this AFTER all schema files have been executed successfully
-- This file contains essential data needed for the application to function

-- =============================================================================
-- SYSTEM CONFIGURATIONS
-- =============================================================================

INSERT INTO system_configurations (config_key, config_value, config_category, config_description, data_type, environment) VALUES
    -- Application Configuration
    ('app.name', 'Happy Path', 'application', 'Application name', 'string', 'production'),
    ('app.version', '1.0.0', 'application', 'Current application version', 'string', 'production'),
    ('app.environment', 'production', 'application', 'Current environment', 'string', 'production'),
    ('app.maintenance_mode', 'false', 'application', 'Enable maintenance mode', 'boolean', 'production'),
    
    -- Crisis Detection Configuration
    ('crisis.detection.enabled', 'true', 'crisis', 'Enable crisis detection features', 'boolean', 'production'),
    ('crisis.detection.sensitivity', '0.75', 'crisis', 'Crisis detection sensitivity threshold (0-1)', 'float', 'production'),
    ('crisis.auto_escalation.enabled', 'true', 'crisis', 'Enable automatic escalation for high-risk cases', 'boolean', 'production'),
    ('crisis.response_time.target_minutes', '5', 'crisis', 'Target response time for crisis interventions', 'integer', 'production'),
    
    -- Security Configuration
    ('security.session.timeout_minutes', '60', 'security', 'User session timeout in minutes', 'integer', 'production'),
    ('security.password.min_length', '8', 'security', 'Minimum password length', 'integer', 'production'),
    ('security.password.require_special_chars', 'true', 'security', 'Require special characters in passwords', 'boolean', 'production'),
    ('security.login.max_attempts', '5', 'security', 'Maximum failed login attempts before lockout', 'integer', 'production'),
    ('security.lockout.duration_minutes', '30', 'security', 'Account lockout duration in minutes', 'integer', 'production'),
    ('security.2fa.enabled', 'true', 'security', 'Enable two-factor authentication option', 'boolean', 'production'),
    
    -- Privacy and Data Retention
    ('privacy.data_retention.default_days', '2555', 'privacy', 'Default data retention period (7 years for medical data)', 'integer', 'production'),
    ('privacy.data_retention.mood_entries_days', '2555', 'privacy', 'Mood entries retention period', 'integer', 'production'),
    ('privacy.data_retention.journal_entries_days', '2555', 'privacy', 'Journal entries retention period', 'integer', 'production'),
    ('privacy.data_retention.chat_messages_days', '2555', 'privacy', 'Chat messages retention period', 'integer', 'production'),
    ('privacy.data_retention.audit_logs_days', '2555', 'privacy', 'Audit logs retention period', 'integer', 'production'),
    ('privacy.anonymization.auto_enabled', 'true', 'privacy', 'Enable automatic data anonymization for research', 'boolean', 'production'),
    
    -- AI Configuration
    ('ai.model.primary', 'gpt-4', 'ai', 'Primary AI model for conversations', 'string', 'production'),
    ('ai.model.crisis_detection', 'custom-crisis-v1', 'ai', 'AI model for crisis detection', 'string', 'production'),
    ('ai.response.max_tokens', '1000', 'ai', 'Maximum tokens per AI response', 'integer', 'production'),
    ('ai.response.temperature', '0.7', 'ai', 'AI response creativity/randomness (0-2)', 'float', 'production'),
    ('ai.moderation.enabled', 'true', 'ai', 'Enable AI content moderation', 'boolean', 'production'),
    ('ai.learning.user_feedback_enabled', 'true', 'ai', 'Enable learning from user feedback', 'boolean', 'production'),
    
    -- Notification Configuration
    ('notifications.email.enabled', 'true', 'notifications', 'Enable email notifications', 'boolean', 'production'),
    ('notifications.sms.enabled', 'true', 'notifications', 'Enable SMS notifications', 'boolean', 'production'),
    ('notifications.push.enabled', 'true', 'notifications', 'Enable push notifications', 'boolean', 'production'),
    ('notifications.crisis.immediate', 'true', 'notifications', 'Send immediate notifications for crisis situations', 'boolean', 'production'),
    
    -- Feature Flags
    ('features.mood_tracking.enabled', 'true', 'features', 'Enable mood tracking features', 'boolean', 'production'),
    ('features.journaling.enabled', 'true', 'features', 'Enable journaling features', 'boolean', 'production'),
    ('features.chat_agent.enabled', 'true', 'features', 'Enable AI chat agent', 'boolean', 'production'),
    ('features.therapy_integration.enabled', 'true', 'features', 'Enable therapist integration features', 'boolean', 'production'),
    ('features.crisis_detection.enabled', 'true', 'features', 'Enable crisis detection and intervention', 'boolean', 'production'),
    ('features.analytics.enabled', 'true', 'features', 'Enable analytics and insights', 'boolean', 'production'),
    
    -- Integration Configuration
    ('integration.twilio.enabled', 'false', 'integration', 'Enable Twilio SMS integration', 'boolean', 'production'),
    ('integration.sendgrid.enabled', 'false', 'integration', 'Enable SendGrid email integration', 'boolean', 'production'),
    ('integration.stripe.enabled', 'false', 'integration', 'Enable Stripe payment integration', 'boolean', 'production');

-- =============================================================================
-- CRISIS RESOURCES (Hotlines and Support Services)
-- =============================================================================

INSERT INTO crisis_resources (
    resource_name, resource_type, phone_number, text_number, website_url, 
    available_24_7, available_hours, timezone, target_demographics, 
    languages_supported, geographic_coverage, crisis_types, specialized_for, 
    verified, is_active, display_priority
) VALUES
    -- National US Crisis Resources
    ('988 Suicide & Crisis Lifeline', 'hotline', '988', NULL, 'https://988lifeline.org', 
     true, '24/7', 'UTC', ARRAY['all'], ARRAY['en', 'es'], ARRAY['US'], 
     ARRAY['suicidal_ideation', 'severe_depression'], ARRAY['suicide', 'mental_health_crisis'], 
     true, true, 1),
     
    ('Crisis Text Line', 'text_line', NULL, '741741', 'https://crisistextline.org', 
     true, '24/7', 'UTC', ARRAY['teens', 'adults'], ARRAY['en', 'es'], ARRAY['US', 'CA', 'UK'], 
     ARRAY['suicidal_ideation', 'self_harm', 'severe_depression'], ARRAY['suicide', 'self_harm', 'crisis_support'], 
     true, true, 2),
     
    ('SAMHSA National Helpline', 'hotline', '1-800-662-4357', NULL, 'https://samhsa.gov', 
     true, '24/7', 'UTC', ARRAY['all'], ARRAY['en', 'es'], ARRAY['US'], 
     ARRAY['substance_abuse'], ARRAY['substance_abuse', 'addiction', 'mental_health'], 
     true, true, 3),
     
    ('National Domestic Violence Hotline', 'hotline', '1-800-799-7233', '22522', 'https://thehotline.org', 
     true, '24/7', 'UTC', ARRAY['all'], ARRAY['en', 'es'], ARRAY['US'], 
     ARRAY['domestic_violence'], ARRAY['domestic_violence', 'intimate_partner_violence'], 
     true, true, 4),
     
    ('National Sexual Assault Hotline', 'hotline', '1-800-656-4673', NULL, 'https://rainn.org', 
     true, '24/7', 'UTC', ARRAY['all'], ARRAY['en', 'es'], ARRAY['US'], 
     ARRAY['trauma_response'], ARRAY['sexual_assault', 'trauma'], 
     true, true, 5),
     
    -- Specialized Resources
    ('Veterans Crisis Line', 'hotline', '1-800-273-8255', '838255', 'https://veteranscrisisline.net', 
     true, '24/7', 'UTC', ARRAY['veterans'], ARRAY['en', 'es'], ARRAY['US'], 
     ARRAY['suicidal_ideation', 'severe_depression', 'ptsd'], ARRAY['veterans', 'military', 'ptsd'], 
     true, true, 6),
     
    ('Trans Lifeline', 'hotline', '877-565-8860', NULL, 'https://translifeline.org', 
     false, 'Daily 10 AM - 4 AM EST', 'EST', ARRAY['lgbtq'], ARRAY['en', 'es'], ARRAY['US', 'CA'], 
     ARRAY['suicidal_ideation', 'severe_depression'], ARRAY['transgender', 'lgbtq', 'suicide'], 
     true, true, 7),
     
    ('National Eating Disorders Association', 'hotline', '1-800-931-2237', NULL, 'https://nationaleatingdisorders.org', 
     false, 'Monday-Thursday 11 AM - 9 PM, Friday 11 AM - 5 PM EST', 'EST', ARRAY['all'], ARRAY['en', 'es'], ARRAY['US'], 
     ARRAY['eating_disorder'], ARRAY['eating_disorders', 'body_image'], 
     true, true, 8),
     
    -- Teen/Youth Resources
    ('Teen Line', 'hotline', '310-855-4673', '839863', 'https://teenline.org', 
     false, 'Daily 6 PM - 10 PM PST', 'PST', ARRAY['teens'], ARRAY['en', 'es'], ARRAY['US'], 
     ARRAY['suicidal_ideation', 'self_harm', 'severe_depression'], ARRAY['teens', 'adolescents', 'peer_support'], 
     true, true, 9),
     
    ('JED Campus Support', 'website', NULL, NULL, 'https://jedfoundation.org', 
     true, '24/7', 'UTC', ARRAY['teens', 'college_students'], ARRAY['en'], ARRAY['US'], 
     ARRAY['suicidal_ideation', 'severe_depression'], ARRAY['college_students', 'mental_health'], 
     true, true, 10);

-- =============================================================================
-- CRISIS KEYWORDS AND PATTERNS
-- =============================================================================

INSERT INTO crisis_keywords (
    keyword_phrase, crisis_type, severity_weight, context_required, 
    is_regex, case_sensitive, word_boundary_required, is_active
) VALUES
    -- High Severity Suicidal Ideation Keywords
    ('kill myself', 'suicidal_ideation', 1.0, false, false, false, true, true),
    ('end my life', 'suicidal_ideation', 1.0, false, false, false, true, true),
    ('want to die', 'suicidal_ideation', 0.95, false, false, false, true, true),
    ('going to kill myself', 'suicidal_ideation', 1.0, false, false, false, false, true),
    ('planning to die', 'suicidal_ideation', 0.9, false, false, false, true, true),
    ('suicide plan', 'suicidal_ideation', 0.95, false, false, false, true, true),
    ('end it all', 'suicidal_ideation', 0.85, false, false, false, true, true),
    ('take my own life', 'suicidal_ideation', 0.9, false, false, false, false, true),
    
    -- Moderate Severity Suicidal Ideation
    ('better off dead', 'suicidal_ideation', 0.8, false, false, false, true, true),
    ('wish I was dead', 'suicidal_ideation', 0.8, false, false, false, false, true),
    ('no reason to live', 'suicidal_ideation', 0.75, false, false, false, false, true),
    ('nothing to live for', 'suicidal_ideation', 0.75, false, false, false, false, true),
    ('world better without me', 'suicidal_ideation', 0.7, false, false, false, false, true),
    
    -- Self-Harm Keywords
    ('hurt myself', 'self_harm', 0.8, false, false, false, true, true),
    ('cutting myself', 'self_harm', 0.9, false, false, false, false, true),
    ('self harm', 'self_harm', 0.85, false, false, false, true, true),
    ('burning myself', 'self_harm', 0.85, false, false, false, false, true),
    ('punish myself', 'self_harm', 0.6, true, false, false, false, true),
    ('deserve pain', 'self_harm', 0.65, true, false, false, false, true),
    
    -- Severe Depression Indicators
    ('completely hopeless', 'severe_depression', 0.7, false, false, false, false, true),
    ('no hope left', 'severe_depression', 0.7, false, false, false, false, true),
    ('totally worthless', 'severe_depression', 0.65, false, false, false, false, true),
    ('hate myself', 'severe_depression', 0.6, false, false, false, false, true),
    ('complete failure', 'severe_depression', 0.55, true, false, false, false, true),
    ('cannot go on', 'severe_depression', 0.65, false, false, false, false, true),
    ('too much pain', 'severe_depression', 0.6, true, false, false, false, true),
    
    -- Substance Abuse Crisis
    ('overdose', 'substance_abuse', 0.9, false, false, false, true, true),
    ('too much drugs', 'substance_abuse', 0.7, false, false, false, false, true),
    ('drinking too much', 'substance_abuse', 0.6, true, false, false, false, true),
    ('cannot stop using', 'substance_abuse', 0.75, false, false, false, false, true),
    
    -- Domestic Violence
    ('being hurt by', 'domestic_violence', 0.7, true, false, false, false, true),
    ('afraid of partner', 'domestic_violence', 0.8, false, false, false, false, true),
    ('partner threatens me', 'domestic_violence', 0.85, false, false, false, false, true),
    ('scared to go home', 'domestic_violence', 0.75, true, false, false, false, true),
    
    -- Eating Disorder Crisis
    ('starving myself', 'eating_disorder', 0.8, false, false, false, false, true),
    ('purging', 'eating_disorder', 0.75, true, false, false, true, true),
    ('binge eating', 'eating_disorder', 0.6, true, false, false, false, true),
    ('obsessed with weight', 'eating_disorder', 0.6, true, false, false, false, true),
    
    -- Psychotic Episode Indicators
    ('hearing voices', 'psychotic_episode', 0.85, false, false, false, false, true),
    ('voices telling me', 'psychotic_episode', 0.9, false, false, false, false, true),
    ('people following me', 'psychotic_episode', 0.7, true, false, false, false, true),
    ('paranoid', 'psychotic_episode', 0.6, true, false, false, true, true),
    
    -- Panic Attack Indicators
    ('cannot breathe', 'panic_attack', 0.7, true, false, false, false, true),
    ('heart racing', 'panic_attack', 0.5, true, false, false, false, true),
    ('panic attack', 'panic_attack', 0.8, false, false, false, false, true),
    ('feeling dizzy', 'panic_attack', 0.4, true, false, false, false, true);

-- =============================================================================
-- AI AGENT CONFIGURATIONS
-- =============================================================================

INSERT INTO ai_agent_configs (
    config_name, version, personality_type, empathy_level, formality_level, 
    enthusiasm_level, response_length_preference, question_frequency, 
    validation_frequency, primary_therapeutic_approach, intervention_aggressiveness, 
    crisis_sensitivity, use_metaphors, use_humor, use_personal_examples, 
    educational_content_frequency, default_temperature, max_tokens, system_prompt, 
    target_age_groups, target_conditions, is_active, requires_supervision
) VALUES
    -- Empathetic General Support Agent
    ('Empathetic Support Agent', '1.0', 'empathetic', 0.9, 0.4, 0.6, 
     'medium', 0.4, 0.8, 'humanistic', 0.3, 0.9, true, false, false, 
     0.2, 0.7, 1000, 
     'You are a compassionate AI mental health companion. Your role is to provide emotional support, active listening, and gentle guidance. Always validate feelings, show empathy, and guide users toward professional help when needed. Maintain a warm, caring tone while being professional. If you detect any crisis language, immediately offer crisis resources and encourage professional help.',
     ARRAY['adults', 'seniors'], ARRAY['anxiety', 'depression', 'general_wellness'], true, false),
     
    -- Professional CBT-Focused Agent
    ('CBT Professional Agent', '1.0', 'professional', 0.7, 0.8, 0.4, 
     'long', 0.6, 0.6, 'cbt', 0.6, 0.8, false, false, false, 
     0.4, 0.6, 1200, 
     'You are a professional AI assistant specializing in Cognitive Behavioral Therapy techniques. Help users identify thought patterns, challenge negative thinking, and develop coping strategies. Use structured CBT approaches including thought records, behavioral activation, and problem-solving techniques. Maintain a professional but supportive tone. Always encourage professional therapy for serious concerns.',
     ARRAY['adults'], ARRAY['anxiety', 'depression', 'ptsd'], true, true),
     
    -- Teen-Friendly Support Agent
    ('Teen Support Agent', '1.0', 'casual', 0.8, 0.2, 0.8, 
     'short', 0.5, 0.7, 'humanistic', 0.4, 0.95, true, true, true, 
     0.3, 0.8, 800, 
     'You are a friendly AI companion designed to support teenagers. Use age-appropriate language, be relatable, and understand the unique challenges teens face. Show genuine care and avoid being preachy. Use contemporary language while maintaining appropriate boundaries. Be especially vigilant for crisis situations and always involve parents/guardians and professional help when needed.',
     ARRAY['teens'], ARRAY['anxiety', 'depression', 'stress', 'social_issues'], true, true),
     
    -- Crisis Intervention Specialist
    ('Crisis Intervention Agent', '1.0', 'professional', 0.9, 0.6, 0.3, 
     'medium', 0.3, 0.9, 'crisis_intervention', 0.9, 1.0, false, false, false, 
     0.1, 0.5, 1000, 
     'You are a specialized AI crisis intervention assistant. Your primary role is to assess crisis situations, provide immediate emotional support, and connect users with appropriate emergency resources. Always prioritize safety, validate feelings, and guide users to professional crisis services. Use de-escalation techniques and maintain a calm, supportive presence. Immediately escalate high-risk situations.',
     ARRAY['all'], ARRAY['suicidal_ideation', 'self_harm', 'crisis'], true, true),
     
    -- Mindfulness and Wellness Coach
    ('Mindfulness Coach Agent', '1.0', 'calm', 0.7, 0.5, 0.5, 
     'medium', 0.3, 0.6, 'mindfulness', 0.2, 0.7, true, false, false, 
     0.5, 0.6, 1000, 
     'You are a mindful AI wellness coach focused on meditation, mindfulness practices, and overall mental wellness. Guide users through breathing exercises, meditation techniques, and present-moment awareness. Use calming language and encourage self-compassion. Help users develop daily mindfulness practices and stress reduction techniques.',
     ARRAY['adults', 'seniors'], ARRAY['stress', 'anxiety', 'general_wellness'], true, false);

-- =============================================================================
-- JOURNAL PROMPTS LIBRARY
-- =============================================================================

INSERT INTO journal_prompts (
    category, subcategory, prompt_type, question, description, follow_up_questions,
    cbt_technique, therapeutic_goal, difficulty_level, target_emotions, 
    target_situations, age_group, clinical_conditions, is_active, language
) VALUES
    -- Daily Reflection Prompts
    ('daily_reflection', 'general', 'daily_reflection', 
     'How are you feeling today, and what contributed to this feeling?',
     'A general daily check-in to build self-awareness and emotional intelligence.',
     ARRAY['What emotions did you experience most strongly today?', 'What events or thoughts influenced your mood?', 'What would you like to focus on tomorrow?'],
     'mindfulness', 'Increase self-awareness and emotional regulation', 'beginner',
     ARRAY['any'], ARRAY['daily_routine'], 'all', ARRAY['general_wellness'], true, 'en'),
     
    ('daily_reflection', 'gratitude', 'gratitude', 
     'What are three things you''re grateful for today, and why?',
     'Focuses on positive aspects of life to improve mood and perspective.',
     ARRAY['How did these positive things make you feel?', 'How can you appreciate similar things tomorrow?', 'Who contributed to these positive experiences?'],
     'behavioral_activation', 'Improve mood and positive thinking', 'beginner',
     ARRAY['sadness', 'depression', 'low_mood'], ARRAY['daily_routine'], 'all', ARRAY['depression', 'general_wellness'], true, 'en'),
     
    -- Anxiety-Focused Prompts
    ('anxiety', 'worry', 'cbt_thought_record', 
     'What thoughts are going through your mind when you feel anxious?',
     'Helps identify anxious thoughts and cognitive patterns for CBT work.',
     ARRAY['How likely is this worry to actually happen?', 'What evidence supports or contradicts this thought?', 'What would you tell a friend having this worry?'],
     'thought_challenging', 'Reduce anxiety through cognitive restructuring', 'intermediate',
     ARRAY['anxiety', 'worry', 'panic'], ARRAY['work_stress', 'social_situations', 'health_concerns'], 'adult', ARRAY['anxiety', 'panic_disorder'], true, 'en'),
     
    ('anxiety', 'coping', 'free_writing', 
     'What helps you feel calm and grounded when anxiety rises?',
     'Identifies personal coping strategies and builds a toolkit for anxiety management.',
     ARRAY['Which of these strategies works best for you?', 'When do you remember to use these techniques?', 'What prevents you from using them sometimes?'],
     'grounding_exercises', 'Develop personalized anxiety coping strategies', 'beginner',
     ARRAY['anxiety', 'stress'], ARRAY['any'], 'all', ARRAY['anxiety', 'stress'], true, 'en'),
     
    -- Depression-Focused Prompts
    ('depression', 'mood', 'mood_exploration', 
     'When did you start feeling this way, and what was happening in your life?',
     'Explores the context and triggers around depressive episodes.',
     ARRAY['What thoughts accompanied these feelings?', 'How has this affected your daily activities?', 'What support do you have available?'],
     'behavioral_activation', 'Understand depression patterns and triggers', 'intermediate',
     ARRAY['sadness', 'depression', 'hopelessness'], ARRAY['life_changes', 'loss', 'stress'], 'adult', ARRAY['depression', 'bipolar'], true, 'en'),
     
    ('depression', 'activities', 'behavioral_activation', 
     'What activities usually bring you comfort or joy, even in small amounts?',
     'Identifies pleasurable activities for behavioral activation therapy.',
     ARRAY['When did you last do one of these activities?', 'What prevents you from doing them now?', 'Could you do a small version of one today?'],
     'behavioral_activation', 'Increase engagement in pleasurable activities', 'beginner',
     ARRAY['sadness', 'depression', 'anhedonia'], ARRAY['isolation', 'low_motivation'], 'all', ARRAY['depression'], true, 'en'),
     
    -- Stress Management Prompts
    ('stress', 'control', 'problem_solving', 
     'What''s causing you the most stress right now, and what aspects can you control?',
     'Helps differentiate between controllable and uncontrollable stressors.',
     ARRAY['What specific actions could you take on the controllable aspects?', 'How can you accept or cope with the uncontrollable parts?', 'Who could help you with this situation?'],
     'problem_solving', 'Develop effective stress management strategies', 'intermediate',
     ARRAY['stress', 'overwhelm', 'frustration'], ARRAY['work_stress', 'family_issues', 'financial_concerns'], 'adult', ARRAY['stress', 'anxiety'], true, 'en'),
     
    ('stress', 'coping_history', 'reflection', 
     'How have you successfully coped with stress in the past?',
     'Identifies existing strengths and successful coping strategies.',
     ARRAY['What made those strategies effective?', 'Could you apply any of those approaches now?', 'What would need to be different for them to work again?'],
     'problem_solving', 'Build on existing coping strengths', 'beginner',
     ARRAY['stress', 'anxiety'], ARRAY['any'], 'all', ARRAY['stress', 'anxiety'], true, 'en'),
     
    -- Trauma-Focused Prompts (Gentle)
    ('trauma', 'safety', 'free_writing', 
     'What helps you feel safe and grounded in this moment?',
     'Focuses on present-moment safety and grounding for trauma survivors.',
     ARRAY['What physical sensations help you feel calm?', 'What places make you feel secure?', 'Who are the people that make you feel safe?'],
     'grounding_exercises', 'Develop safety and grounding techniques', 'beginner',
     ARRAY['fear', 'anxiety', 'trauma'], ARRAY['trauma_recovery'], 'adult', ARRAY['ptsd', 'trauma'], true, 'en'),
     
    -- Relationship Prompts
    ('relationships', 'communication', 'reflection', 
     'How did your interactions with others make you feel today?',
     'Explores social connections and their impact on emotional well-being.',
     ARRAY['What kinds of interactions energize you?', 'Which interactions drain your energy?', 'How do you want to show up in relationships?'],
     'mindfulness', 'Improve relationship awareness and skills', 'intermediate',
     ARRAY['loneliness', 'anger', 'frustration'], ARRAY['social_situations', 'conflict'], 'all', ARRAY['social_anxiety', 'depression'], true, 'en'),
     
    -- Goal Setting and Future Focus
    ('goals', 'future', 'goal_setting', 
     'What small step could you take today toward something you care about?',
     'Encourages forward-focused thinking and small actionable steps.',
     ARRAY['What would achieving this goal mean to you?', 'What obstacles might you face?', 'Who could support you in this goal?'],
     'behavioral_activation', 'Increase motivation and goal-directed behavior', 'beginner',
     ARRAY['hopelessness', 'low_motivation'], ARRAY['life_transitions', 'low_motivation'], 'all', ARRAY['depression', 'general_wellness'], true, 'en'),
     
    -- Teen-Specific Prompts
    ('teen_issues', 'identity', 'free_writing', 
     'What''s one thing about yourself that you''re proud of today?',
     'Builds self-esteem and positive self-identity for adolescents.',
     ARRAY['How has this strength helped you recently?', 'How do others see this quality in you?', 'How can you use this strength to handle challenges?'],
     'mindfulness', 'Build positive self-identity and self-esteem', 'beginner',
     ARRAY['insecurity', 'low_self_esteem'], ARRAY['school', 'peer_pressure'], 'teen', ARRAY['adolescent_issues'], true, 'en'),
     
    ('teen_issues', 'peer_pressure', 'reflection', 
     'When do you feel most like yourself, and when do you feel pressure to be different?',
     'Explores authentic self-expression and peer influence for teens.',
     ARRAY['What situations make it hard to be yourself?', 'Who accepts you as you are?', 'What values are most important to you?'],
     'mindfulness', 'Develop authentic self-expression', 'intermediate',
     ARRAY['anxiety', 'insecurity'], ARRAY['peer_pressure', 'social_situations'], 'teen', ARRAY['social_anxiety', 'adolescent_issues'], true, 'en');

-- =============================================================================
-- SUBSCRIPTION PLANS
-- =============================================================================

INSERT INTO subscription_plans (
    plan_name, plan_type, description, 
    monthly_price, quarterly_price, semi_annual_price, annual_price,
    trial_days, trial_price,
    max_journal_entries, max_mood_entries_per_day, max_assessment_frequency_days,
    provider_coordination_included, premium_analytics_included, priority_support_included, ai_insights_included,
    is_active, is_visible, sort_order
) VALUES
    -- Free Trial Plan
    ('Free Trial', 'trial', '7-day free trial with basic features to explore the platform', 
     0.00, NULL, NULL, NULL,
     7, 0.00,
     10, 3, 7,
     false, false, false, false,
     true, true, 1),
    
    -- Basic Plan
    ('Basic Wellness', 'basic', 'Essential wellness tracking for personal mental health management',
     9.99, 27.99, 54.99, 99.99,
     7, 0.00,
     NULL, NULL, 1, -- unlimited journal entries, mood entries, daily assessments
     false, false, false, true,
     true, true, 2),
    
    -- Premium Plan  
    ('Premium Care', 'premium', 'Advanced features with provider coordination and premium analytics',
     19.99, 54.99, 107.99, 199.99,
     14, 0.00,
     NULL, NULL, 1,
     true, true, true, true,
     true, true, 3),
    
    -- Professional Plan
    ('Professional Plus', 'professional', 'Comprehensive platform for individuals working with healthcare providers',
     39.99, 107.99, 215.99, 399.99,
     14, 0.00,
     NULL, NULL, 1,
     true, true, true, true,
     true, true, 4),
    
    -- Enterprise Plan (for organizations)
    ('Enterprise', 'enterprise', 'Full-featured platform for healthcare organizations and large teams',
     99.99, 269.99, 539.99, 999.99,
     30, 0.00,
     NULL, NULL, 1,
     true, true, true, true,
     true, false, 5); -- Not visible to individual users

-- =============================================================================
-- SUBSCRIPTION COUPONS
-- =============================================================================

INSERT INTO subscription_coupons (
    code, name, description,
    discount_type, discount_value, currency,
    max_redemptions, max_redemptions_per_user,
    valid_from, valid_until,
    minimum_amount, first_time_customers_only,
    is_active
) VALUES
    -- Welcome discount
    ('WELCOME20', 'Welcome Discount', 'Get 20% off your first month',
     'percentage', 20.00, 'USD',
     1000, 1,
     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '6 months',
     NULL, true,
     true),
    
    -- Annual plan discount
    ('ANNUAL30', 'Annual Plan Discount', 'Save 30% when you choose annual billing',
     'percentage', 30.00, 'USD',
     NULL, 1, -- unlimited redemptions
     CURRENT_TIMESTAMP, NULL, -- no expiry
     99.99, false, -- minimum $99.99 purchase (annual plans)
     true),
    
    -- Student discount
    ('STUDENT50', 'Student Discount', 'Special 50% discount for verified students',
     'percentage', 50.00, 'USD',
     500, 1,
     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 year',
     NULL, false,
     true),
    
    -- Healthcare worker discount
    ('HEALTHCARE25', 'Healthcare Worker Discount', 'Thank you discount for healthcare professionals',
     'percentage', 25.00, 'USD',
     1000, 1,
     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '1 year',
     NULL, false,
     true),
    
    -- Extended trial
    ('TRIAL30', 'Extended Trial', 'Get 30 days free trial instead of 7',
     'free_trial', 23.00, 'USD', -- 23 extra days
     100, 1,
     CURRENT_TIMESTAMP, CURRENT_TIMESTAMP + INTERVAL '3 months',
     NULL, true,
     true);

-- =============================================================================
-- SYSTEM HEALTH CHECK CONFIGURATIONS
-- =============================================================================

-- Note: These would typically be inserted by the application, but included for completeness
INSERT INTO system_analytics (
    report_date, report_type, total_users, active_users, new_registrations,
    user_retention_rate, total_sessions, average_session_duration, 
    generated_by, data_freshness_hours
) VALUES
    (CURRENT_DATE, 'daily', 0, 0, 0, 0.0, 0, 0.0, 'initial_setup', 0);

-- =============================================================================
-- COMMENT DOCUMENTATION
-- =============================================================================

COMMENT ON TABLE system_configurations IS 'Initial system configuration values for application settings, feature flags, and operational parameters';
COMMENT ON TABLE crisis_resources IS 'Pre-loaded crisis intervention resources including hotlines, text lines, and specialized support services';
COMMENT ON TABLE crisis_keywords IS 'Crisis detection keyword library with severity weights for automated risk assessment';
COMMENT ON TABLE ai_agent_configs IS 'Pre-configured AI agent personalities optimized for different user demographics and therapeutic approaches';
COMMENT ON TABLE journal_prompts IS 'Therapeutic journal prompts library organized by category, difficulty, and target conditions';

-- =============================================================================
-- VERIFICATION QUERIES
-- =============================================================================
-- Uncomment these to verify data was inserted correctly:

-- SELECT COUNT(*) as config_count FROM system_configurations;
-- SELECT COUNT(*) as resource_count FROM crisis_resources;
-- SELECT COUNT(*) as keyword_count FROM crisis_keywords;
-- SELECT COUNT(*) as agent_config_count FROM ai_agent_configs;
-- SELECT COUNT(*) as prompt_count FROM journal_prompts;

-- =============================================================================
-- END OF INITIAL DATA
-- =============================================================================
